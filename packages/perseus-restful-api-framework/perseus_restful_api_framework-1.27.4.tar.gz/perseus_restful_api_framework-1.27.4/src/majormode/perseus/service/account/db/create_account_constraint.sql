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

ALTER TABLE account
  ADD CONSTRAINT pk_account_id
      PRIMARY KEY (account_id);


ALTER TABLE account_contact
  ADD CONSTRAINT fk_account_contact_account_id
      FOREIGN KEY (account_id)
      REFERENCES account (account_id)
      ON DELETE CASCADE
      ON UPDATE CASCADE;


ALTER TABLE account_contact_verification
  ADD CONSTRAINT pk_account_contact_verification_request_id
      PRIMARY KEY (request_id);

ALTER TABLE account_contact_verification
  ADD CONSTRAINT fk_account_contact_verification_account_id
      FOREIGN KEY (account_id)
      REFERENCES account (account_id)
      ON DELETE CASCADE
      ON UPDATE CASCADE;

ALTER TABLE account_contact_verification
  ADD CONSTRAINT fk_account_contact_verification_application_id
      FOREIGN KEY (app_id)
      REFERENCES application (app_id)
      ON DELETE CASCADE
      ON UPDATE CASCADE;


ALTER TABLE account_index
  ADD CONSTRAINT fk_account_index_account_id
      FOREIGN KEY (account_id)
      REFERENCES account (account_id)
      ON DELETE CASCADE
      ON UPDATE CASCADE;


ALTER TABLE account_password_reset
  ADD CONSTRAINT pk_request_id
    PRIMARY KEY (request_id);

ALTER TABLE account_password_reset
  ADD CONSTRAINT fk_account_password_reset_account_id
      FOREIGN KEY (account_id)
      REFERENCES account (account_id)
      ON DELETE CASCADE
      ON UPDATE CASCADE;

ALTER TABLE account_password_reset
  ADD CONSTRAINT fk_account_password_reset_application_id
      FOREIGN KEY (app_id)
      REFERENCES application (app_id)
      ON DELETE CASCADE
      ON UPDATE CASCADE;


ALTER TABLE account_picture
  ADD CONSTRAINT pk_account_picture_id
    PRIMARY KEY (picture_id);

-- @note: We CANNOT add a foreign key constraint on the column `account_id`
--     of the table `account_picture` because the account could have been
--     inserted in an inheriting table.
--
--ALTER TABLE account_picture
--  ADD CONSTRAINT fk_account_picture_account_id
--      FOREIGN KEY (account_id)
--      REFERENCES account (account_id)
--      ON DELETE SET NULL  -- @note: We need to delete the corresponding file before deleting this record.
--      ON UPDATE CASCADE;

-- @note: We CANNOT add a foreign key constraint on the column
--     `submitter_account_id` of the table `account_picture` because the
--     account could have been inserted in an inheriting table.
--
--ALTER TABLE account_picture
--  ADD CONSTRAINT fk_account_picture_submitter_account_id
--      FOREIGN KEY (submitter_account_id)
--      REFERENCES account (account_id)
--      ON DELETE SET NULL
--      ON UPDATE CASCADE;

ALTER TABLE account_picture
  ADD CONSTRAINT fk_account_picture_team_id
      FOREIGN KEY (team_id)
      REFERENCES team (team_id)
      ON DELETE SET NULL
      ON UPDATE CASCADE;


ALTER TABLE account_preference
  ADD CONSTRAINT fk_account_preference_account_id
      FOREIGN KEY (account_id)
      REFERENCES account (account_id)
      ON DELETE CASCADE
      ON UPDATE CASCADE;

ALTER TABLE account_preference
  ADD CONSTRAINT fk_account_preference_app_id
      FOREIGN KEY (app_id)
      REFERENCES application (app_id)
      ON DELETE CASCADE
      ON UPDATE CASCADE;

ALTER TABLE account_preference
  ADD CONSTRAINT cst_account_preference_unique
    UNIQUE (
      account_id,
      property_name,
      app_id
    );
