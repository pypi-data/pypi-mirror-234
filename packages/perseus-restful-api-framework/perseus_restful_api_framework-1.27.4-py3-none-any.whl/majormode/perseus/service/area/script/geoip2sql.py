#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2016 Majormode.  All rights reserved.
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


# GeoLite2 databases are free IP geolocation databases comparable to,
# but less accurate than, MaxMind’s GeoIP2 databases. GeoLite2 databases
# are updated on the first Tuesday of each month.
#
# IP geolocation is inherently imprecise. Locations are often near the
# center of the population.  Any location provided by a GeoIP database
# should not be used to identify a particular address or household.
#
# Use the Accuracy Radius as an indication of geolocation accuracy for
# the latitude and longitude coordinates we return for an IP address.
# The actual location of the IP address is likely within the area
# defined by this radius and the latitude and longitude coordinates.
#
# The GeoLite2 databases are distributed under the Creative Commons
# Attribution-ShareAlike 4.0 International License.  The attribution
# requirement may be met by including the following in all advertising
# and documentation mentioning features of or use of this database::
#
#     This product includes GeoLite2 data created by MaxMind, available
#     from <a href="http://www.maxmind.com">http://www.maxmind.com</a>.

from majormode.utils import file_util
from majormode.utils import zip_util

import argparse
import contextlib
import os
import re
import urllib2
import zipfile


# URL of the ZIP archive of GeoLite2 City database, which allows to
# determine the country, subdivisions, city, and postal code associated
# with IPv4 and IPv6 addresses worldwide.
GEOLITE2_CITY_ZIP_URL = 'http://geolite.maxmind.com/download/geoip/database/GeoLite2-City-CSV.zip'

# # URL of the ZIP archive of GeoLite Country database, which allows to
# # determine an Internet visitor's country based on their IP address.
# GEOLITE2_COUNTRY_ZIP_URL = 'http://geolite.maxmind.com/download/geoip/database/GeoLite2-Country-CSV.zip'


# REGEX_GEOIP_ZIP_FILE_NAME = re.compile(r'GeoLite2-City-CSV_(\d{8}).zip')



