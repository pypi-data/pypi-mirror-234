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


/* @warning:
  GRANT SELECT ON public.spatial_ref_sys TO dbo;
*/


/**
 * Check whether two geographical areas are connected, meaning if there
 * is a direct parent relationship between these two areas.
 *
 *
 * @param p_this_area_id: identification of a geographical area.
 *
 * @param p_that_area_id: identification of another geographical area.
 *
 *
 * @return: ``true`` if the two geographical areas are connected,
 *     ``false`` otherwise.
 */
CREATE OR REPLACE FUNCTION are_areas_connected(
    IN p_this_area_id uuid,
    IN p_that_area_id uuid)
  RETURNS boolean
  STABLE
AS $$
DECLARE
  v_area_biggest_level int;
  v_area_id uuid;
  v_area_level int;
  v_match_area_id uuid;
  v_parent_area_id uuid;
  v_this_area_level int;
  v_that_area_level int;
BEGIN
  IF p_this_area_id = p_that_area_id THEN
    RETURN true;
  END IF;

  -- Retrieve the levels of the two geographical areas.  If they have the
  -- same level, these two geographical areas cannot be connected.
  SELECT area_level
    INTO v_this_area_level
    FROM area
    WHERE area_id = p_this_area_id;

  SELECT area_level
    INTO v_that_area_level
    FROM area
    WHERE area_id = p_that_area_id;

  IF v_this_area_level = v_that_area_level THEN
    RETURN false;
  END IF;

  -- Determine the smallest geographical area to start with.  The second
  -- geographical area needs to be a parent of the latter.
  IF v_this_area_level > v_that_area_level THEN
    v_area_id = p_this_area_id;
    v_match_area_id = p_that_area_id;
    v_area_biggest_level = v_that_area_level;
  ELSE
    v_area_id = p_that_area_id;
    v_match_area_id = p_this_area_id;
    v_area_biggest_level = v_this_area_level;
  END IF;

  -- Find all the parents of the smalled geographical area until the
  -- algorithm find the second geographical area (in which case the two
  -- geographical areas are connected) or until there is no more parent
  -- (in which case these two geographical areas are not connected).
  LOOP
    SELECT parent_area_id,
           area_level
      INTO v_parent_area_id,
           v_area_level
      FROM area
      WHERE area_id = v_area_id;

    IF NOT FOUND THEN
      RAISE EXCEPTION 'Undefined area %', v_area_id;
    END IF;

    IF v_parent_area_id IS NULL THEN
      RETURN false;
    ELSIF v_parent_area_id = v_match_area_id THEN
      RETURN true;
    ELSIF v_area_level <= v_area_biggest_level THEN
       RETURN false;
    END IF;

    v_area_id = v_parent_area_id;
  END LOOP;
END;
$$ LANGUAGE PLPGSQL;


/**
 * Return information of a list of areas that encompass the specified
 * location.
 *
 *
 * @param p_location: a point defined by at least a longitude and a
 *     latitude distance (WGS84 datum), as given for instance by the
 *     PostGIS function "ST_MakePoint".
 *
 * @param p_lowest_area_level: the level of the smallest administrative
 *     area to start with.
 *
 *     As a reminder, for clarity and convenience the standard neutral
 *     reference for the largest administrative subdivision of a country
 *     is called the "first-level administrative division" or "first
 *     administrative level". Next smaller is called "second-level
 *     administrative division" or "second administrative level", etc.
 *
 *     Note: the smallest the area, the fastest the function returns
 *     result.
 *
 * @param minimal_area_surface: minimal surface in square meter of the
 *     smallest geographical area that are returned.
 *
 * @param p_highest_area_level: the level of the largest administrative
 *     area to finish with.
 *
 * @param p_locale: the locale to return the text information of each
 *     administrative areas found.
 *
 * @param p_limit: constrain the number of geographical areas that are
 *     returned to the specified number, from the smallest to the largest.
 *     By default, the function returns all the geographical areas that
 *     have been found.
 *
 *
 * @return: a set of records of type ``area_info``.
 */
