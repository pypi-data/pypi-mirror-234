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
 * Represent user sessions.
 */
CREATE TABLE account_session
(
  -- The identification of the session of a user account.
  session_id uuid NOT NULL DEFAULT uuid_generate_v4(),

  -- The identification of a user account.
  account_id uuid NOT NULL,

  -- The identification of the client application that the user is
  -- connected to.
  app_id uuid NOT NULL,

  -- The current status of this user session.
  object_status text NOT NULL DEFAULT +object-status-enabled+,

  -- The time when this session started.
  creation_time timestamptz(3) NOT NULL DEFAULT current_timestamp,

  -- The time of the most recent modification of one or more attributes
  -- of this user session.
  update_time timestamptz(3) NOT NULL DEFAULT current_timestamp,

  -- The time when the use session expires.
  expiration_time timestamptz(3) NOT NULL
);
