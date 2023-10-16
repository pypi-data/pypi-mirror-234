/**
 * Copyright (C) 2015 Majormode.  All rights reserved.
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
 * Return the value of the specified contact information of a given
 * user.
 *
 * @param p_team_id: identification of a team.
 *
 * @param property_name: name of the contact information to return the
 *     value.  This name can be one of a set of pre-defined strings
 *     such as:
 *
 *     * `EMAIL`: e-mail address.
 *
 *     * `PHONE`: phone number in E.164 numbering plan, an ITU-T
 *       recommendation which defines the international public
 *       telecommunication numbering plan used in the Public Switched
 *       Telephone Network (PSTN).
 *
 *     * `WEBSITE`: Uniform Resource Locator (URL) of a Web site.
 *
 * @return: the value of the specified contact information.  If this
 *     team has several entries for the specified contact information,
 *     the function sorts these entries by whether they are verified
 *     or not, whether they are primary or not, whether they are prior
 *     or not, and returns the entry that has the best selection.
 */
CREATE OR REPLACE FUNCTION get_team_contact_value(
    IN p_team_id uuid,
    IN p_property_name text,
    IN p_primary_only boolean = false,
    IN p_verified_only boolean = false)
  RETURNS text
  STABLE
AS $$
DECLARE
  v_property_value text = NULL;
BEGIN
  SELECT property_value
    INTO v_property_value
    FROM team_contact
    WHERE team_id = p_team_id
      AND property_name = p_property_name
      AND (NOT p_primary_only OR is_primary)
      AND (NOT p_is_verified OR is_verified)
    ORDER BY is_verified DESC, -- trick to get verified contact first
             is_primary DESC, -- trick to get primary contact first
             creation_time ASC
    LIMIT 1;

  RETURN v_property_value;
END
$$ LANGUAGE PLPGSQL;


/**
 * Indicate whether the specified user is an administrator of a given
 * team.
 *
 *
 * @param p_account_id: identification of an account of a user.
 *
 * @param p_team_id: identification of a team.
 *
 *
 * @return: `true` if the specified user is an administrator of this
 *     team; `false` otherwise.
 */
CREATE OR REPLACE FUNCTION team_is_administrator(
    IN p_account_id uuid,
    IN p_team_id uuid)
  RETURNS boolean
  STABLE
AS $$
  SELECT COUNT(*) > 0
    FROM team_member
    WHERE team_id = $2
      AND account_id = $1
      AND object_status = +object-status-enabled+
      AND role = 'administrator';
$$ LANGUAGE SQL;


/**
 * Indicate whether the specified user is a member of a given team.
 *
 *
 * @param p_account_id: identification of an account of a user.
 *
 * @param p_team_id: identification of a team.
 *
 *
 * @return: `true` if the specified user is a member of the given
 *     team; `false` otherwise.
 */
CREATE OR REPLACE FUNCTION team_is_member(
    IN p_account_id uuid,
    IN p_team_id uuid)
  RETURNS boolean
  STABLE
AS $$
  SELECT COUNT(*) > 0
    FROM team_member
    WHERE team_id = $2
      AND account_id = $1
      AND object_status = +object-status-enabled+;
$$ LANGUAGE SQL;