CREATE OR REPLACE FUNCTION find_areas_with_location(
    IN p_location geometry,
    IN p_lowest_area_level int = 5,
    IN p_minimal_area_surface float = 0,
    IN p_highest_area_level int = 0,
    IN p_locale text = 'eng',
    IN p_limit int = 0)
  RETURNS SETOF area_info
  STABLE
AS $$
DECLARE
  v_area_label label;
  v_area_id uuid;
  v_area_info area_info%rowtype;
  v_area_level int := p_lowest_area_level;
  v_area_type text;
  v_bounding_box geometry;
  v_centroid geometry;
  v_parent_area_id uuid;
BEGIN
  -- Find the smallest administrative division that contains the given
  -- location, starting from the specified smallest administrative level.
  LOOP
    SELECT area_id,
           parent_area_id,
           area_type,
           centroid,
           bounding_box
      INTO v_area_id,
           v_parent_area_id,
           v_area_type,
           v_centroid,
           v_bounding_box
      FROM area
      WHERE area_level = v_area_level
        AND (p_minimal_area_surface <= 0 OR get_area_surface(area_id) >= p_minimal_area_surface)
        AND ST_Contains(boundaries, p_location);

    IF FOUND THEN
      p_limit := p_limit - 1;

      v_area_info.area_id = v_area_id;
      v_area_info.parent_area_id = v_parent_area_id;
      v_area_info.centroid = v_centroid;
      v_area_info.bounding_box = v_bounding_box;
      v_area_info.area_level = v_area_level;
      v_area_info.area_type = v_area_type;
      v_area_label = get_area_label(v_area_id, p_locale);
      v_area_info.content = v_area_label.content;
      v_area_info.locale = v_area_label.locale;
      RETURN NEXT v_area_info;

      EXIT;
    END IF;

    IF v_area_level = p_highest_area_level THEN
      EXIT;
    END IF;

    v_area_level = v_area_level - 1;
  END LOOP;

  -- Find the parent administrative divisions up to the specified biggest
  -- administrative level.
  IF FOUND THEN
    WHILE v_area_info.area_level > p_highest_area_level LOOP
      IF p_limit = 0 THEN
        EXIT;
      END IF;

      p_limit := p_limit - 1;

      SELECT area_id,
             parent_area_id,
             area_level,
             area_type,
             centroid,
             bounding_box
        INTO v_area_id,
             v_parent_area_id,
             v_area_level,
             v_area_type,
             v_centroid,
             v_bounding_box
        FROM area
        WHERE area_id = v_parent_area_id;

      v_area_info.area_id = v_area_id;
      v_area_info.parent_area_id = v_parent_area_id;
      v_area_info.centroid = v_centroid;
      v_area_info.bounding_box = v_bounding_box;
      v_area_info.area_level = v_area_level;
      v_area_info.area_type = v_area_type;
      v_area_label = get_area_label(v_area_id, p_locale);
      v_area_info.content = v_area_label.content;
      v_area_info.locale = v_area_label.locale;
      RETURN NEXT v_area_info;
    END LOOP;
  END IF;

  RETURN;
END;
$$ LANGUAGE PLPGSQL;


/**
 * Return information of a list of areas that encompass the IP address.
 *
 *
 * @depends: ``find_areas_with_location``
 *
 *
 * @param p_ip_address: IP network as a string.
 *
 * @param p_lowest_area_level: the level of the smallest administrative
 *     area to start with.
 *
 *     As a reminder, for clarity and convenience the standard neutral
 *     reference for the largest administrative subdivision of a country
 *     is called the "first-level administrative division" or "first
 *     administrative level". Next smaller is called "second-level
 *     administrative division" or "second administrative level", etc.
 *
 *     Note: the smallest the area, the fastest the function returns
 *     result.
 *
 * @param p_highest_area_level: the level of the largest administrative
 *     area to finish with.
 *
 * @param p_locale: the locale to return the text information of each
 *     administrative areas found.
 *
 *
 * @return: a set of records of type ``area_info``.
 */
