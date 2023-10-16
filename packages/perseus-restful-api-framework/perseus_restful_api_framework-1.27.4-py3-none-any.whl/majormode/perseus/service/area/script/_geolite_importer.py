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

import argparse
import re

REGEX_GEOLITE_COUNTRY = re.compile(r'^"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}","\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}","(\d+)","(\d+)","([A-Z]{2})",".*"$')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='GeoLite Country Importer')
    parser.add_argument('--file')
    arguments = parser.parse_args()

    with open(arguments.file) as file:
        print 'INSERT INTO _ip2country(from_ip, to_ip, country_code) VALUES %s' % \
            ','.join([ "(%s,%s,'%s')" % (match.group(1), match.group(2), match.group(3))
                         for match in [ REGEX_GEOLITE_COUNTRY.match(line) for line in file.readlines() ] if match ])
