/**
 * Copyright (C) 2010 Majormode.  All rights reserved.
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
 *
 * @version $Revision$
 */

ALTER TABLE team
  ADD CONSTRAINT pk_team_id
      PRIMARY KEY (team_id);

ALTER TABLE team
  ADD CONSTRAINT fk_team_account_id
      FOREIGN KEY (account_id)
      REFERENCES account (account_id)
      ON DELETE CASCADE
      ON UPDATE CASCADE;


ALTER TABLE team_contact
  ADD CONSTRAINT fk_team_contact_team_id
      FOREIGN KEY (team_id)
      REFERENCES team (team_id)
      ON DELETE CASCADE
      ON UPDATE CASCADE;


ALTER TABLE team_member
  ADD CONSTRAINT cst_team_member_unique
      UNIQUE (team_id, account_id);

ALTER TABLE team_member
  ADD CONSTRAINT fk_team_member_account_id
      FOREIGN KEY (account_id)
      REFERENCES account (account_id)
      ON DELETE CASCADE
      ON UPDATE CASCADE;

ALTER TABLE team_member
  ADD CONSTRAINT fk_team_member_team_id
      FOREIGN KEY (team_id)
      REFERENCES team (team_id)
      ON DELETE CASCADE
      ON UPDATE CASCADE;


ALTER TABLE team_membership_invitation
  ADD CONSTRAINT pk_team_membership_invitation_id
      PRIMARY KEY (invitation_id);

ALTER TABLE team_membership_invitation
  ADD CONSTRAINT cst_team_membership_invitation_unique
      UNIQUE (team_id, account_id);

ALTER TABLE team_membership_invitation
  ADD CONSTRAINT fk_team_member_team_id
      FOREIGN KEY (team_id)
      REFERENCES team (team_id)
      ON DELETE CASCADE
      ON UPDATE CASCADE;


ALTER TABLE team_membership_request
  ADD CONSTRAINT cst_team_membership_request_unique
      UNIQUE (team_id, account_id);

ALTER TABLE team_membership_request
  ADD CONSTRAINT fk_team_id
      FOREIGN KEY (team_id)
      REFERENCES team (team_id)
      ON DELETE CASCADE
      ON UPDATE CASCADE;

ALTER TABLE team_membership_request
  ADD CONSTRAINT fk_account_id
      FOREIGN KEY (account_id)
      REFERENCES account (account_id)
      ON DELETE CASCADE
      ON UPDATE CASCADE;
