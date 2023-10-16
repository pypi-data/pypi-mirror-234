/**
 * -*- coding: utf-8 -*-
 *
 * Copyright (C) 2010 Majormode.  All rights reserved.
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
 * Represent the information of a geographic area, such as an
 * administrative division, provided in a given locale.
 *
 * @field area_id: unique identification of the geographical area.
 *
 * @field parent_area_id: identification of the parent geographical
 *     area, if any.
 *
 * @field centroid: geometry center of this area.
 *
 * @field bounding_box: maximum extents of the geographical area.
 *
 * @field area_type: name of the type of the geographical area, such
 *     as administrative divisions.  This name can have been localized.
 *     There is no naming convention as each country might have its own
 *     administrative division classification.
 *
 * @field area_level: administrative level of this area.  For clarity
 *     and convenience the standard neutral reference for the largest
 *     administrative subdivision of a country is called the "first-
 *     level administrative division" or "first administrative level".
 *     Next smaller is called "second-level administrative division" or
 *     "second administrative level".
 *
 * @field content: textual content of the label.
 *
 * @field locale: ISO 639-3 alpha-3 code element, optionally followed
 *     by a dash character "-" and a ISO 3166-1 alpha-2 code.  For
 *     example: "eng" (which denotes a standard English), "eng-US"
 *     (which denotes an American English).
 */
CREATE TYPE area_info AS (
  area_id        uuid,
  parent_area_id uuid,
  centroid       geometry,
  bounding_box   geometry,
  area_type      text,
  area_level     int,
  content        text,
  locale         text
);