CREATE OR REPLACE FUNCTION find_areas_with_ip_address(
    IN p_ip_address ip4r,
    IN p_lowest_area_level int = 5,
    IN p_minimal_area_surface float = 0,
    IN p_highest_area_level int = 0,
    IN p_locale text = 'eng',
    IN p_limit int = 0)
  RETURNS SETOF area_info
  STABLE
AS $$
DECLARE
  v_area_info area_info%rowtype;
  v_location  geometry;
BEGIN
  SELECT location
    INTO v_location
    FROM geoip_block
    WHERE network >> p_ip_address;

  IF FOUND THEN
    FOR v_area_info IN
      SELECT *
        FROM find_areas_with_location(v_location,
                p_lowest_area_level:=p_lowest_area_level,
                p_minimal_area_surface:=p_minimal_area_surface,
                p_highest_area_level:=p_highest_area_level,
                p_locale:=p_locale,
                p_limit:=p_limit)
    LOOP
      RETURN NEXT v_area_info;
    END LOOP;
  END IF;

  RETURN;
END;
$$ LANGUAGE PLPGSQL;


/**
 * Return information of a list of areas that intersect the specified
 * bounding box.
 *
 *
 * @param p_bounding_box: a polygon formed by a given shell, generally
 *    defined with a closed ``LINESTRINGS`` of four points that represent
 *    the north-east corner and the south-west corners (WGS84 datum) of
 *    the rectangle area to search places in.
 *
 * @param p_lowest_area_level: the level of the smallest administrative
 *     area to start with.
 *
 *     As a reminder, for clarity and convenience the standard neutral
 *     reference for the largest administrative subdivision of a country
 *     is called the "first-level administrative division" or "first
 *     administrative level". Next smaller is called "second-level
 *     administrative division" or "second administrative level", etc.
 *
 *     Note: the smallest the area, the fastest the function returns
 *     result.
 *
 * @param p_highest_area_level: the level of the largest administrative
 *     area to finish with.
 *
 * @param p_locale: the locale to return the text information of each
 *     administrative areas found.
 *
 *
 * @return: a set of records of type ``area_info``.
 */
CREATE OR REPLACE FUNCTION find_areas_in_bounding_box(
    IN p_bounding_box geometry,
    IN p_lowest_area_level int = 5,
    IN p_highest_area_level int = 0,
    IN p_locale text = 'eng')
  RETURNS SETOF area_info
  VOLATILE
AS $$
DECLARE
  v_area record;
  v_area_info area_info%rowtype;
  v_area_label label;
  v_area_level int := p_highest_area_level;
  v_point geometry;
BEGIN
  -- Find the lowest level of geographical area that contains the specified
  -- bounding box.
  LOOP
    IF EXISTS(
      SELECT true
        FROM area
        WHERE area_level = v_area_level
          AND ST_Contains(p_bounding_box, bounding_box)
        LIMIT 1) THEN
      EXIT;
    ELSE

      -- If the specified bounding box doesn't contain any geographical area,
      -- find the geographical area of the smalled level that contains the
      -- center of the bounding box.
      IF v_area_level = p_lowest_area_level THEN
        RAISE NOTICE 'No geographical area is contained in the bounding box; seaching the best area level...';