class GeoIP2BlockFile(object):
    # Name of the GeoIP2 block CSV file.
    GEOIP_BLOCK_CSV_FILE_NAME = 'GeoLite2-City-Blocks-IPv4.csv'

    # This is the IPv4 or IPv6 network in CIDR format such as “2.21.92.0/29”
    # or “2001:4b0::/80”.
    FIELD_NAME_NETWORK = 'network'

    # A unique identifier for the network’s location as specified by
    # GeoNames (http://www.geonames.org/).  This ID can be used to look up
    # the location information in the Location file.
    FIELD_NAME_GEONAME_ID = 'geoname_id'

    # The registered country is the country in which the ISP has registered
    # the network.  This column contains a unique identifier for the
    # network’s registered country as specified by GeoNames.  This ID can
    # be used to look up the location information in the Location file.
    FIELD_NAME_REGISTERED_COUNTRY_GEONAME_ID = 'registered_country_geoname_id'

    # The represented country is the country which is represented by users
    # of the IP address. For instance, the country represented by an
    # overseas military base. This column contains a unique identifier for
    # the network’s registered country as specified by GeoNames.  This ID
    # can be used to look up the location information in the Location file.
    FIELD_NAME_REPRESENTED_COUNTRY_GEONAME_ID = 'represented_country_geoname_id'

    # Deprecated. Please see our GeoIP2 Anonymous IP database
    # (https://www.maxmind.com/en/geoip2-anonymous-ip-database) to
    # determine whether the IP address is used by an anonymizing service.
    FIELD_NAME_IS_ANONYMOUS_PROXY = 'is_anonymous_proxy'

    # Deprecated. Please see our GeoIP2 Anonymous IP database.
    FIELD_NAME_IS_SATELLITE_PROVIDER = 'is_satellite_provider'

    # The postal code associated with the IP address.  These are available
    # for some IP addresses in Australia, Canada, France, Germany, Italy,
    # Spain, Switzerland, United Kingdom, and the US.  We return the first
    # 3 characters for Canadian postal codes.  We return the the first 2-4
    # characters (outward code) for postal codes in the United Kingdom.
    FIELD_NAME_POSTAL_CODE = 'postal_code'

    # The approximate latitude of the location associated with the network.
    # This value is not precise and should not be used to identify a
    # particular address or household.
    FIELD_NAME_LATITUDE = 'latitude'

    # The approximate longitude of the location associated with the network.
    # Latitude and Longitude are often near the center of population.  These
    # values are not precise and should not be used to identify a particular
    # address or household.
    FIELD_NAME_LONGITUDE = 'longitude'

    # The radius in kilometers around the specified location where the IP
    # address is likely to be.
    FIELD_NAME_ACCURACY_RADIUS = 'accuracy_radius'

    FIELD_NAMES = [
        FIELD_NAME_NETWORK,
        FIELD_NAME_GEONAME_ID,
        FIELD_NAME_REGISTERED_COUNTRY_GEONAME_ID,
        FIELD_NAME_REPRESENTED_COUNTRY_GEONAME_ID,
        FIELD_NAME_IS_ANONYMOUS_PROXY,
        FIELD_NAME_IS_SATELLITE_PROVIDER,
        FIELD_NAME_POSTAL_CODE,
        FIELD_NAME_LATITUDE,
        FIELD_NAME_LONGITUDE,
        FIELD_NAME_ACCURACY_RADIUS
    ]


    COLUMN_NAME_NETWORK = 'network'
    COLUMN_NAME_GEONAME_ID = 'geoname_id'
    COLUMN_NAME_REGISTERED_COUNTRY_GEONAME_ID = 'registered_country_geoname_id'
    COLUMN_NAME_REPRESENTED_COUNTRY_GEONAME_ID = 'represented_country_geoname_id'
    COLUMN_NAME_POSTAL_CODE = 'postal_code'
    COLUMN_NAME_LOCATION = 'location'
    COLUMN_NAME_ACCURACY = 'accuracy'

    COLUMN_NAMES = [
        COLUMN_NAME_NETWORK,
        COLUMN_NAME_GEONAME_ID,
        COLUMN_NAME_REGISTERED_COUNTRY_GEONAME_ID,
        COLUMN_NAME_REPRESENTED_COUNTRY_GEONAME_ID,
        COLUMN_NAME_POSTAL_CODE,
        COLUMN_NAME_LOCATION,
        COLUMN_NAME_ACCURACY
    ]

    @staticmethod
    def csv_to_sql(fd):
        """
        Generate the SQL values representing each block contained in the
        GeoIP2 block CSV file.


        @warning: the function makes the assumption that the CSV fields are
            given in the order described in MaxMind's specifications, i.e., as
            declared in the array ``FIELD_NAMES``.


        @param fd: file descriptor of a GeoIP2 block CSV file.


        @return: a generator of SQL values representing each block contained
            in the GeoIP2 block CSV file.
        """
        # Retrieve the names of the fields from the GeoIP2 block CSV file.
        field_names = fd.readline().strip().split(',')

        # Check whether some fields are unknown or missing.
        unknown_field_names = [ field_name for field_name in field_names
                if field_name not in GeoIP2BlockFile.FIELD_NAMES ]
        assert not unknown_field_names, 'Unsupported GeoIP2 block field(s): ' % ', '.join(unknown_field_names)

        missing_field_names = [ field_name for field_name in GeoIP2BlockFile.FIELD_NAMES
                if field_name not in field_names ]
        assert not missing_field_names, 'Missing GeoIP2 block field(s): ' % ', '.join(missing_field_names)

        # Parse each line of GeoIP2 block and generate the corresponding SQL
        # values.
        for line in fd:
            (network,
             geoname_id,
             registered_country_geoname_id,
             represented_country_geoname_id,
             _, # @deprecated is_anonymous_proxy
             _, # @deprecated is_satellite_provider
             postal_code,
             latitude,
             longitude,
             radius) = line.strip().split(',')

            yield [
                network,
                geoname_id,
                registered_country_geoname_id,
                represented_country_geoname_id,
                postal_code,
                longitude and latitude and 'SRID=4326;POINT(%s %s)' % (longitude, latitude),
                radius ]


