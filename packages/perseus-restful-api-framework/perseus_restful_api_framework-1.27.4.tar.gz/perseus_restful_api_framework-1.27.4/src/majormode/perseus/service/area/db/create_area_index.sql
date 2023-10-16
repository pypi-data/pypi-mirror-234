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

CREATE INDEX idx_area_boundaries
  ON area USING GIST (boundaries);

CREATE INDEX idx_area__boundaries
  ON area USING GIST (_boundaries);

CREATE INDEX idx_area_bounding_box
  ON area USING GIST (bounding_box);

CREATE INDEX idx_area_area_level
  ON area (area_level);

CREATE INDEX idx_area_parent_area_id
  ON area (parent_area_id);


CREATE INDEX idx_area_label_area_id
  ON area_label (area_id);


CREATE INDEX idx_area_index_keyword
  ON area_index (keyword);