-- @patch: because of an unsolved performance issue with the following
--   query, we need to build the geographical point apart from this
--   query otherwise PostgreSQL's execution planner doesn't use the
--   index ``idx_area_bounding_box``, probably because of the conjoint
--   usage of the aggregate function ``MAX``.
        v_point = ST_SetSRID(ST_MakePoint(
            (ST_XMin(p_bounding_box) + ST_XMax(p_bounding_box)) / 2,
            (ST_YMin(p_bounding_box) + ST_YMax(p_bounding_box)) / 2), 4326);

        SELECT LEAST(MAX(area_level), p_lowest_area_level)
          INTO v_area_level
          FROM area
          WHERE ST_Contains(bounding_box, v_point);

        EXIT;
      END IF;

      v_area_level = v_area_level + 1;
    END IF;
  END LOOP;

  RAISE NOTICE 'The most appropriate area level for this bounding box is %', v_area_level;

  -- @patch: because of an unsolved performance issue while querying
  --   geographical areas of level 0 (country), where the execution
  --   planner doesn't use the index idx_area_area_level, which
  --   provides better performance, and because PostgreSQL doesn't
  --   let choose a particular index to use, we need to split the query
  --   in two parts for the latter areas: we filter geographical area of
  --   this level, then we check for each individual area whether it
  --   instersects the specified bounding box.  For information,
  --
  --   area_level | count
  --  ------------+--------
  --            0 |    252
  --            1 |   3389
  --            2 |  41878
  --            3 | 114909
  --            4 |  49307
  --            5 |  40267
  IF v_area_level = 0 THEN
    FOR v_area IN
      SELECT area_id,
             parent_area_id,
             area_type,
             centroid,
             bounding_box
        FROM area
        WHERE area_level = v_area_level
      LOOP
        IF ST_Intersects(v_area.bounding_box, p_bounding_box) THEN
          v_area_info.area_id = v_area.area_id;
          v_area_info.parent_area_id = v_area.parent_area_id;
          v_area_info.centroid = v_area.centroid;
          v_area_info.bounding_box = v_area.bounding_box;
          v_area_info.area_level = v_area_level;
          v_area_info.area_type = v_area.area_type;

          v_area_label = get_area_label(v_area.area_id, p_locale);
          v_area_info.content = v_area_label.content;
          v_area_info.locale = v_area_label.locale;
          RETURN NEXT v_area_info;
        END IF;
      END LOOP;
  ELSE
    FOR v_area IN
      SELECT area_id,
             parent_area_id,
             area_type,
             centroid,
             bounding_box
        FROM area
        WHERE area_level = v_area_level
          AND ST_Intersects(bounding_box, p_bounding_box)
    LOOP
      v_area_info.area_id = v_area.area_id;
      v_area_info.parent_area_id = v_area.parent_area_id;
      v_area_info.centroid = v_area.centroid;
      v_area_info.bounding_box = v_area.bounding_box;
      v_area_info.area_level = v_area_level;
      v_area_info.area_type = v_area.area_type;

      v_area_label = get_area_label(v_area.area_id, p_locale);
      v_area_info.content = v_area_label.content;
      v_area_info.locale = v_area_label.locale;
      RETURN NEXT v_area_info;
    END LOOP;
  END IF;

  RETURN;
END;
$$ LANGUAGE PLPGSQL;


/**
 * Find the smallest administrative division that contains the given
 * location, starting from the specified administrative level.
 *
 *
 * @param p_location: a point defined by at least a longitude and a
 *     latitude distance (WGS84 datum), as given for instance by the
 *     PostGIS function "ST_MakePoint".
 *
 * @param p_area_level: smallest administrative level to start with.
 *
 *     As a reminder, for clarity and convenience the standard neutral
 *     reference for the largest administrative subdivision of a country
 *     is called the "first-level administrative division" or "first
 *     administrative level". Next smaller is called "second-level
 *     administrative division" or "second administrative level", etc.
 *
 *     The smallest the area, the fastest the function returns result.
 *
 *
 * @return: the smallest administrative division that contains the given
 *     location, equals or above the specified administrative level; or
 *     ``NULL`` if no administrative division contains this location.
 */
CREATE OR REPLACE FUNCTION find_smallest_area(
    IN p_location geometry,
    IN p_area_level int = 5)
  RETURNS uuid
  STABLE
AS $$
DECLARE
  v_area_id uuid = NULL;
BEGIN
  LOOP
    SELECT area_id
      INTO v_area_id
      FROM area
      WHERE area_level = p_area_level
        AND ST_Contains(_boundaries, p_location);

    IF v_area_id IS NOT NULL OR p_area_level = 0 THEN
      EXIT;
    END IF;

    p_area_level = p_area_level - 1;
  END LOOP;

  RETURN v_area_id;
END;
$$ LANGUAGE PLPGSQL;