class GeoIP2LocationFile(object):
    # Regular expression that matches the name of a GeoIP2 location CSV
    # file.
    REGEX_GEOIP_LOCATION_CSV_FILE_NAME = re.compile(r'GeoLite2-City-Locations-(([a-z]{2,3}-[A-Z]{2})|[a-z]{2,3}).csv')

    # Regular expression that matches a value in a CSV file that is not
    # properly quoted.
    REGEX_QUOTED_UNQUOTED_CSV_VALUE = re.compile(r'(?:^|,)(\"(?:[^\"]+|\"\")*\"|[^,]*)')

    # A unique identifier for the a location as specified by GeoNames.  This
    # ID can be used as a key for the Location file.
    FIELD_NAME_GEONAME_ID = 'geoname_id'

    # The locale that the names in this row are in. This will always
    # correspond to the locale name of the file.
    FIELD_NAME_LOCALE_CODE = 'locale_code'

    # The continent code for this location. Possible codes are:
    #
    #   * ``AF``: Africa
    #   * ``AN``: Antarctica
    #   * ``AS``: Asia
    #   * ``EU``: Europe
    #   * ``NA``: North America
    #   * ``OC``: Oceania
    #   * ``SA``: South America
    FIELD_NAME_CONTINENT_CODE = 'continent_code'

    # The continent name for this location in the file’s locale.
    FIELD_NAME_CONTINENT_NAME = 'continent_name'

    # A two-character ISO 3166-1 country code for the country associated
    # with the location.
    FIELD_NAME_COUNTRY_ISO_CODE = 'country_iso_code'

    # The country name for this location in the file’s locale.
    FIELD_NAME_COUNTRY_NAME = 'country_name'

    # A string of up to three characters containing the region-portion of
    # the ISO 3166-2 code for the first level region associated with the IP
    # address. Some countries have two levels of subdivisions, in which case
    # this is the least specific. For example, in the United Kingdom this
    # will be a country like “England”, not a county like “Devon”.
    FIELD_NAME_SUBDIVISION_1_ISO_CODE = 'subdivision_1_iso_code'

    # The subdivision name for this location in the file’s locale.  As with
    # the subdivision code, this is the least specific subdivision for the
    # location.
    FIELD_NAME_SUBDIVISION_1_NAME = 'subdivision_1_name'

    # A string of up to three characters containing the region-portion of
    # the ISO 3166-2 code for the second level region associated with the
    # IP address.  Some countries have two levels of subdivisions, in which
    # case this is the most specific. For example, in the United Kingdom
    # this will be a a county like “Devon”, not a country like “England”.
    FIELD_NAME_SUBDIVISION_2_ISO_CODE = 'subdivision_2_iso_code'

    # The subdivision name for this location in the file’s locale.  As with
    # the subdivision code, this is the most specific subdivision for the
    # location.
    FIELD_NAME_SUBDIVISION_2_NAME = 'subdivision_2_name'

    # The city name for this location in the file’s locale.
    FIELD_NAME_CITY_NAME = 'city_name'

    # The metro code associated with the IP address.  These are only
    # available for networks in the US. MaxMind provides the same metro
    # codes as used by DoubleClick.
    FIELD_NAME_METRO_CODE = 'metro_code'

    # The time zone associated with location, as specified by the IANA Time
    # Zone Database, e.g., “America/New_York”.
    FIELD_NAME_TIME_ZONE = 'time_zone'
    
    FIELD_NAMES = [
        FIELD_NAME_GEONAME_ID,
        FIELD_NAME_LOCALE_CODE,
        FIELD_NAME_CONTINENT_CODE,
        FIELD_NAME_CONTINENT_NAME,
        FIELD_NAME_COUNTRY_ISO_CODE,
        FIELD_NAME_COUNTRY_NAME,
        FIELD_NAME_SUBDIVISION_1_ISO_CODE,
        FIELD_NAME_SUBDIVISION_1_NAME,
        FIELD_NAME_SUBDIVISION_2_ISO_CODE,
        FIELD_NAME_SUBDIVISION_2_NAME,
        FIELD_NAME_CITY_NAME,
        FIELD_NAME_METRO_CODE,
        FIELD_NAME_TIME_ZONE
    ]

    @staticmethod
    def csv_to_sql(fd):
        # Retrieve the names of the fields from the GeoIP2 location CSV file.
        field_names = fd.readline().strip().split(',')

        # Check whether some fields are unknown or missing.
        unknown_field_names = [ field_name for field_name in field_names
                if field_name not in GeoIP2LocationFile.FIELD_NAMES ]
        assert not unknown_field_names, 'Unsupported GeoIP2 block field(s): ' % ', '.join(unknown_field_names)

        missing_field_names = [ field_name for field_name in GeoIP2LocationFile.FIELD_NAMES
                if field_name not in field_names ]
        assert not missing_field_names, 'Missing GeoIP2 block field(s): ' % ', '.join(missing_field_names)

        # Parse each line of GeoIP2 block and generate the corresponding SQL
        # values.
        for line in fd:
            values = GeoIP2LocationFile.REGEX_QUOTED_UNQUOTED_CSV_VALUE.findall(line.strip())
            assert len(values) > 0, 'The specified entry does not correspond to a valid CSV line'
            yield [ value.replace('"', '') for value in values ]


