/**
 * Copyright (C) 2016 Majormode.  All rights reserved.
 *
 * This software is the confidential and proprietary information of
 * Majormode or one of its subsidiaries.  You shall not disclose this
 * confidential information and shall use it only in accordance with
 * the terms of the license agreement or other applicable agreement you
 * entered into with Majormode.
 *
 * MAJORMODE MAKES NO REPRESENTATIONS OR WARRANTIES ABOUT THE
 * SUITABILITY OF THE SOFTWARE, EITHER EXPRESS OR IMPLIED, INCLUDING
 * BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE, OR NON-INFRINGEMENT.  MAJORMODE
 * SHALL NOT BE LIABLE FOR ANY LOSSES OR DAMAGES SUFFERED BY LICENSEE
 * AS A RESULT OF USING, MODIFYING OR DISTRIBUTING THIS SOFTWARE OR ITS
 * DERIVATIVES.
 *
 * @version $Revision$
 */

/**
 * Represent geolocation associated to IP Internet ranges. IP
 * geolocation are inherently imprecise. Locations are often near the
 * center of the population. Any location provided by a GeoIP database
 * should not be used to identify a particular address or household.
 *
 *
 * @column network: IP network as a string.  This is the IPv4 or IPv6
 *     network in CIDR format such as “2.21.92.0/29” or “2001:4b0::/80”.
 *
 * @column geoname_id: A unique identifier for the network’s location as
 *     specified by GeoNames. This ID can be used to look up the location
 *     information in the Location file.
 *
 * @column registered_country_geoname_id: The registered country is the
 *     country in which the ISP has registered the network. This column
 *     contains a unique identifier for the network’s registered
 *     country as specified by GeoNames.
 *
 * @column represented_country_geoname_id: The represented country is
 *     the country which is represented by users of the IP address. For
 *     instance, the country represented by an overseas military base.
 *     This column contains a unique identifier for the network’s
 *     registered country as specified by GeoNames.
 *
 * @column postal_code: The postal code associated with the IP address.
 *     These are available for some IP addresses in Australia, Canada,
 *     France, Germany, Italy, Spain, Switzerland, United Kingdom, and
 *     the US. We return the first 3 characters for Canadian postal
 *     codes. We return the the first 2-4 characters (outward code) for
 *     postal codes in the United Kingdom.
 *
 * @column location: The approximate location associated with the
 *     network. This value is not precise and should not be used to
 *     identify a particular address or household.
 *
 * @column accuracy: The radius in kilometers around the specified
 *     location where the IP address is likely to be. This field will only
 *     be available on or after May 3, 2016, for GeoLite2 and on or after
 *     May 10, 2016, for GeoIP2.
 *
 *
 * @depends: ip4r
 *     [https://github.com/RhodiumToad/ip4r]
 *     IP4R  - IPv4/v6 and IPv4/v6 range index type for PostgreSQL
 *
 *     While PostgreSQL already has builtin types 'inet' and 'cidr', the
 *     authors of this module found that they had a number of requirements
 *     that were not addressed by the builtin type.
 *
 *     Firstly and most importantly, the builtin types have no support for
 *     index lookups of the form (column >>= parameter), i.e. where you have
 *     a table of IP address ranges and wish to find which ones include a
 *     given IP address.  This requires an rtree or gist index to do
 *     efficiently, and also requires a way to represent IP address ranges
 *     that do not fall precisely on CIDR boundaries.
 *
 *     Installation procedure:
 *
 *         sudo su postgres
 *         psql -c "CREATE EXTENSION ip4r" <database_name>_<env>
 */
CREATE TABLE geoip_block
(
  network                        ip4r           NOT NULL,
  geoname_id                     int            NULL,
  registered_country_geoname_id  int            NULL,
  represented_country_geoname_id int            NULL,
  postal_code                    text           NULL,
  location                       geometry       NULL,
  accuracy                       int            NULL,
  creation_time                  timestamptz(3) NOT NULL DEFAULT current_timestamp
);


/**
 * Localised information of locations.
 *
 * @column geoname_id: A unique identifier for the a location as
 *     specified by GeoNames.
 *
 * @column locale_code: The locale that the names in this row are in.
 *
 * @column continent_code:  The continent code for this location.
 *     Possible codes are:
 *
 *     * `AF`: Africa
 *     * `AN`: Antarctica
 *     * `AS`: Asia
 *     * `EU`: Europe
 *     * `NA`: North America
 *     * `OC`: Oceania
 *     * `SA`: South America
 *
 * @column continent_name: The continent name of this location in the
 *     specified locale.
 *
 * @column country_iso_code	string: A two-character ISO 3166-1 country
 *     code for the country associated with the location.
 *
 * @country_name: The country name for this location in the specified
 *     locale.
 *
 * @column subdivision_1_iso_code: A string of up to three characters
 *     containing the region-portion of the ISO 3166-2 code for the first
 *     level region associated with the IP address. Some countries have
 *     two levels of subdivisions, in which case this is the least
 *     specific. For example, in the United Kingdom this will be a
 *     country like “England”, not a county like “Devon”.
 *
 * @column subdivision_1_name: The subdivision name for this location in
 *     the specified locale. As with the subdivision code, this is the
 *     least specific subdivision for the location.
 *
 * @column subdivision_2_iso_code: A string of up to three characters
 *     containing the region-portion of the ISO 3166-2 code for the
 *     second level region associated with the IP address. Some countries
 *     have two levels of subdivisions, in which case this is the most
 *     specific. For example, in the United Kingdom this will be a county
 *     like “Devon”, not a country like “England”.
 *
 * @column subdivision_2_name: The subdivision name for this location in
 *     the specified locale. As with the subdivision code, this is the
 *     most specific subdivision for the location.
 *
 * @column city_name: The city name for this location in the specified
 *    locale.
 */
CREATE TABLE geoip_location
(
  geoname_id             bigint     NOT NULL,
  locale_code            varchar(6) NULL,
  continent_code         char(2)    NULL,
  continent_name         text       NULL,
  country_iso_code       char(2)    NULL,
  country_name           text       NULL,
  subdivision_1_iso_code varchar(3) NULL,
  subdivision_1_name     text       NULL,
  subdivision_2_iso_code varchar(3) NULL,
  subdivision_2_name     text       NULL,
  city_name              text       NULL,

  -- The metro code associated with the IP address.  These are only
  -- available for networks in the US. MaxMind provides the same metro
  -- codes as the Google AdWords API.
  metro_code             int        NULL,

  -- The time zone associated with location, as specified by the IANA Time
  -- Zone Database, e.g., "America/New_York".
  time_zone text NULL
);
