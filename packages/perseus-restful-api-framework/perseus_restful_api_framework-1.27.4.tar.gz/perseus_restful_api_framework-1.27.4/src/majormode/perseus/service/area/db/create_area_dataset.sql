/**
 * -*- coding: utf-8 -*-
 *
 * Copyright (C) 2013 Majormode.  All rights reserved.
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

--
--INSERT INTO area(area_id, area_code, area_name, area_type) VALUES
--  (6255146, 'AF', 'Africa', 'continent'),
--  (6255147, 'AS', 'Asia', 'continent'),
--  (6255148, 'EU', 'Europe', 'continent'),
--  (6255149, 'NA', 'North America', 'continent'),
--  (6255151, 'OC', 'Oceania', 'continent'),
--  (6255150, 'SA', 'South America', 'continent'),
--  (6255152, 'AN', 'Antarctica', 'continent')
--
--
--
--SUBREGION   SUBREGION_NAME
--1A  Central Africa
--1B  Eastern Africa
--1C  Indian Ocean
--1D  Northern Africa
--1E  Southern Africa
--1F  Western Africa
--2A  Central America
--2B  North America
--2C  South America
--2D  West Indies
--3A  Antarctica
--3B  Atlantic Ocean
--4A  Central Asia
--4B  East Asia
--4C  Northern Asia
--4D  South Asia
--4E  South East Asia
--4F  South West Asia
--5A  Central Europe
--5B  Eastern Europe
--5C  Northern Europe
--5D  South East Europe
--5E  South West Europe
--5F  Southern Europe
--5G  Western Europe
--6A  North Pacific Ocean
--6B  Pacific
--6C  South Pacific Ocean
--
--SELECT register_region('Caribbean, the', 'America');
--SELECT register_region('Central America', 'America');
--SELECT register_region('Northern America', 'America');
--SELECT register_region('South America', 'America');
--SELECT register_region('Eastern Europe', 'Europe');
--SELECT register_region('Northern Europe', 'Europe');
--SELECT register_region('Southern Europe', 'Europe');
--SELECT register_region('Western Europe', 'Europe');
--SELECT register_region('Eastern Asia', 'Asia');
--SELECT register_region('South-central Asia', 'Asia');
--SELECT register_region('South-eastern Asia', 'Asia');
--SELECT register_region('Western Asia', 'Asia');
--SELECT register_region('Eastern Africa', 'Africa');
--SELECT register_region('Middle Africa', 'Africa');
--SELECT register_region('Northern Africa', 'Africa');
--SELECT register_region('Southern Africa', 'Africa');
--SELECT register_region('Western Africa', 'Africa');
--SELECT register_region('Australia & New Zealand', 'Oceania');
--SELECT register_region('Melanesia', 'Oceania');
--SELECT register_region('Micronesia', 'Oceania');
--SELECT register_region('Polynesia', 'Oceania');
