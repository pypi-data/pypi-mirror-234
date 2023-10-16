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

ALTER TABLE notification
  ADD CONSTRAINT pk_notification_id
      PRIMARY KEY (notification_id);

/**
 * Ensure that a device can only register once to the push notification
 * service for a given device platform (Android, iOS, Windows mobile),
 * for a specific mobile application, and on behalf of a given user.
 */
ALTER TABLE notification_device
  ADD CONSTRAINT cst_notification_device_unique
      UNIQUE (
        device_id,
        device_platform,
        app_id,
        account_id
      );
