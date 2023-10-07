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

CREATE UNIQUE INDEX cst_account_unique_username
  ON account (lower(username));


CREATE UNIQUE INDEX idx_account_contact_unique
  ON account_contact (
    lower(property_value),
    property_name
  )
  WHERE
    is_verified = true;


CREATE UNIQUE INDEX cst_account_contact_verification_unique
  ON account_contact_verification (
    account_id,
    property_name,
    lower(property_value)
  );


CREATE UNIQUE INDEX idx_account_index_keyword
  ON account_index (keyword, account_id);
