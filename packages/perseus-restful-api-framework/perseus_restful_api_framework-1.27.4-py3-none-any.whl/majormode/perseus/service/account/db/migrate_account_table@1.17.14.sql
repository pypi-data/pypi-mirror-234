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
  ADD COLUMN is_password_change_required boolean NOT NULL DEFAULT false,
  ADD COLUMN can_password_be_changed boolean NOT NULL DEFAULT true,
  ADD COLUMN does_password_never_expire boolean NOT NULL DEFAULT true;


CREATE TABLE account_bulk_update
(
  bulk_id uuid NOT NULL DEFAULT uuid_generate_v1(),
  account_id uuid NOT NULL,
  team_id uuid NULL,
  object_status text NOT NULL DEFAULT 'pending',
  creation_time timestamptz(3) NOT NULL DEFAULT current_timestamp,
  update_time timestamptz(3) NOT NULL DEFAULT current_timestamp
);

CREATE TABLE account_bulk_update_item
(
  bulk_id uuid NOT NULL,
  account_id uuid NULL,
  full_name text NULL,
  first_name text NULL,
  last_name text NULL,
  username text NULL,
  account_type text NOT NULL DEFAULT 'standard',
  password text NULL,
  is_password_change_required boolean NOT NULL DEFAULT false,
  can_password_be_changed boolean NOT NULL DEFAULT true,
  does_password_never_expire boolean NOT NULL DEFAULT true,
  locale varchar(6) NOT NULL DEFAULT 'eng',
  email_address text NOT NULL,
  phone_number text NULL,
  object_status text NOT NULL DEFAULT 'pending',
  creation_time timestamptz(3) NOT NULL DEFAULT current_timestamp,
  update_time timestamptz(3) NOT NULL DEFAULT current_timestamp
);

ALTER TABLE account_bulk_update
  ADD CONSTRAINT pk_account_bulk_update_id
    PRIMARY KEY (bulk_id);

ALTER TABLE account_bulk_update_item
  ADD CONSTRAINT fk_account_bulk_update_item_bulk_id
      FOREIGN KEY (bulk_id)
      REFERENCES account_bulk_update (bulk_id)
      ON DELETE CASCADE
      ON UPDATE CASCADE;

ALTER TABLE account_bulk_update_item
  ADD CONSTRAINT fk_account_bulk_update_item_account_id
      FOREIGN KEY (account_id)
      REFERENCES account (account_id)
      ON DELETE CASCADE
      ON UPDATE CASCADE;
