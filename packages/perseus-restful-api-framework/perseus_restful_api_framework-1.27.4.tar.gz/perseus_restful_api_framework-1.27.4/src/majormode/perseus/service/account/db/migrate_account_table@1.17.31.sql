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

DELETE FROM
    account_index
  WHERE
    NOT EXISTS (
      SELECT
          true
        FROM
          account
        WHERE
          account.account_id = account_index.account_id
    );

ALTER TABLE account_index
  ADD CONSTRAINT fk_account_index_account_id
      FOREIGN KEY (account_id)
      REFERENCES account (account_id)
      ON DELETE CASCADE
      ON UPDATE CASCADE;

