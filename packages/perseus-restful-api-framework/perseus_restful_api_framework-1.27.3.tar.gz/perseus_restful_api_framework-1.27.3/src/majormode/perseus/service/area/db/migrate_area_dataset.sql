/**
 * Copyright (C) 2019 Majormode.  All rights reserved.
 *
 * This software is the confidential and proprietary information of
 * Majormode or one of its subsidiaries.  You shall not disclose this
 * confidential information and shall use it only in accordance with the
 * terms of the license agreement or other applicable agreement you
 * entered into with Majormode.
 *
 * MAJORMODE MAKES NO REPRESENTATIONS OR WARRANTIES ABOUT THE SUITABILITY
 * OF THE SOFTWARE, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
 * TO THE IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
 * PURPOSE, OR NON-INFRINGEMENT.  MAJORMODE SHALL NOT BE LIABLE FOR ANY
 * LOSSES OR DAMAGES SUFFERED BY LICENSEE AS A RESULT OF USING, MODIFYING
 * OR DISTRIBUTING THIS SOFTWARE OR ITS DERIVATIVES.
 */

CREATE OR REPLACE FUNCTION _migrate_area_surface(
    IN p_force boolean = false)
  RETURNS void
AS $$
DECLARE
  v_area_id uuid;
  v_label label;
  v_surface float;
BEGIN
  FOR v_area_id, v_surface IN
    SELECT area_id, surface
      FROM area
  LOOP
    IF p_force OR v_surface IS NULL THEN
      v_label = get_area_label(v_area_id, p_locale:='eng');

      BEGIN
        UPDATE area
          SET surface = ST_Area(ST_Transform(boundaries, utmzone(centroid)))
          WHERE area_id = v_area_id
          RETURNING surface into v_surface;

        RAISE NOTICE 'Surface of area % => %', v_label.content, v_surface;
      EXCEPTION WHEN OTHERS THEN
        RAISE NOTICE 'Error while calculating surface of area %', v_label.content;
      END;
    END IF;
  END LOOP;
END;
$$ LANGUAGE PLPGSQL;
