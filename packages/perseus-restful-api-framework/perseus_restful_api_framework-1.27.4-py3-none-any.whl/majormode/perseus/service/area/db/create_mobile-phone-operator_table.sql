/**
 * Copyright (C) 2010 Skunkworks.  All rights reserved.
 *
 * This software is the confidential and proprietary information of
 * Skunkworks or one of its subsidiaries.  You shall not disclose this
 * confidential information and shall use it only in accordance with
 * the terms of the license agreement or other applicable agreement
 * you entered into with Skunkworks.
 *
 * SKUNKWORKS MAKES NO REPRESENTATIONS OR WARRANTIES ABOUT THE
 * SUITABILITY OF THE SOFTWARE, EITHER EXPRESS OR IMPLIED, INCLUDING
 * BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE, OR NON-INFRINGEMENT.  SKUNKWORKS
 * SHALL NOT BE LIABLE FOR ANY LOSSES OR DAMAGES SUFFERED BY LICENSEE
 * AS A RESULT OF USING, MODIFYING OR DISTRIBUTING THIS SOFTWARE OR
 * ITS DERIVATIVES.
 *
 * @version $Revision: 1802 $
 */

/**
 * A Mobile Network Code (MNC) is used in combination with a Mobile Country Code (MCC) (also known as a "MCC / MNC tuple") to uniquely identify a mobile phone operator/carrier
 *
 * The tuple MCC/MNC/country is NOT unique.  For instance, in Moldova,
 * the mobile phone operators Unité (Moldtelecom) and IDC
 * (Interdnestrcom) share the same MNC.
 */
CREATE TABLE mobile_phone_operator
(
  mcc          int     NOT NULL,
  mnc          int     NOT NULL,
  brand_name   text    NOT NULL,
  country_code char(2) NULL,
  area_id      int     NULL
);
/*
 *  the MCC list (mapping of to country names) you can get from ITU:
http://www.itu.int/dms_pub/itu-t/opb...2007-PDF-E.pdf

Same with MNC (mapping to operator/carrier names):
http://www.itu.int/dms_pub/itu-t/oth...030002PDFE.pdf

*/
