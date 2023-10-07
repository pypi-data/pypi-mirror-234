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
 * Return a string representation of a locale, i.e., a ISO 639-3
 * alpha-3 code element, optionally followed by a dash character "-"
 * and a ISO 3166-1 alpha-2 code.
 *
 *
 * @param p_language_code: a ISO 639-3 alpha-3 code.
 *
 * @param p_country_code: a ISO 3166-1 alpha-2 code.
 *
 *
 * @return: a string representing a locale.
 */
CREATE OR REPLACE FUNCTION compose_locale(
    IN p_language_code text,
    IN p_country_code text)
  RETURNS text
  IMMUTABLE
AS $$
  SELECT CASE WHEN $2 IS NULL THEN $1 ELSE $1 || '-' || $2 END;
$$ LANGUAGE SQL;

/**
 * Indicate whether the two specified locales are identic, similar, or
 * simply different.
 *
 * Two locales are identic if they correspond to the same language of
 * the same country.
 *
 * Two locales are similar if their language is identic, but their
 * country is different.
 *
 * Two locales are different when their language is different.
 *
 *
 * @param p_this_locale: a string representation of a locale, i.e., a
 *     ISO 639-3 alpha-3 code element, optionally followed by a dash
 *     character "-" and a ISO 3166-1 alpha-2 code.
 *
 * @param p_other_locale: another string representation of a locale.
 *
 *
 * @return: the value ``2`` if the two specified locales are identical;
 *     the value ``1`` if these locales are similar; and the value ``0``
  *    if these locales are different.
 */
CREATE OR REPLACE FUNCTION compare_locale(
    IN p_this_locale text,
    IN p_other_locale text)
  RETURNS smallint
  IMMUTABLE
AS $$
DECLARE
  v_this_locale_parts text[];
  v_other_locale_parts text[];
BEGIN
  IF p_this_locale = p_other_locale THEN
    RETURN 2;
  ELSE
    IF (string_to_array(p_this_locale, '-'))[1] = (string_to_array(p_other_locale, '-'))[1] THEN
      RETURN 1;
    ELSE
      RETURN 0;
    END IF;
  END IF;
END;
$$ LANGUAGE PLPGSQL;
