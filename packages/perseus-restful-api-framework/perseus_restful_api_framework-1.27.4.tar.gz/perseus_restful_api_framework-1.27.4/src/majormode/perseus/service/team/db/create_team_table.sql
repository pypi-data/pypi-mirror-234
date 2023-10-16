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
 */

/**
 * Represent a group of people having a common purpose or interest,
 * such as, for instance, an organization, an association, a guild,
 * an institute, a squad. etc.
 */
CREATE TABLE team (
  -- Identification of the team.
  team_id uuid NOT NULL DEFAULT uuid_generate_v4(),

  -- The name given to the team.
  name text NOT NULL,

  -- A short textual description of the team written in whatever locale.
  description text NULL,

  -- Identification of the picture that visually represents the team
  -- (logo).
  picture_id uuid NULL,

  -- Number of pixel columns of the team's original logo image.
  image_width smallint NULL,

  -- Number of pixel rows of the team's original logo image.
  image_height smallint NULL,

  -- Size in bytes of the team's original logo image file.
  image_file_size int NULL,

  -- Message digest of the the binary data of the team's original logo
  -- image file.
  image_file_checksum text NULL,

  -- Identification of the account of the user who registered this team.
  -- This user is the agent (super administrator) of this team.
  account_id uuid NOT NULL,

-- Uniform Resource Locator (URL) that is provided as a link in the
-- email the online service sends to a user who is invited to join the
-- team.  When the user clicks on the link embedded in the email, the
-- email reader application issues a HTTP GET request to this URL.
  invitation_url text NULL,

  -- Template of the letter to send by email to a user who is invited to
  -- join the team.  If no specific template is defined for this team, the
  -- online service provides a default template.
  invitation_email text NULL,

  -- Minimum number of administrators of the team, expressed in percentage
  -- of the total number of administrators, that must accept a user to be
  -- granted the role of administrator so that decisions can be made
  -- properly.  If the value is `0.0`, only the agent of the team can grant
  -- the role of administrator to a member.
  administrator_acceptance_quorum float NULL DEFAULT 0.0,

  -- Minimum number of administrators of the team, expressed in percentage
  -- of the total number of administrators, that must revoke a member from
  -- the team so that decisions can be made properly.  If the value is `0.0`,
  -- only the agent of the team can revoke the role of administrator from a
  -- member.
  administrator_revocation_quorum float NULL DEFAULT 0.0,

  -- Current status of this team.
  object_status text NOT NULL DEFAULT 'enabled',

  -- Time when the team has been registered.
  creation_time timestamptz(3) NOT NULL DEFAULT current_timestamp,

  -- Time of the most recent modification of some information of the team.
  update_time timestamptz(3) NOT NULL DEFAULT current_timestamp
);

/**
 * Represent the contact information of a team
 *
 * Contact information corresponds to a list of properties, such as
 * e-mail addresses, phone numbers, websites.
 */
CREATE TABLE team_contact
(
  -- Identification of a team.
  team_id uuid NOT NULL,

  -- Name of the contact information property, which can be one of a set
  -- of pre-defined strings such as:
  --
  -- * `EMAIL`: e-mail address.
  --
  -- * `PHONE`: phone number in E.164 numbering plan, an ITU-T recommendation
  --   which defines the international public telecommunication numbering
  --   plan used in the Public Switched Telephone Network (PSTN).
  --
  -- * `WEBSITE`: Uniform Resource Locator (URL) of a Web site.
  property_name text NOT NULL,

  -- A property of a contact information can be further qualified with a
  -- property parameter expression.  The property parameter expressions are
  -- specified as either a `name=value` or a value string.
  property_parameters text NULL,

  -- Value of the contact information property representing by a string,
  -- such as ``+84.0812170781``, the formatted value for an international
  -- telephone number.  There can be only a unique property with a given
  -- name and a given value.
  property_value text NOT NULL,

  -- Indicate whether this contact information is the primary one for the
  -- given property.
  is_primary boolean NOT NULL DEFAULT false,

  -- Indicate the visibility of this contact information to other users.
  visibility text NOT NULL DEFAULT +visibility-public+,

  -- Indicate whether this contact information has been verified, whether
  -- it has been grabbed from a trusted Social Networking Service (SNS), or
  -- whether through a challenge/response process.
  is_verified boolean NOT NULL DEFAULT false,

  -- Current status of this contact information property.
  object_status text NOT NULL DEFAULT +object-status-enabled+,

  -- Time when this contact information property has been added.
  creation_time timestamptz(3) NOT NULL DEFAULT current_timestamp,

  -- Time of the most recent modification of this contact information
  -- property.
  update_time timestamptz(3) NOT NULL DEFAULT current_timestamp
);

