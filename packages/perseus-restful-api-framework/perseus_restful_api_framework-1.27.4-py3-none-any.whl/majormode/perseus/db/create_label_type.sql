/**
 * Copyright (C) 2016 Majormode.  All rights reserved.
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

/**
 * Represent a localised label.
 */
CREATE TYPE label AS
(
  -- textual content of the label in a given locale.
  content text,

  -- ISO 639-3 alpha-3 code element, optionally followed by a dash
  -- character "-" and a ISO 3166-1 alpha-2 code.  For example: "eng"
  -- (which denotes a standard English), "eng-US" (which denotes an
  -- American English).
  locale varchar(6)
);
