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
 * An administrative division, or more commonly called an "area", is a
 * demarcated geographic area of the Earth, such as a portion of a
 * country or other region delineated for the purpose of administration.
 *
 * Countries are divided up into these smaller units.  For example, a
 * country may be divided into provinces, which, in turn, are divided
 * into counties, which, in turn, may be divided in whole or in part
 * into municipalities; and so on.
 *
 * @todo: ISO 3166-2 is part of the ISO 3166 standard published by the
 *     International Organization for Standardization (ISO), and
 *     defines codes for the names of the principal subdivisions (e.g.,
 *     provinces or states) of all countries coded in ISO 3166-1.  The
 *     official name of the standard is Codes for the representation of
 *     names of countries and their subdivisions – Part 2: Country
 *     subdivision code.
 */
CREATE TABLE area
(
  -- Identification of the geographical area.
  area_id uuid NOT NULL,

  -- Identification of its parent area, if any.
  parent_area_id uuid NULL,

  -- Code used to reference this area in the 3rd party GIS standard this
  -- area has been imported from.  This code should be used to update
  -- area's data during future synchronization with this 3rd party GIS.
  area_code text NOT NULL,

  -- Name of the type of the geographical area, such as administrative
  -- divisions.  This name can have been localized.  There is no naming
  -- convention as each country might have its own administrative division
  -- classification.
  area_type text NULL,

  -- Administrative level of this area.  For clarity and convenience the
  -- standard neutral reference for the largest administrative subdivision
  -- of a country is called the "first-level administrative division" or
  -- "first administrative level".  Next smaller is called "second-level
  -- administrative division" or "second administrative level".
  area_level smallint NOT NULL,

  -- Indicate whether this geographical area is the smallest administrative
  -- subdivision of its hierarchy.
  --
  -- This field is calculated with the following SQL statement::
  --
  --     UPDATE area
  --       SET is_leaf = is_area_leaf(area_id);
  is_leaf boolean NULL,

  -- A collection of zero or more polygon that delimit the topological
  -- space of the geographical area.  All of the polygons are within the
  -- spatial reference system.
  boundaries geometry NULL,

  -- Maximum extents of the geographical area.  The value of this field is
  -- calculated by the function ``_simplify_area_boundaries``.
  bounding_box geometry NULL,

  -- Geometric center of the area determined from the geometry of this area::
  --
  --     UPDATE area
  --       SET centroid = ST_Centroid(boundaries);
  centroid geometry NULL,

  -- Simplified boundaries of the geographical area.  To be used for
  -- display performance.   The value of this column calculated by the
  -- function ``_simplify_area_boundaries``.
  _boundaries geometry NULL,

  -- Surface in square meters of the geographical area::
  --
  --     UPDATE area
  --       SET surface = ST_Area(ST_Transform(boundaries, utmzone(centroid)))
  --
  -- The function ``get_area_surface(area_id::uuid)`` can be used to
  -- memoize and returns the surface of a specified geographical area.
  --
  -- @note: this field might not been defined for very large geographical
  --     area (cf. function ``get_area_surface``).
  surface float NULL,

  -- Time when this geographical area has been registered to the platform.
  creation_time timestamp with time zone NOT NULL DEFAULT current_timestamp,

  -- Time of the most recent modification of any attribute of this
  -- geographical area.
  update_time timestamp with time zone NOT NULL DEFAULT current_timestamp
);

/**
 * Represent a list of lowercase ASCII representation of words contained
 * in the textual information of areas.  These words can be used in a
 * query to rapidly search areas and rank them by relevance.
 *
 * Common words like articles (a, an, the) and conjunctions (and, or,
 * but) should not be treated as keywords because it is inefficient to do
 * so.
 */
CREATE TABLE area_index
(
  -- Identification of an area.
  area_id  uuid NOT NULL,

  -- Plain ASCII and lowercase representation of the name of this area.
  keyword  text NOT NULL
);


/**
 * Represent localized names of geographic areas.
 */
CREATE TABLE area_label
(
  -- Identification of the area.
  area_id uuid NOT NULL,

  -- ISO 639-3 alpha-3 code element, optionally followed by a dash
  -- character "-" and a ISO 3166-1 alpha-2 code.  For example: "eng"
  -- (which denotes a standard English), "eng-US" (which denotes an
  -- American English).
  locale varchar(6) NOT NULL DEFAULT 'eng',

  -- Human-readable name of the area written in the given locale.
  content text NOT NULL
);
