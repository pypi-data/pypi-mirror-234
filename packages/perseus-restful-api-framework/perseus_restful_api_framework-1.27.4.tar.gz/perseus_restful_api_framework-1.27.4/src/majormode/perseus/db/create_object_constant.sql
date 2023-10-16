/**
 * -*- coding: utf-8 -*-
 *
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

/**
 * Define constants specifying standard status of a persistent object
 * stored on the platform used as reference for object synchronization
 * with other remote storages, such as client applications.
 */
--(defconstant +object-status-enabled+ 'enabled')
--(defconstant +object-status-deleted+ 'deleted')
--(defconstant +object-status-disabled+ 'disabled')
--(defconstant +object-status-pending+ 'pending')
