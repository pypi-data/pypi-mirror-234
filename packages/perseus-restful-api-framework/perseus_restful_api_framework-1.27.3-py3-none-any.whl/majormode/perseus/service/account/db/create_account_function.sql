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

/**
 * Return the name of the specified account, either the full name of
 * the user, either the user name.
 *
 * @param p_account_id: identification number of a user account.
 *
 * @return: the full name of the the user, if defined; the user name
 *     otherwise.
 */
CREATE OR REPLACE FUNCTION get_account_name(
    IN p_account_id uuid)
  RETURNS text
  STABLE
AS $$
  SELECT COALESCE(full_name, username) AS account_name
    FROM account
    WHERE account_id = $1;
$$ LANGUAGE SQL;

/**
 * Indicate whether the specified user accounts are connected to each
 * others.
 *
 * The function doesn't check that the two specified user account
 * identifications are valid, nor does it test whether one of these
 * user accounts is suspended or deleted.
 *
 * @param p_this_account_id: identification of a first user account.
 *
 * @param p_other_account_id: identification of the second user
 *     account to check the connection to the first user account.
 *
 * @return: `true` if the two specified user accounts are connected,
 *     or `false` if they are not.
 */
CREATE OR REPLACE FUNCTION is_account_connected_to(
    IN p_this_account_id uuid,
    IN p_other_account_id uuid)
  RETURNS boolean
  STABLE
AS $$
BEGIN
  IF p_this_account_id = p_other_account_id THEN
    RETURN true;
  END IF;

  RETURN false;
END
$$ LANGUAGE PLPGSQL;


/**
 * Return the value of the specified contact information of a given
 * user.
 *
 * @param p_account_id: identification of the account of a user.
 *
 * @param property_name: The name of the contact information to return
 *     the value.  This name can be one of a set of pre-defined strings
 *     such as:
 *
 *     * `EMAIL`: The e-mail address.
 *
 *     * `PHONE`: The phone number in E.164 numbering plan, an ITU-T
 *       recommendation which defines the international public
 *       telecommunication numbering plan used in the Public Switched
 *       Telephone Network (PSTN).
 *
 *     * `WEBSITE`: The Uniform Resource Locator (URL) of a Web site.
 *
 * @return: The value of the specified contact information.  If this
 *     user account has several entries for the specified contact
 *     information, the function sorts these entries by whether they
 *     are verified or not, whether they are primary or not, whether
 *     they are prior or not, and returns the entry that has the best
 *     selection.
 */
CREATE OR REPLACE FUNCTION get_account_contact(
    IN p_account_id uuid,
    IN p_property_name text,
    IN p_primary_only boolean = false,
    IN p_verified_only boolean = false)
  RETURNS text
  LANGUAGE SQL
  STABLE
AS $$
  SELECT
      property_value
    FROM
      account_contact
    WHERE
      account_id = p_account_id
      AND property_name = p_property_name
      AND (NOT p_primary_only OR is_primary)
      AND (NOT p_verified_only OR is_verified)
    ORDER BY
      is_verified DESC,  -- trick to get verified contact first
      is_primary DESC,  -- trick to get primary contact first
      creation_time ASC
    LIMIT 1;
$$;


/**
 * Invoked when a user's picture is updated either with a NULL value,
 * or with the identification of a picture.
 *
 * If the user's picture is updated with a NULL value, meaning that the
 * user doesn't have any picture representing him anymore, this function
 * proceed the following task:
 *
 * 1. Clear the attributes of the user's picture (widh, height, size, and
 *    checksum);
 * 2. Disable the last enabled picture in the user's picture history.
 *
 * If the user's picture is updated with the identification of a picture,
 * the function checks whether this picture was already uploaded by this
 * user, i.e., whether this picture is already registered in the user's
 * picture history. If not, the function simply adds it in this history,
 * otherwise the function proceeds the following tasks:
 *
 * 1. Disable the last enabled picture in the user's picture history;
 * 2. Enable this picture present in the user's picture history;
 * 3. Update the attributes of the user's picture (width, height,
 *    file_size, and file_checksum) with the attribute of this picture
 *    as stored in the user's picture history.
 */
CREATE OR REPLACE FUNCTION on_account_picture_updated()
  RETURNS trigger
AS $$
BEGIN
  -- @note: the operation `!=` doesn't work with NULL values.
  IF NEW.picture_id IS DISTINCT FROM OLD.picture_id THEN
    -- Disable the last enabled picture in the user's picture history, if any.
    UPDATE
        account_picture
      SET
         object_status = 'disabled'
      WHERE
         account_id = NEW.account_id
         AND object_status = 'enabled';

    -- Clear the attributes of the user's picture.
    IF NEW.picture_id IS NULL THEN
      UPDATE
        account
      SET
        image_file_checksum = NULL,
        image_file_size = NULL,
        image_height = NULL,
        image_width = NULL
      WHERE
        account_id = NEW.account_id;

    ELSE
      -- Enable this picture in the user's picture history if already present.
      UPDATE
          account_picture
        SET
           object_status = 'enabled'
        WHERE
           account_id = NEW.account_id  -- Prevent enabling a photo associated to another user!
           AND picture_id = NEW.picture_id;

      -- Insert this new picture to the user's picture history
      --
      -- @note: There is a possibility that this picture was actually already
      --     registered but associated with another user, in which case the
      --     previous SQL query hasn't enabled this photo; the following SQL
      --     query would raise an integrity error, and therefore the reason of
      --     the "UPSERT" option `ON CONFLICT DO NOTHING` which simply avoids
      --     inserting a row.
      IF NOT FOUND THEN
        INSERT INTO account_picture(
            picture_id,
            account_id,
            image_width,
            image_height,
            image_file_size,
            image_file_checksum,
            object_status,
            creation_time,
            update_time
          )
          VALUES (
            NEW.picture_id,
            NEW.account_id,
            NEW.image_width,
            NEW.image_height,
            NEW.image_file_size,
            NEW.image_file_checksum,
            'pending',
            current_timestamp,
            current_timestamp
          )
          ON CONFLICT DO NOTHING;

      -- The user is reusing one of his previous picture; update the
      -- attributes of the account's picture with those stored in the user'
      -- picture history.
      ELSE
        UPDATE account
          SET
            image_file_checksum = account_picture.image_file_checksum,
            image_file_size = account_picture.image_file_size,
            image_height = account_picture.image_height,
            image_width = account_picture.image_width,
            picture_time = accout_picture.creation_time
          FROM
            account_picture
          WHERE
            account_picture.picture_id = NEW.picture_id
            AND account.account_id = NEW.account_id;
      END IF;
    END IF;
  END IF;

  RETURN NEW;
END;
$$ LANGUAGE PLPGSQL;
