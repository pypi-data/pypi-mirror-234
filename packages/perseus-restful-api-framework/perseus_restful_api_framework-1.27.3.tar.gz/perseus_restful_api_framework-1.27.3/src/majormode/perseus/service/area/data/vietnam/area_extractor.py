#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2010 Majormode.  All rights reserved.
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
# @version $Revision: 274 $

from __future__ import with_statement
from xml.dom import minidom

import contextlib
import json
import jsonpickle
import sys
import time
import urllib2

class Area(object):
    AREA_TYPE_CITY = 'city'
    AREA_TYPE_DISTRICT = 'district'
    AREA_TYPE_WARD = 'ward'

    def __init__(self, name, boundary):
        names = [ n.strip() for n in name.split('/') ]
        if len(names) == 1:
            self.type = Area.AREA_TYPE_CITY
            (self.city, ) = names
        elif len(names) == 2:
            self.type = Area.AREA_TYPE_DISTRICT
            (self.city, self.district) = names
        elif len(names) == 3:
            self.type = Area.AREA_TYPE_WARD
            (self.city, self.district, self.ward) = names
        else:
            raise ValueError('The name of this area is of an unexpected composition')

        self.boundary = boundary.replace('*#', ' ').replace('*', ',').replace(' ', ',')

discovered_areas = dict()

def parse_area_data(url):
    # {s1:'21.3852558,105.801338,...',s2:'TP.Hà Nội',s3:'28'}]}

    for __attempt__ in range(3):
        try:
            with contextlib.closing(urllib2.urlopen(url)) as response:
                data = response.read()

                start_index = data.find("s1:'")
                if start_index == -1:
                    return None

                end_index = data.find("',s2:'", start_index + 4)
                boundary = data[start_index + 4:end_index]

                start_index = data.find("s2:'")
                end_index = data.find("',s3:", start_index + 4)
                name = data[start_index + 4:end_index]

                area = Area(name, boundary)
                if area.type == Area.AREA_TYPE_CITY:
                    sys.stderr.write(area.city)
                elif area.type == Area.AREA_TYPE_DISTRICT:
                    sys.stderr.write('\t' + area.district)
                else:
                    sys.stderr.write('\t\t' + area.ward)
                sys.stderr.write('\n')
                sys.stderr.flush()

                return area

        except urllib2.URLError, exception:
            sys.stderr.write(str(exception))
            time.sleep(2)


def parse_area(url):
    # <div class="NameCity">
    #  <a href="http://muabannhadat.com.vn/ban-do/ban-do-Quan-Ba-Dinh-TP-Ha-Noi-q241-t28/"
    #     class="LinkCity">
    #   Bản đồ Q.Ba Đình
    #  </a>
    # </div>
    if discovered_areas.has_key(url):
        return

    for _attempt_ in range(3):
        try:
            with contextlib.closing(urllib2.urlopen(url)) as response:
                data = response.read()

                start_index = data.find('http://muabannhadat.com.vn/nvc/')
                if start_index > 0:
                    end_index = data.find('"', start_index)
                    area = parse_area_data(data[start_index:end_index])
                    if area is not None:
                        discovered_areas[url] = area

                start_index = data.find('<div class="CityManila">')
                end_index = data.find('\t<div class="clr_both">')
                xmldoc = minidom.parseString(data[start_index:end_index]).documentElement
                for divnode in xmldoc.getElementsByTagName('div'):
                    if divnode.getAttribute('class') != 'NameCity':
                        raise Exception("Unexpected HTML page format: doesn't contain div class of NameCity")
                    if len(divnode.childNodes) != 1:
                        raise Exception('Unexpected number of URL links to a geographic area')
                    anode = divnode.childNodes[0]
                    if anode.getAttribute('class') != 'LinkCity':
                        raise Exception('Unexpected class for a HTML reference of a geographic area')
                    parse_area(anode.getAttribute('href'))
            break
        except urllib2.URLError, exception:
            sys.stderr.write(str(exception))
            time.sleep(2)

if __name__ == "__main__":
    parse_area('http://muabannhadat.com.vn/ban-do/ban-do-viet-nam/')
    sys.stdout.write(json.dumps(jsonpickle.Pickler(unpicklable=False).flatten(discovered_areas.values()), indent=2))
    sys.stdout.flush()
