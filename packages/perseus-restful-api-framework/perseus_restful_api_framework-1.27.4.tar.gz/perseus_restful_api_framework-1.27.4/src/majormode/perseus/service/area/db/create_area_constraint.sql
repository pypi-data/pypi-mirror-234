/**
 * -*- coding: utf-8 -*-
 *
 * Copyright (C) 2010 Majormode.  All rights reserved.
 *
 * This software is the confidential and proprietary information of
 * Majormode or one of its subsidiaries.  You shall not disclose this
 * confidential information and shall use it only in accordance with
 * the terms of the license agreement or other applicable agreement you
 * entered into with Majormode.
 *
 * MAJORMODE MAKES NO REPRESENTATIONS OR WARRANTIES ABOUT THE
 * SUITABILITY OF THE SOFTWARE, EITHER EXPRESS OR IMPLIED, INCLUDING
 * BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE, OR NON-INFRINGEMENT.  MAJORMODE
 * SHALL NOT BE LIABLE FOR ANY LOSSES OR DAMAGES SUFFERED BY LICENSEE
 * AS A RESULT OF USING, MODIFYING OR DISTRIBUTING THIS SOFTWARE OR ITS
 * DERIVATIVES.
 *
 * @version $Revision$
 */

ALTER TABLE area
  ADD CONSTRAINT pk_area_id
      PRIMARY KEY (area_id);

ALTER TABLE area
  ADD CONSTRAINT cst_unique_area_code
      UNIQUE (area_code);

ALTER TABLE area
  ADD CONSTRAINT fk_area_parent_area_id
      FOREIGN KEY (parent_area_id)
      REFERENCES area (area_id)
      ON DELETE CASCADE
      ON UPDATE CASCADE;


ALTER TABLE area_label
  ADD CONSTRAINT fk_area_label_area_id
      FOREIGN KEY (area_id)
      REFERENCES area (area_id)
      ON DELETE CASCADE
      ON UPDATE CASCADE;


ALTER TABLE area_index
  ADD CONSTRAINT fk_area_index_area_id
      FOREIGN KEY (area_id)
      REFERENCES area (area_id)
      ON DELETE CASCADE
      ON UPDATE CASCADE;