/**
 * Represent the members of a team
 */
CREATE TABLE team_member
(
  -- Identification of an team.
  team_id uuid NOT NULL,

  -- Identification of the account of this user member of the team.
  account_id uuid NOT NULL,

  -- Complete personal name of this member, as possibly overridden (from
  -- `account.full_name`) by an administrator of the team.
  full_name text NULL,

  -- Role of this user within the team.
  role text NOT NULL,

  -- Current status of the member.
  object_status text NOT NULL DEFAULT 'enabled',

  -- Time when this user has been added as a member of the team.
  creation_time timestamptz(3) NOT NULL DEFAULT current_timestamp,

  -- Time of the most recent modification of the membership of this user.
  update_time timestamptz(3) NOT NULL DEFAULT current_timestamp
);

/**
 * Represent invitations sent to users to join a team
 *
 * Only an administrator of a team can invite a user to join this team.
 *
 * By convention, when an administrator cancels a membership invitation
 * to a user, this invitation is hard-deleted, while when a user declines
 * the membership invitation that is sent to him, this invitation is soft-
 * deleted (i.e., the invite's object status is set to `deleted`).
 */
CREATE TABLE team_membership_invitation
(
  -- Identification of the membership invitation that has been sent to a
  -- user on behalf of an administrator of the team.
  invitation_id uuid NOT NULL DEFAULT uuid_generate_v1(),

  -- "Number used once", a pseudo-random number issued when generating the
  -- invitation key to ensure that this key cannot be reused in replay
  -- attacks.
  invitation_nonce text NOT NULL,

  -- Identification of the team that the user is invited to join.
  team_id uuid NOT NULL,

  -- Identification of the account of the user who is invited to join the
  -- team.
  account_id uuid NOT NULL,

  -- Role that is given to this user within the team.
  role text NOT NULL,

  -- Identification of the account of the administrator who invited the
  -- other user to be member of the team.
  originator_id uuid NOT NULL,

  -- Number of times the platform notified the user from the membership
  -- invitation.  After a certain number of time, the membership invitation
  -- may may be canceled.
  attempt_count smallint NOT NULL DEFAULT 0,

  -- Current status of this invitation.
  object_status text NOT NULL DEFAULT +object-status-enabled+,

  -- Time when this invitation has been requested.
  creation_time timestamptz(3) NOT NULL DEFAULT current_timestamp,

  -- Time of the most recent modification of this invitation.
  update_time timestamptz(3) NOT NULL DEFAULT current_timestamp
);

/**
 * Represent request of user who would like to join a team
 */
CREATE TABLE team_membership_request
(
  -- Identification of the team that a user requests to join.
  team_id uuid NOT NULL,

  -- Identification of the account of a user who requests to join a team.
  account_id uuid NOT NULL,

  -- Current status of this request.
  object_status text NOT NULL DEFAULT +object-status-enabled+,

  -- Time when the user requested to join the team.
  creation_time timestamptz(3) NOT NULL DEFAULT current_timestamp,

  -- Time of the most recent modification of this request.
  update_time timestamptz(3) NOT NULL DEFAULT current_timestamp
);
