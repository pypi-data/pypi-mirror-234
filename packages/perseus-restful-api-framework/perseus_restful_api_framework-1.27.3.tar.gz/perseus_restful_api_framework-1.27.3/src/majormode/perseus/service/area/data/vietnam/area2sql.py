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
# @version $Revision$

import json
import sys

import hashlib
import unidecode


{
    "city": "Hà Tĩnh",
    "ward": "Xã Phù Việt",
    "type": "ward",
    "district": "Huyện Thạch Hà",
    "coordinates": "18.4062614,105.824653,18.4044284,105.828567,18.4035224,105.828460,18.4015045,105.829559,18.4023742,105.830421,18.4022178,105.831855,18.4029731,105.832450,18.4019432,105.834419,18.4035491,105.834968,18.4031410,105.837493,18.4040870,105.838935,18.4036254,105.839958,18.4017295,105.840263,18.4017276,105.840896,18.4023399,105.841636,18.4036312,105.841049,18.4047298,105.841659,18.4049854,105.842277,18.4043865,105.843093,18.4035377,105.842155,18.4013710,105.842727,18.3997173,105.841636,18.3981876,105.841819,18.3973312,105.842582,18.3961143,105.841667,18.3934249,105.842300,18.3929862,105.841163,18.3912506,105.841171,18.3898391,105.843109,18.3882942,105.837867,18.3886795,105.837043,18.3895912,105.838104,18.3906021,105.837486,18.3886184,105.836433,18.3876380,105.834259,18.3865985,105.835357,18.3871135,105.835868,18.3864574,105.836517,18.3849525,105.835411,18.3836479,105.836372,18.3821239,105.836196,18.3822364,105.837265,18.3788585,105.837066,18.3773498,105.837913,18.3763427,105.826255,18.3789958,105.823135,18.3828163,105.821823,18.3826980,105.820167,18.3840007,105.821121,18.3860187,105.820648,18.3849201,105.814758,18.3855876,105.814262,18.3875904,105.815765,18.3878860,105.817115,18.3891639,105.817825,18.3925056,105.818313,18.3969402,105.815650,18.3968753,105.816978,18.4070739,105.820396,18.4079761,105.822326,18.4062614,105.824653"
}


if __name__ == "__main__":
    AREA_CODE_PREFIX_VIETNAM = 'asia.vietnam'

    AREA_TABLE_COLUMN_NAMES = (
        'area_id',
        'parent_area_id',
        'area_code',
        'area_type',
        'boundary'
    )

    def _normalize(name):
        return unidecode.unidecode(name.lower().replace(' ', '_').replace("'", "").replace('\\', ''))

    def _quote(value):
        return None if value is None else unicode(value).replace("'", "''").replace('\\', '\\\\')

    areas = json.loads(sys.stdin.read())
    if len(areas) > 0:
        for area in areas:
            area_code = AREA_CODE_PREFIX_VIETNAM
            area_code += '.%s' % area['city']
            if area['type'] in ['district', 'ward']:
                area_code += '.%s' % area['district']
            if area['type'] == 'ward':
                area_code += '.%s' % area['ward']

            area_code = _normalize(area_code)
            area['area_code'] = area_code
            area['area_id'] = hashlib.md5(area_code).hexdigest()
            area['parent_area_id'] = hashlib.md5(area_code[:area_code.rfind('.')]).hexdigest()

            coordinates = area['boundary'].split(',')
            # [PATCH]
            if len(coordinates) > 1:
                last_geo_offset = len(coordinates) - 2
                if coordinates[last_geo_offset] != coordinates[0] or \
                   coordinates[last_geo_offset + 1] != coordinates[1]:
                    coordinates.append(coordinates[0])
                    coordinates.append(coordinates[1])

            if len(coordinates) > 1:
                area['boundary'] = ','.join(['%s %s 0' % (coordinates[i * 2 + 1], coordinates[i * 2]) for i in range(len(coordinates) / 2) ])
                print unicode.encode("""INSERT INTO area(area_id, parent_area_id, area_code, area_type, boundary)
                    VALUES ('%(area_id)s', '%(parent_area_id)s', E'%(area_code)s', '%(area_type)s', ST_GeomFromText('POLYGON((%(boundary)s))',4326));""" % \
                    { 'area_code': _quote(area['area_code']),
                      'area_id': area['area_id'],
                      'area_type': area['type'],
                      'boundary': area['boundary'],
                      'parent_area_id': area['parent_area_id'] }, "utf-8")
            else:
                print unicode.encode("""INSERT INTO area(area_id, parent_area_id, area_code, area_type, boundary)
                    VALUES ('%(area_id)s', '%(parent_area_id)s', E'%(area_code)s', '%(area_type)s', NULL);""" % \
                    { 'area_code': _quote(area['area_code']),
                      'area_id': area['area_id'],
                      'area_type': area['type'],
                      'parent_area_id': area['parent_area_id'] }, "utf-8")

            print unicode.encode("INSERT INTO area_l10n(area_id, locale, label) VALUES ('%(area_id)s', 'vie', E'%(label)s');" % \
                { 'area_id': area['area_id'],
                  'label': _quote(area['city'] if area['type'] == 'city'\
                      else area['district'] if area['type'] == 'district' \
                      else area['ward']) }, "utf-8")
            print unicode.encode("INSERT INTO area_l10n(area_id, locale, label) VALUES ('%(area_id)s', 'eng', E'%(label)s');" % \
                { 'area_id': area['area_id'],
                  'label': _quote(unidecode.unidecode(area['city'] if area['type'] == 'city'\
                      else area['district'] if area['type'] == 'district' \
                      else area['ward'])) }, "utf-8")
