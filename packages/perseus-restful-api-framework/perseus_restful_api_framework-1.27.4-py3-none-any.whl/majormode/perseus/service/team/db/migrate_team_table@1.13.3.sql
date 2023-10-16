/**
 * Copyright (C) 2021 Majormode.  All rights reserved.
 *
 * This software is the confidential and proprietary information of
 * Majormode or one of its subsidiaries.  You shall not disclose this
 * confidential information and shall use it only in accordance with
 * the terms of the license agreement or other applicable agreement
 * you entered into with Majormode.
 *
 * MAJORMODE MAKES NO REPRESENTATIONS OR WARRANTIES ABOUT THE
 * SUITABILITY OF THE SOFTWARE, EITHER EXPRESS OR IMPLIED, INCLUDING
 * BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE, OR NON-INFRINGEMENT.  MAJORMODE
 * SHALL NOT BE LIABLE FOR ANY LOSSES OR DAMAGES SUFFERED BY LICENSEE
 * AS A RESULT OF USING, MODIFYING OR DISTRIBUTING THIS SOFTWARE OR
 * ITS DERIVATIVES.
 */

ALTER TABLE team
  ALTER COLUMN administrator_acceptance_quorum DROP NOT NULL,
  ALTER COLUMN administrator_revocation_quorum DROP NOT NULL;

ALTER TABLE team_contact
  ADD COLUMN visibility text NOT NULL DEFAULT 'public';

DELETE FROM team_contact
  WHERE team_id NOT IN (
    SELECT
        team_id
      FROM
        team
  );

ALTER TABLE team_contact
  ADD CONSTRAINT fk_team_contact_team_id
      FOREIGN KEY (team_id)
      REFERENCES team (team_id)
      ON DELETE CASCADE
      ON UPDATE CASCADE;

CREATE UNIQUE INDEX idx_team_contact
  ON team_contact (
    lower(property_value),
    property_name
  );

ALTER TABLE team_member
  ADD COLUMN full_name text NULL;

ALTER TABLE team_invitation
  ADD COLUMN role text NOT NULL,
  DROP COLUMN is_administrator;

ALTER TABLE team_join_request
  ADD COLUMN object_status text NOT NULL DEFAULT 'enabled',
  ADD COLUMN update_time timestamptz(3) NOT NULL DEFAULT current_timestamp;

ALTER TABLE team_invitation
  RENAME COLUMN invite_id TO invitation_id;

DELETE FROM team_invitation;

ALTER TABLE team_invitation
  ADD COLUMN _invitation_id uuid NOT NULL DEFAULT uuid_generate_v1();

ALTER TABLE team_invitation
  DROP COLUMN invitation_id;

ALTER TABLE team_invitation
  RENAME COLUMN _invitation_id TO invitation_id;

DROP SEQUENCE seq_team_invitation_id;

ALTER TABLE team_invitation
  RENAME COLUMN invite_nonce TO invitation_nonce;

ALTER TABLE team_invitation
  RENAME TO team_membership_invitation;

ALTER TABLE team_join_request
  RENAME TO team_membership_request;

ALTER TABLE team
  ADD COLUMN image_width smallint NULL,
  ADD COLUMN image_height smallint NULL,
  ADD COLUMN image_file_size int NULL,
  ADD COLUMN image_file_checksum text NULL;