/**
 * Return the boundaries of the specified geographical area.
 *
 *
 * @note: this function is mainly used within SQL statement that needs
 *     to check whether a given area contains a location.
 *
 *
 * @param p_area_id: identification of a given geographical area.
 *
 *
 * @return a collection of zero or more polygon that delimit the
 *     topological space of the geographical area.  All of the polygons
 *     are within the spatial reference system.
 */
CREATE OR REPLACE FUNCTION get_area_boundaries(
    IN p_area_id uuid)
  RETURNS geometry
  STABLE
AS $$
  SELECT boundaries
    FROM area
    WHERE area_id = $1;
$$ LANGUAGE SQL;


/**
 * Return the content of the specified geographical area in the requested
 * locale, or the closest locale if no content is defined for this
 * particular locale, which is, at least, English by default.
 *
 *
 * @param p_area_id: identification of a geographical area.
 *
 * @param p_locale: the locale to return the text information of the
 *     specified administrative areas found.  It corresponds to a ISO
 *     639-3 alpha-3 code (or alpha-2 code) that represents a language,
 *     possibly followed with a ISO 3166-1 alpha-2 code that represents
 *     region where this language is spoken.
 *
 *
 * @return: a record ``(content, locale)`` corresponding to the content
 *    of the geographical area in the closest locale that is requested.
 *
 *
 * @hint: this function could be used with the following SQL statement:
 *
 *     SELECT (get_area_label({{area_id}})).*;
 */
CREATE OR REPLACE FUNCTION get_area_label(
    IN p_area_id uuid,
    IN p_locale varchar(6) = 'eng')
  RETURNS label
  STABLE
AS $$
DECLARE
  v_locale text := COALESCE(p_locale, 'eng');
  v_label label;
BEGIN
  SELECT content,
         locale
    INTO v_label
    FROM area_label
    WHERE area_id = p_area_id
      AND compare_locale(locale, p_locale) > 0
    ORDER BY compare_locale(locale, p_locale) ASC
    LIMIT 1;

  IF NOT FOUND THEN
    IF v_locale = 'eng' THEN
      RAISE EXCEPTION 'Area % doesn''t have default English content defined', p_area_id;
    END IF;

    v_label = get_area_label(p_area_id, 'eng');
  END IF;

  RETURN v_label;
END;
$$ LANGUAGE PLPGSQL;


/**
 * Return the combined identification of a specified area with those of
 * its parents.
 *
 *
 * @param p_area_id: identification of the geographical area.
 *
 *
 * @return: a dot separated list of identifications starting with the
 *     specified up to its bigger enclosing parent.
 */
CREATE OR REPLACE FUNCTION get_area_extended_id(
    IN p_area_id uuid)
  RETURNS text
  STABLE
AS $$
DECLARE
  v_area_extended_id text = p_area_id::text;
  v_area_id uuid = p_area_id;
BEGIN
  LOOP
    SELECT parent_area_id
      INTO v_area_id
      FROM area
      WHERE area_id = v_area_id;

    IF v_area_id IS NULL THEN
      EXIT;
    END IF;

    v_area_extended_id = v_area_extended_id || '.' || v_area_id::text;
  END LOOP;

  RETURN v_area_extended_id;
END;
$$ LANGUAGE PLPGSQL;


/**
 * Return the smallest parent of the specified geographical area that
 * has at least the specified level.
 *
 * For example, requesting the parent of ``Bordeaux`` (level-3) that
 * is at least a ``level-2`` would return ``Gironde`` (``level-2``)
 * if defined, or ``Aquitaine`` (``level-1``) if defined, or eventually
 * ``France`` (``level-0``).
 *
 *
 * @param p_area_id: identification of a geographical area.
 *
 * @param p_highest_area_level: administrative level of the largest
 *     parent of this geographical area to return.
 *
 *     As a reminder, for clarity and convenience the standard neutral
 *     reference for the largest administrative subdivision of a country
 *     is called the "first-level administrative division" or "first
 *     administrative level". Next smaller is called "second-level
 *     administrative division" or "second administrative level", etc.
 *
 * @param p_locale: the locale to return the text information of the
 *     parent geographical area that is found.  It corresponds to a ISO
 *     639-3 alpha-3 code (or alpha-2 code) that represents a language,
 *     possibly followed with a ISO 3166-1 alpha-2 code that represents
 *     region where this language is spoken.
 *
 *
 * @return: a record of type ``area_info`` corresponding to parent
 *     geographical area found.
 */
