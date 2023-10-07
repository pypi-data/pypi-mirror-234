# -*- coding: utf-8 -*-
#
# Copyright (C) 2013 Majormode.  All rights reserved.
#
# This software is the confidential and proprietary information of
# Majormode or one of its subsidiaries.  You shall not disclose this
# confidential information and shall use it only in accordance with
# the terms of the license agreement or other applicable agreement you
# entered into with Majormode.
#
# MAJORMODE MAKES NO REPRESENTATIONS OR WARRANTIES ABOUT THE
# SUITABILITY OF THE SOFTWARE, EITHER EXPRESS OR IMPLIED, INCLUDING
# BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE, OR NON-INFRINGEMENT.  MAJORMODE
# SHALL NOT BE LIABLE FOR ANY LOSSES OR DAMAGES SUFFERED BY LICENSEE
# AS A RESULT OF USING, MODIFYING OR DISTRIBUTING THIS SOFTWARE OR ITS
# DERIVATIVES.
#
# @version $Revision$

from majormode.perseus.model import rir
from majormode.utils import cast
from majormode.utils import ftp_util
from majormode.utils import postgresql_util
from majormode.utils import rdbms

import datetime
import dateutil
import os
import settings
import sys


# Minimum time interval between updates, in seconds.
MINIMUM_TIME_INTERVAL_BETWEEN_UPDATES = 60 * 60 * 24 * 30

# Path on the local file system where files downloaded from Regional
# Internet Registry are going to be stored into.
FILE_DOWNLOAD_PATH = '/tmp'

if __name__ == '__main__':
    # Check with Regional Internet Registry has new update to be
    # downloaded.
    updated_rir_statistics = []
    for (rir_name, registry, hostname, remote_path, remote_file_name) in rir.RIR_PROPERTIES:
        with rdbms.RdbmsConnection.acquire_connection(settings.RDBMS_CONNECTION_PROPERTIES) as connection:
            cursor = connection.execute("""
                SELECT md5_checksum,
                       update_time
                  FROM _rir_update
                  WHERE registry = %(registry)s""",
                { 'registry': registry })
            row = cursor.fetch_one()
            last_update = row and row.get_object({ 'update_time': cast.string_to_timestamp })
            if last_update and (datetime.datetime.now(dateutil.tz.tzlocal()) - last_update.update_time).total_seconds() < MINIMUM_TIME_INTERVAL_BETWEEN_UPDATES:
                continue

            sys.stdout.write('Retrieving MD5 checksum for %s...\n' % rir_name)
            md5_file_name ='%s.md5' % remote_file_name
            ftp_util.get_file(hostname, 'anonymous', 'joebar@example.com',
                remote_path, md5_file_name, local_path=FILE_DOWNLOAD_PATH, debug=False)

            with open(os.path.join(FILE_DOWNLOAD_PATH, md5_file_name)) as file:
                md5_checksum = file.read().split('=')[1].strip()

            if last_update is None or md5_checksum != last_update.md5_checksum:
                updated_rir_statistics.append((rir_name, registry, hostname, remote_path, remote_file_name, last_update, md5_checksum))

    # Update the Regional Internet Registry records cached into database.
    if len(updated_rir_statistics) > 0:
        with rdbms.RdbmsConnection.acquire_connection(settings.RDBMS_CONNECTION_PROPERTIES, auto_commit=True) as connection:
            if not postgresql_util.does_table_exist(connection, '_rir_record'):
                connection.execute("""
                    CREATE TABLE _rir_record AS
                      SELECT * FROM rir_record LIMIT 0""") # Trick to create a table with the same structure

            # Remove records that have been lastly downloaded from registries
            # that have new content.
            connection.execute("""
                DELETE FROM _rir_record
                  WHERE registry IN (%[registries]s)""",
                { 'registries': [ registry for (_, registry, _, _, _, _, _) in updated_rir_statistics ] })

            for (rir_name, registry, hostname, remote_path, remote_file_name, last_update, md5_checksum) in updated_rir_statistics:
                sys.stdout.write('Downloading data from %s...' % rir_name)
                ftp_util.get_file(hostname, 'anonymous', 'joebar@example.com',
                    remote_path, remote_file_name, local_path=FILE_DOWNLOAD_PATH, debug=True)
                print

                sys.stdout.write('Processing data from %s...' % rir_name)
                print
                rir_statistics = rir.RIRStatistics.from_file(os.path.join(FILE_DOWNLOAD_PATH, remote_file_name))

                sys.stdout.write('Storing data from %s...' % rir_name)
                print
                connection.execute("""
                    INSERT INTO _rir_record(
                                    registry,
                                    country_code,
                                    record_type,
                                    start,
                                    value,
                                    date,
                                    status)
                      VALUES %[values]s""",
                    { 'values': [ (record.registry, record.country_code, record.type,
                                   record.start, record.value, record.date, record.status)
                          for record in rir_statistics.records ] })

                if last_update:
                    connection.execute("""
                        UPDATE _rir_update
                          SET md5_checksum = %(md5_checksum)s,
                              update_time = current_timestamp
                          WHERE registry = %(registry)s""",
                        { 'md5_checksum': md5_checksum,
                          'registry': registry })
                else:
                    connection.execute("""
                        INSERT INTO _rir_update(
                                        registry,
                                        md5_checksum,
                                        update_time)
                          VALUES (%(registry)s,
                                  %(md5_checksum)s,
                                  current_timestamp)""",
                        { 'md5_checksum': md5_checksum,
                          'registry': registry })

            # Switch a copy of the back table and the front table.
            connection.execute("""
                CREATE TABLE __rir_record AS
                   SELECT * FROM _rir_record""")
            connection.execute('DROP TABLE rir_record')
            connection.execute('ALTER TABLE __rir_record RENAME TO rir_record')
