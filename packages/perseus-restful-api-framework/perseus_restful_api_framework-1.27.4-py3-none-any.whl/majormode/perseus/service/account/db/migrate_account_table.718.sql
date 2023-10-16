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
  ADD COLUMN _object_status text NULL;

UPDATE account
  SET _object_status = CASE
            WHEN object_status = 0 THEN 'enabled'
            WHEN object_status = 1 THEN 'deleted'
            WHEN object_status = 2 THEN 'disabled'
            WHEN object_status = 3 THEN 'pending'
          END;

ALTER TABLE account
  DROP COLUMN object_status;

ALTER TABLE account
  RENAME COLUMN _object_status TO object_status;

ALTER TABLE account
  ALTER COLUMN object_status SET NOT NULL;


ALTER TABLE account_contact
  ADD COLUMN _object_status text NULL;

UPDATE account_contact
  SET _object_status = CASE
            WHEN object_status = 0 THEN 'enabled'
            WHEN object_status = 1 THEN 'deleted'
            WHEN object_status = 2 THEN 'disabled'
            WHEN object_status = 3 THEN 'pending'
          END;

ALTER TABLE account_contact
  DROP COLUMN object_status;

ALTER TABLE account_contact
  RENAME COLUMN _object_status TO object_status;

ALTER TABLE account_contact
  ALTER COLUMN object_status SET NOT NULL;

ALTER TABLE account_contact
  ADD COLUMN visibility text NOT NULL DEFAULT 'organization';


ALTER TABLE account_password_reset
  DROP COLUMN object_status;

CREATE TABLE account_index
(
  account_id uuid NOT NULL,
  keyword    text NOT NULL
);
