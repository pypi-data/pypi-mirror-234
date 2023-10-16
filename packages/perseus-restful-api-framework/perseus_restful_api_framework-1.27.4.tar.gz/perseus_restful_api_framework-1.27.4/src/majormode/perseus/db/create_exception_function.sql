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
 * Raise a PostgreSQL exception formatting the message, which is
 * reported to the client, in respect of the following convention::
 *
 *   (exception :class P_CLASS_NAME :message "P_MESSAGE" [@parameter ["]value["] ...])
 *
 * @param p_class_name: the name of the exception, for instance
 *        <code>IllegalArgument</code> or whatever else.
 * @param p_message: the message of the exception.
 * @param p_parameters: a string representation of optional parameters
 *        to be added to the exception.  The string representation
 *        must the following convention:
 *        <pre>
 *          @parameter ["]value["] [@parameter ["]value["]]
 *        </pre>
 *
 * @raise exception: the exception defined by the caller.
 */
CREATE OR REPLACE FUNCTION raise_exception(
    IN p_class_name varchar,
    IN p_message varchar,
    IN p_parameters varchar)
  RETURNS void
AS $$
BEGIN
  RAISE EXCEPTION '(exception :class % :message "%" %)',
                  p_class_name, p_message, p_parameters;
END;
$$ LANGUAGE PLPGSQL;
