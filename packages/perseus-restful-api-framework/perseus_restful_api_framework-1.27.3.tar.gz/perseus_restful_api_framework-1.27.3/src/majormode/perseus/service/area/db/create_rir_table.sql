/**
 * -*- coding: utf-8 -*-
 *
 * Copyright (C) 2013 Majormode.  All rights reserved.
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
 * Represent the last data update from Regional Internet Registry
 * (RIR) organizations, which manages the allocation and registration
 * of Internet number resources within a particular region of the
 * world.  Internet number resources include IP  addresses and
 * autonomous system (AS) numbers.
 *
 * The Regional Internet Registry system evolved over time, eventually
 * dividing the world into five RIRs:
 *
 * * African Network Information Centre (AfriNIC) for Africa
 *   (ftp.afrinic.net/pub/stats/afrinic/delegated-afrinic-latest)
 *
 * * American Registry for Internet Numbers (ARIN) for the United
 *   States, Canada, several parts of the Caribbean region, and
 *   Antarctica
 *   (ftp.arin.net/pub/stats/arin/delegated-arin-latest)
 *
 * * Asia-Pacific Network Information Centre (APNIC) for Asia,
 *   Australia, New Zealand, and neighboring countries
 *   (ftp.apnic.net/pub/stats/apnic/delegated-apnic-latest)
 *
 * * Latin America and Caribbean Network Information Centre (LACNIC)
 *   for Latin America and parts of the Caribbean region
 *   (ftp.lacnic.net/pub/stats/lacnic/delegated-lacnic-latest)
 *
 * * Réseaux IP Européens Network Coordination Centre (RIPE NCC) for
 *   Europe, Russia, the Middle East, and Central Asia
 *   (ftp.ripe.net/ripe/stats/delegated-ripencc-latest)
 *
 * @column registry: one value from the set of defined strings:
 *         * ``afrinic``
 *         * ``apnic``
 *         * ``arin``
 *         * ``iana``
 *         * ``lacnic``
 *         * ``ripencc``
 * @column md5_checksum: message digest of the last update that has
 *         been downloaded from this registry.
 * @column update_time: time of the last update from this registry.
 */
CREATE TABLE _rir_update
(
  registry     text                     NOT NULL,
  md5_checksum text                     NOT NULL,
  update_time  timestamp with time zone NOT NULL
);

/**
 * Represent allocation or assignment records downloaded from Regional
 * Internet Registries (RIR).
 *
 * A script is responsible to download data from RIRs using a
 * double buffering technique.  This script automatically builds a
 * table ``_rir_record`` in which records are being updated from RIRs
 * while client software components access to the "front buffer"
 * ``rir_record`` ; once the updates applied into the "back buffer"
 * table, "front buffer" and "back buffer" tables are switched.
 *
 * @column registry: one value from the set of defined strings:
 *         * ``afrinic``
 *         * ``apnic``
 *         * ``arin``
 *         * ``iana``
 *         * ``lacnic``
 *         * ``ripencc``
 * @column country_code: ISO 3166 2-letter code of the organization to
 *         which the allocation or assignment was made.
 * @column type: type of Internet number resource represented in this
 *         record. One value from the set of defined strings:
 *         * ``asn``
 *         * ``ipv4``
 *         * ``ipv6``
 * @column start: in the case of records of type 'ipv4' or 'ipv6' this
 *         is the IPv4 or IPv6 'first address' of the range.
 *         In the case of an 16 bit AS number the format is the
 *         integer value in the range 0 to 65535, in the case of a 32
 *         bit ASN the value is in the range 0 to 4294967296.  No
 *         distinction is drawn between 16 and 32 bit ASN values in
 *         the range 0 to 65535.
 * @column value: in the case of IPv4 address the count of hosts for
 *         this range.  This count does not have to represent a CIDR
 *         range.  In the case of an IPv6 address the value will be
 *         the CIDR prefix length from the 'first address' value of
 *         ``start``.  In the case of records of type 'asn' the number
 *         is the count of AS from this start value.
 * @column date: date on this allocation/assignment was made by the
 *         RIR.  Where the allocation or assignment has been
 *         transferred from another registry, this date represents the
 *         date of first assignment or allocation as received in from
 *         the original RIR.  It is noted that where records do not
 *         show a date of first assignment, this can take the null
 *         value status.
 * @column status: type of allocation from the set:
 *         * ``allocated``
 *         * ``assigned``
 *         This is the allocation or assignment made by the registry
 *         producing the file and not any sub-assignment by other
 *         agencies.
 */
CREATE TABLE rir_record
(
  registry     text                     NOT NULL,
  country_code char(2)                  NOT NULL,
  record_type  text                     NOT NULL,
  start        text                     NOT NULL,
  value        int                      NOT NULL,
  date         timestamp with time zone NULL,
  status       text                     NOT NULL
);