CREATE OR REPLACE FUNCTION get_area_parent(
    IN p_area_id uuid,
    IN p_highest_area_level int = 0,
    IN p_locale text = 'eng')
  RETURNS area_info
  STABLE
AS $$
DECLARE
  v_area_id uuid := p_area_id;
  v_area_info area_info%rowtype;
  v_area_label label;
  v_area_level int;
  v_area_type text;
  v_bounding_box geometry;
  v_centroid geometry;
  v_parent_area_id uuid;
BEGIN
  -- Retrieve information about the specified area.
  SELECT parent_area_id,
         area_level
    INTO v_parent_area_id,
         v_area_level
    FROM area
    WHERE area_id = v_area_id;

  IF NOT FOUND THEN
    RAISE EXCEPTION 'Undefined area %', v_area_id;
  END IF;

  IF v_area_level < p_highest_area_level THEN
    RAISE EXCEPTION 'The level of the specified area % is higher than the required level %', p_area_id, p_highest_area_level;
  END IF;

  IF v_parent_area_id IS NULL THEN
    RAISE EXCEPTION 'The specified area %s has no parent', p_area_id;
  END IF;

  -- Find the smallest parent of the specified geographical area that
  -- has a higher administrative level that the one specified.
  v_area_id = v_parent_area_id;

  SELECT parent_area_id,
         centroid,
         bounding_box,
         area_level,
         area_type
    INTO v_parent_area_id,
         v_centroid,
         v_bounding_box,
         v_area_level,
         v_area_type
    FROM area
    WHERE area_id = v_area_id;

  IF v_area_level < p_highest_area_level THEN
    RAISE EXCEPTION 'The level of the area''s parent is higher than the required level %', p_highest_area_level;
  END IF;

  v_area_info.area_id = v_area_id;
  v_area_info.parent_area_id = v_parent_area_id;
  v_area_info.centroid = v_centroid;
  v_area_info.bounding_box = v_bounding_box;
  v_area_info.area_level = v_area_level;
  v_area_info.area_type = v_area_type;

  v_area_label = get_area_label(v_area_id, p_locale);
  v_area_info.content = v_area_label.content;
  v_area_info.locale = v_area_label.locale;

  RETURN v_area_info;
END;
$$ LANGUAGE PLPGSQL;


/**
 * Return the path of the specified geographic area, corresponding to a
 * list of parent-child areas from the root area to the specified area.
 * The name of each geographic area is provided in a locale closest to
 * the one requested.
 *
 *
 * @param p_area_id: identification of a geogprahic area.
 *
 * @param p_language_code: a ISO 639-3 alpha-3 code (or alpha-2 code)
 *     that represents a language.
 *
 * @param p_country_code: a ISO 3166-1 alpha-2 code that represents
 *     region where this language is spoken.
 *
 *
 * @return: the path of this geographical area from the root area it
 *     belongs to, each parent-child areas separated by the character
 *     ".".
 */
CREATE OR REPLACE FUNCTION get_area_path(
    IN p_area_id uuid,
    IN p_locale varchar(6) = 'eng')
  RETURNS text
  STABLE
AS $$
DECLARE
  v_area_content text;
  v_area_path text = '';
  v_area_id uuid = p_area_id;
BEGIN
  WHILE v_area_id IS NOT NULL LOOP
    SELECT parent_area_id,
           (get_area_label(v_area_id, p_locale := p_locale)).content
      INTO v_area_id,
           v_area_content
      FROM area
      WHERE area_id = v_area_id;

    v_area_path = '.' || v_area_content || v_area_path;
  END LOOP;

  -- Remove the leading "." character.
  RETURN substring(v_area_path from 2 for length(v_area_path) - 1);
END;
$$ LANGUAGE PLPGSQL;


