/**
 * Copyright (C) 2021 Majormode.  All rights reserved.
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

ALTER TABLE account
  RENAME COLUMN locale TO language;


ALTER TABLE account_contact
  RENAME COLUMN name TO property_name;

ALTER TABLE account_contact
  RENAME COLUMN value TO property_value;


ALTER TABLE account_contact_verification
  ADD COLUMN verification_code text NULL;

ALTER TABLE account_contact_verification
  ADD COLUMN expiration_time timestamptz(3) NULL;

ALTER TABLE account_contact_verification
  ADD COLUMN object_status text NOT NULL DEFAULT 'enabled';

ALTER TABLE account_contact_verification
  RENAME COLUMN locale TO language;

ALTER TABLE account_contact_verification
  RENAME COLUMN name TO property_name;

ALTER TABLE account_contact_verification
  RENAME COLUMN value TO property_value;

ALTER TABLE account_contact_verification
  RENAME COLUMN attempt_time TO last_attempt_time;


ALTER TABLE account_password_reset
  RENAME COLUMN locale TO language;


DROP INDEX idx_account_contact_unique;

CREATE UNIQUE INDEX idx_account_contact_unique
  ON account_contact (
    lower(property_value),
    property_name
  )
  WHERE
    is_verified = 'true';
