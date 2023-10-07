/**
 * -*- coding: utf-8 -*-
 *
 * Copyright (C) 2010 Majormode.  All rights reserved.
 *
 * This software is the confidential and proprietary information of
 * Majormode or one of its subsidiaries.  You shall not disclose this
 * confidential information and shall use it only in accordance with the
 * terms of the license agreement or other applicable agreement you
 * entered into with Majormode.
 *
 * MAJORMODE MAKES NO REPRESENTATIONS OR WARRANTIES ABOUT THE SUITABILITY
 * OF THE SOFTWARE, EITHER EXPRESS OR IMPLIED, INCLUDING  BUT NOT LIMITED
 * TO THE IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
 * PURPOSE, OR NON-INFRINGEMENT.  MAJORMODE SHALL NOT BE LIABLE FOR ANY
 * LOSSES OR DAMAGES SUFFERED BY LICENSEE AS A RESULT OF USING, MODIFYING
 * OR DISTRIBUTING THIS SOFTWARE OR ITS DERIVATIVES.
 *
 * @version $Revision$
 */


/**
 * Return the Universal Transverse Mercator (UTM) zone corresponding to
 * the specified location.
 *
 *
 * @param p_location: a location on the surface of the Earth
 *
 *
 * @return: the Universal Transverse Mercator (UTM) zone corresponding to
 *     the specified location.
 */
CREATE OR REPLACE FUNCTION utmzone(
    IN p_location geometry)
  RETURNS int
  IMMUTABLE
AS $$
DECLARE
  v_location geometry;
  v_zone int;
  v_pref int;
BEGIN
  v_location := ST_Transform(p_location, 4326);

  IF ST_Y(v_location)>0 THEN
    v_pref := 32600;
  ELSE
    v_pref := 32700;
  END IF;

  v_zone := floor((ST_X(v_location) + 180) / 6) + 1;

  RETURN v_zone + v_pref;
END;
$$ LANGUAGE PLPGSQL;