def fetch_latest_geolite2_zip_file(url, path_name):
    """
    Download the ZIP archive of the latest version of the GeoLite2
    database.

    The function checks whether a previous ZIP archive of the GeoLite2
    database has been downloaded, and whether this archive corresponds to
    the latest version available.  If so, the function immediately returns
    the path and name of this file.


    @param url: Uniform Resource Locator (URL) of the ZIP archive of the
        latest version of the GeoLite2 database hosted on MaxMind's server.

    @param path_name: name of the local path where to store this ZIP
        archive file.


    @return: path and name of the ZIP archive file of the latest version
        of the GeoLite2 database is stored in.
    """
    file_util.make_directory_if_not_exists(path_name)

    zip_file_name = os.path.basename(url)
    geolite2_zip_file_path_name = os.path.join(path_name, zip_file_name)
    geolite2_md5_zip_file_path_name = os.path.join(path_name, zip_file_name + '.md5')

    opener = urllib2.build_opener()
    opener.addheaders = [ ('User-agent', 'Mozilla/5.0') ]

    with contextlib.closing(opener.open(GEOLITE2_CITY_ZIP_URL + '.md5', None, 5)) as url_handle:
        md5_digest = url_handle.read()

    if os.path.exists(geolite2_md5_zip_file_path_name):
        with open(geolite2_md5_zip_file_path_name, 'rt') as file_handle:
            previous_md5_digest = file_handle.read()
            if md5_digest == previous_md5_digest:
                return geolite2_zip_file_path_name

    with contextlib.closing(opener.open(url, None, 5)) as url_handle:
        with open(geolite2_zip_file_path_name, 'wb') as file_handle:
            file_handle.write(url_handle.read())

    with open(geolite2_md5_zip_file_path_name, 'wt') as file_handle:
        file_handle.write(md5_digest)

    return geolite2_zip_file_path_name


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', dest='path_name', metavar='pathname', default='~/.geolite2',
            help='specify the absolute path of the directory GeoLite ZIP archive is stored in')
    arguments = parser.parse_args()

    # Fetch the ZIP archive file of the latest version of the GeoLite2
    # database, whether from the cache, whether from MaxMind's server.
    zip_file_path_name = fetch_latest_geolite2_zip_file(GEOLITE2_CITY_ZIP_URL, os.path.expanduser(arguments.path_name))
    zip_file = zipfile.ZipFile(zip_file_path_name)

    # Parse the GeoIP2 block CSV file stored as an entry of the ZIP archive.
    for entry_file_name in zip_file.filelist:
        if os.path.basename(entry_file_name.filename) == GeoIP2BlockFile.GEOIP_BLOCK_CSV_FILE_NAME:
            print 'COPY geoip_block(%s) FROM stdin;' % ','.join(GeoIP2BlockFile.COLUMN_NAMES)

            fd = zip_util.open_entry_file(zip_file, entry_file_name)
            for values in GeoIP2BlockFile.csv_to_sql(fd):
                print '\t'.join([ value or r'\N' for value in values ])

            print '\\.\n'
            fd.close()

            break

    # Parse the various translated GeoIP location CSV files stored as
    # entries of the ZIP archive.
    geoip2_location_file_exists = False

    for entry_file_name in zip_file.filelist:
        if GeoIP2LocationFile.REGEX_GEOIP_LOCATION_CSV_FILE_NAME.match(os.path.basename(entry_file_name.filename)):
            if not geoip2_location_file_exists:
                print 'COPY geoip_location(%s) FROM stdin;' % ','.join(GeoIP2LocationFile.FIELD_NAMES)
                geoip2_location_file_exists = True

            fd = zip_util.open_entry_file(zip_file, entry_file_name)
            for values in GeoIP2LocationFile.csv_to_sql(fd):
                print '\t'.join([ value or r'\N' for value in values ])

            fd.close()

        if geoip2_location_file_exists:
            geoip2_location_file_exists = False
            print '\\.\n'