/**
 * Indicate whether the specified geographical area has not children,
 * meaning it is the lowest administrative subdivision.
 *
 *
 * @param p_area_id: identification of the geographical area.
 *
 *
 * @return: ``true`` if this geographical area has not children,
 *   ``false`` otherwise.
 */
CREATE OR REPLACE FUNCTION is_area_leaf(
    IN p_area_id uuid)
  RETURNS boolean
  IMMUTABLE
AS $$
   SELECT NOT EXISTS(
      SELECT true
        FROM area
        WHERE parent_area_id = $1)
$$ LANGUAGE SQL;


/**
 * Return the surface in square meters of the specified geographical area.
 *
 *
 * @param p_area_id: identification of a geographical area.
 *
 * @param p_force: indicate whether the function MUST recalculate the
 *    surface of the geographical area, even if this surface has been
 *    already stored.
 *
 *
 * @return: surface in square meters of the specified geographical area.
 *
 *
 * @note: the function uses a memoisation technique for better
 *     performance, storing the result of the surface calculation and
 *     returning the cached result if the argument ``p_force`` is
 *     ``false``.
 *
 * @note: this function DOES NOT work for very large geographical areas
 *     such as countries, as the projection method used is based on the
 *     centroid of this geographical area, which may not correspond to
 *     every region of this area.
 */
CREATE OR REPLACE FUNCTION get_area_surface(
    IN p_area_id uuid,
    IN p_force boolean = false)
  RETURNS float
  VOLATILE
AS $$
DECLARE
  v_surface float;
BEGIN
  IF NOT p_force THEN
    SELECT surface
      INTO v_surface
      FROM area
      WHERE area_id = p_area_id;
  END IF;

  -- @patch: The code with "utmzone" raises an error:
  --     transform: couldn't project point (-179.094 76.1646 0): latitude
  --     or longitude exceeded limits (-14)
  IF v_surface IS NULL THEN
    UPDATE area
      SET surface = ST_Area(ST_Transform(boundaries, utmzone(centroid)))
      WHERE area_id = p_area_id
      RETURNING surface
        INTO v_surface;
  END IF;

  RETURN v_surface;
END;
$$ LANGUAGE PLPGSQL;


/**
 * Calculate the simplified boundaries of each geographical area.
 *
 * This function updates the column ``_boundaries`` of the table
 * ``area``.
 *
 * You need to execute this function as follows:
 *
 *   DROP INDEX idx_area__boundaries;
 *
 *   SELECT _simplify_area_boundaries();
 *
 *   ALTER TABLE area
 *     ALTER COLUMN _boundaries SET NOT NULL;
 *
 *   CREATE INDEX idx_area__boundaries
 *     ON area USING GIST (_boundaries);
 *
 *
 * @depends: PostGIS 2.0 (Box2D instead of ST_Box2D)
 */
CREATE OR REPLACE FUNCTION _simplify_area_boundaries()
  RETURNS void
AS $$
DECLARE
  v_area_id uuid;
  v_area_level smallint;
  v_label label;
  v_ratio float;
BEGIN
  FOR v_area_id, v_area_level IN
    SELECT area_id, area_level
      FROM area
  LOOP
    UPDATE area
      SET _boundaries = ST_Simplify(boundaries,
               GREATEST(ST_XMax(Box2D(boundaries)) - ST_XMin(Box2D(boundaries)),
                        ST_YMax(Box2D(boundaries)) - ST_YMin(Box2D(boundaries))) / 2000),
          bounding_box = ST_SetSRID(Box2D(boundaries), 4326),
          centroid = ST_Centroid(boundaries)
      WHERE area_id = v_area_id
      RETURNING 100.0 - (ST_NPoints(_boundaries) * 100.0 / ST_NPoints(boundaries))
        INTO v_ratio;

    IF v_ratio > 0.0 THEN
      v_label = get_area_label(v_area_id, p_locale:='eng');
      RAISE NOTICE 'Simplify area % [%] => % %%', v_label.content, v_area_level, v_ratio;
    END IF;
  END LOOP;
END;
$$ LANGUAGE PLPGSQL;
