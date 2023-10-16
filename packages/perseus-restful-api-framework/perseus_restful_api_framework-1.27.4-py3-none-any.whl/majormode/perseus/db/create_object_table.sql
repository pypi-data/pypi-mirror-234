/**
 * Copyright (C) 2017 Majormode.  All rights reserved.
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
 *
 * @version $Revision$
 */

/**
 * Represent the postal address of entities, composed of one or more
 * address components, which textual information is written in a
 * specified locale.  An address component is defined with a component
 * type and its value.
 */
CREATE TABLE object_address
(
  -- Identification of an entity.
  object_id uuid NOT NULL,

  -- Identification of the account of the user who submitted this component
  -- address.  A default value for an address component can be defined
  -- without account identification.  A default value generally results
  -- from a merge of a similar value suggested by several users.
  account_id uuid NULL,

  -- Component type of this address.  Refer to the API documentation for
  -- the list of the supported address component types.
  property_name text NOT NULL,

  -- Localised value of this address component.
  property_value text NOT NULL,

  -- Locale of the textual information of the address component.  A locale
  -- corresponds to a tag respecting RFC 4646, i.e., a ISO 639-3 alpha-3
  -- code element optionally followed by a dash character - and a ISO 3166-1
  -- alpha-2 code (referencing the country that this language might be
  -- specific to).  For example: ``eng`` (which denotes a standard English),
  -- ``eng-US`` (which denotes an American English).
  locale varchar(6) NOT NULL DEFAULT 'eng',

  -- Indicate the visibility of this address component to other users.
  visibility text NOT NULL DEFAULT +visibility-private+,

  -- Current status of this address component.
  object_status text NOT NULL DEFAULT +object-status-pending+,

  -- Time when this address component has been created.
  creation_time timestamptz(3) NOT NULL DEFAULT current_timestamp,

  -- Time of the most recent modification of this address component.
  update_time timestamptz(3) NOT NULL DEFAULT current_timestamp
);


/**
 * Represent contact information of entities, which correspond to a
 * list of properties such as e-mail addresses, phone numbers, etc.
 *
 *
 * @note: there can be only a unique property with a given name and a
 *     given value.
 */
CREATE TABLE object_contact
(
  -- Identification of the entity this contact information is linked to.
  object_id uuid NOT NULL,

  -- Identification of the account of the user who submitted this contact
  -- property.  A default value for a contact property can be defined
  -- without account identification.  A default value generally results
  -- from a merge of a similar value suggested by several users.
  account_id uuid NULL,

  -- Name of this contact property, which can be one of a set of pre-
  -- defined strings in respect with the electronic business card
  -- specification (vCard), such as:
  --
  -- * ``EMAIL``: e-mail address.
  --
  -- * ``PHONE``: phone number in E.164 numbering plan, an ITU-T
  --   recommendation which defines the international public
  --   telecommunication numbering plan used in the Public Switched Telephone
  --   Network (PSTN).
  --
  -- * ``WEBSITE``: Uniform Resource Locator (URL) of a Web site.
  name text NOT NULL,

  -- A property value can be further qualified with a property parameter
  -- expression, such as for instance, `HOME`, `WORK`.
  parameter text NULL,

  -- Value of the property representing by a string, such as ``+84.01272170781``,
  -- the formatted value for a telephone number property.
  value text NOT NULL,

  -- Indicate whether this contact property is the first to be used to
  -- contact the entity that this contact information corresponds to.
  -- There is only one primary contact property for a given property name
  -- (e.g., `EMAIL`, `PHONE`, `WEBSITE`).
  is_primary boolean NOT NULL DEFAULT true,

  -- Indicate whether this contact information has been verified, whether
  -- it has been grabbed from a trusted Social Networking Service (SNS), or
  -- whether through a challenge/response process.
  is_verified boolean NOT NULL DEFAULT false,

  -- Indicate the visibility of this contact information to other users.
  visibility text NOT NULL DEFAULT +visibility-private+,

  -- Current status of this contact property.
  object_status text NOT NULL DEFAULT +object-status-pending+,

  -- Time when this contact property has been created.
  creation_time timestamptz(3) NOT NULL DEFAULT current_timestamp,

  -- Time of the most recent modification of this contact property.
  update_time timestamptz(3) NOT NULL DEFAULT current_timestamp
);


/**
 * Represent localised labels of entities.
 */
CREATE TABLE object_label
(
  -- Identification of the entity this label is related to.
  object_id uuid NOT NULL,

  -- Identification of the account of the user who defined this label.  A
  -- default content for a label can be defined without account
  -- identification.  A default content generally results from a merge of
  -- a similar content suggested by several users.
  account_id uuid NULL,

  -- Locale of the label.  A locale corresponds to a tag respecting RFC
  -- 4646, i.e., a ISO 639-3 alpha-3 code element optionally followed by
  -- a dash character - and a ISO 3166-1 alpha-2 code (referencing the
  -- country that this language might be specific to).  For example: ``eng``
  -- (which denotes a standard English), ``eng-US`` (which denotes an
  -- American English).
  locale varchar(6) NOT NULL DEFAULT 'eng',

  -- textual content of the label in the given locale.
  content text NOT NULL,

  -- Indicate the visibility of this label to other users.
  visibility text NOT NULL DEFAULT +visibility-private+,

  -- Current status of this label.
  object_status text NOT NULL default +object-status-enabled+,

  -- Time when this label has been defined.
  creation_time timestamptz(3) NOT NULL DEFAULT current_timestamp,

  -- Time of the most recent modification of the content of this label.
  update_time timestamptz(3) NOT NULL DEFAULT current_timestamp
);
