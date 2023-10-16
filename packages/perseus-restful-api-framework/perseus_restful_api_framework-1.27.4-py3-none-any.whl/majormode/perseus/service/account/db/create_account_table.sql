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

--(defconstant +account-type-standard+ 'standard')
--(defconstant +account-type-sns+ 'sns')
--(defconstant +account-type-botnet+ 'botnet')
--(defconstant +account-type-test+ 'test')
--(defconstant +account-type-administrator+ 'administrator')


/**
 * Represent user accounts, or system entities, that have been
 * registered against the online platform.
 *
 * Email address and password are optional since a user might use an
 * authenticated session of a Social Networking Site (such as Facebook,
 * Twitter, etc.) to sign-in against the online service.  email
 * address and password are more likely defined when a user signs-up
 * against the platform without sign-in against a Social Networking
 * Site (SNS).
 */
CREATE TABLE account (
  -- Identification of this user account.
  account_id uuid NOT NULL DEFAULT uuid_generate_v4(),

  -- The personal name by which the user is known.  It is either given by
  -- the user himself or an administrator, or as determined from the email
  -- address of this user.
  full_name text NULL,

  -- Forename (also known as *given name*) of the user.  The first name can
  -- be used to alphabetically sort a list of users.
  first_name text NULL,

  -- Surname (also known as *family name*) of the user.  The last name can
  -- be used to alphabetically sort a list of users.
  last_name text NULL,

  -- Also known as screen name or nickname, username is chosen by the end
  -- user to identify himself when accessing the platform and communicating
  -- with others online.  A username should be totally made-up pseudonym,
  -- not reveal the real name of the person.  The username is unique across
  -- the platform.  A username is not case sensitive.
  username text NULL,

  -- Describe the context that caused the registration of this user account,
  -- such as `standard`, `botnet`, `ghost`, `sns`.
  account_type text NOT NULL DEFAULT 'standard',

  -- Encrypted version of the password.
  password text NULL,

  -- Indicate whether user must change his password at the next login.
  is_password_change_required boolean NOT NULL DEFAULT false,

  -- Indicate whether the user can change his password.
  can_password_be_changed boolean NOT NULL DEFAULT false,

  -- Indicate whether the password of the user never expires.
  does_password_never_expire boolean NOT NULL DEFAULT true,

  -- The identification of the picture of the user account, whether the
  -- graphical representation of the user (avatar) or their photo ID.
  picture_id uuid NULL,

  -- A locale that references the preferred language of the user.  A
  -- locale is expressed by a ISO 639-3 alpha-3 code element, optionally
  -- followed by a dash character "-" and a ISO 3166-1 alpha-2 code.  For
  -- example: "eng" (which denotes a standard English), "eng-US" (which
  -- denotes an American English).
  language varchar(6) NOT NULL DEFAULT 'eng',

  -- Nationality of the user expressed by a ISO 3166-1 alpha-2 code.
  nationality char(2) NULL,

  -- Time zone of the default location of the user.  It is the difference
  -- between the time at this location and UTC (Universal Time Coordinated).
  -- UTC is also known as GMT or Greenwich Mean Time or Zulu Time.
  timezone smallint NULL,

  -- Current status of this user account.
  object_status text NOT NULL DEFAULT 'pending',

  -- Time when this user account has been created.
  creation_time timestamptz(3) NOT NULL DEFAULT current_timestamp,

  -- Time of the most recent modification of information of this user
  -- account.
  update_time timestamptz(3) NOT NULL DEFAULT current_timestamp,

  -- Time of the last login of the user who connected with this account.
  last_login_time timestamptz(3) NULL,

  -- Identification of the client application that registered this user
  -- account.  This information could be missing as the first accounts
  -- might be created without using a client application but the command
  -- line (cf. the "chicken or the egg" causality dilemma).
  app_id uuid NULL
);


/**
 * Represent the contact information of users.
 *
 * A contact information corresponds to e-mail addresses and phone
 * numbers.
 *
 *
 * @note: There can be only a unique property with a given name and a
 *     given value.
 */
CREATE TABLE account_contact (
  -- The identification of a user account.
  account_id uuid NOT NULL,

  -- The name (type) of this contact information:
  --
  -- * `EMAIL`: An electronic mail address.
  --
  -- * `PHONE`: A phone number in E.164 numbering plan, an ITU-T
  --    recommendation which defines the international public
  --    telecommunication numbering plan used in the Public Switched
  --    Telephone Network (PSTN).
  property_name text NOT NULL,

  -- A string representation of the value associated to this contact
  -- information.
  property_value text NOT NULL,

  -- The property value of a contact information can be further
  -- qualified with a property parameter expression.  The property
  -- parameter expressions are specified as either a single string or
  -- `name=value`, separated with comas.  This information is optional.
  property_parameter text NULL,

  -- Indicate whether this contact information is the primary contact
  -- for this type of contact information (cf. {@link
  -- account_contact.property_name}).
  is_primary boolean NOT NULL DEFAULT false,

  -- The visibility of this contact information to other users.
  visibility text NOT NULL DEFAULT 'private',

  -- Indicate whether this contact information has been verified, it has
  -- been grabbed from a trusted Social Networking Service (SNS), or
  -- through a challenge/response process.
  is_verified boolean NOT NULL DEFAULT false,

  -- The current status of this contact information.
  object_status text NOT NULL DEFAULT 'enabled',

  -- The time when this contact information has been created.
  creation_time timestamptz(3) NOT NULL DEFAULT current_timestamp,

  -- The time of the most recent modification of this contact information.
  update_time timestamptz(3) NOT NULL DEFAULT current_timestamp,

  -- The identification of the client application that has created or
  -- updated this contact information.
  app_id uuid NULL
);


/**
 * Represent requests sent by user to change one of their contact
 * information.
 */
CREATE TABLE account_contact_change_request
(
  -- The identification of the contact information change request.
  request_id uuid NOT NULL DEFAULT uuid_generate_v4(),

  -- The verification code (also known as a "number used once"), a pseudo-
  -- random number issued and sent to the user to allow him to confirm the
  -- change of his contact information.
  verification_code text NULL,

  -- The identification of the account of the user that requested to change
  -- one of his contact information.
  account_id uuid NOT NULL,

  -- The identification of the client application that submitted this
  -- request.
  app_id uuid NOT NULL,

  -- A locale that references the preferred language of the user.
  --
  -- A locale is expressed by a ISO 639-3 alpha-3 code  element, optionally
  -- followed by a dash character `-` and a ISO 3166-1 alpha-2 code.  For
  -- example: `eng` (which denotes a standard English), `eng-US` (which
  -- denotes an American English).
  language varchar(6) NOT NULL DEFAULT 'eng',

  -- The type of the contact information that the user requested to change.
  -- This type is one of a set of predefined strings in respect with the
  -- electronic business card specification (vCard), such as:
  --
  -- * `EMAIL`: e-mail address.
  --
  -- * `PHONE`: phone number in E.164 numbering plan, an ITU-T recommendation
  --   which defines the international public telecommunication numbering
  --   plan used in the Public Switched Telephone Network (PSTN).
  property_name text NOT NULL,

  -- The old value of the contact information that the user requests to
  -- change.
  property_old_value text NOT NULL,

  -- The new value of the contact information that the user requests to
  -- change to.
  property_new_value text NOT NULL,

  -- A JSON expression corresponding to the context in which this contact
  -- information is being changed.
  context text NULL,

  -- The number of times the user requested to change this contact
  -- information.
  request_count smallint NOT NULL DEFAULT 1,

  -- The number of times the cloud service sent a message with a
  -- verification code to the new address of the user's contact information.
  attempt_count smallint NOT NULL DEFAULT 0,

  -- The current status of this request.
  --
  -- * `+object-status-deleted+`: The request has been fulfilled.
  --
  -- * `+object-status-disabled+`: The request has expired.
  --
  -- * `+object-status-enabled+`: The request is active.
  object_status text NOT NULL DEFAULT +object-status-enabled+,

  -- The time when the user requested to change his contact information.
  creation_time timestamptz(3) NOT NULL DEFAULT current_timestamp,

  -- The time of the most recent modification of one or more attributes of
  -- this request.
  update_time timestamptz(3) NOT NULL DEFAULT current_timestamp,

  -- The time when this request expires.
  expiration_time timestamptz(3) NOT NULL,

  -- The time of the last attempt in sending a message with a verification
  -- code to the user's.
  last_attempt_time timestamptz(3) NULL
);


/**
 * Represent requests to users to verify their contact information.
 */
CREATE TABLE account_contact_verification (
  -- Identification of contact information verification request.
  request_id uuid NOT NULL DEFAULT uuid_generate_v4(),

  -- A pseudo-random number (nonce) that was generated and sent to the
  -- user to verify his contact information.
  verification_code text NULL,

  -- Identification of the account of the user who is requested to verify
  -- his contact information.
  account_id uuid NULL,

  -- The identification of the client application that adds the user's
  -- contact information.
  app_id uuid NOT NULL,

  -- A locale that references the preferred language of the user.  A locale
  -- is expressed by a ISO 639-3 alpha-3 code  element, optionally followed
  -- by a dash character "-" and a ISO 3166-1 alpha-2 code.  For example:
  -- "eng" (which denotes a standard English), "eng-US" (which denotes an
  -- American  English).
  language varchar(6) NOT NULL DEFAULT 'eng',

  -- Name of this contact information, which can be one of a set of pre-
  -- defined strings in respect with the electronic business card
  -- specification (vCard), such as:
  --
  -- * `EMAIL`: e-mail address.
  --
  -- * `PHONE`: phone number in E.164 numbering plan, an ITU-T recommendation
  --   which defines the international public telecommunication numbering
  --   plan used in the Public Switched Telephone Network (PSTN).
  property_name text NOT NULL,

  -- Value of this contact information representing by a string.
  property_value text NOT NULL,

  -- Indicate the type of the action that initiates requests for verifying
  -- contact information.
  action_type text NULL,

  -- A JSON expression corresponding to the context in which this contact
  -- has been added and needs to be verified.
  context_payload text NULL,

  -- Number of times this contact information has been requested to be
  -- verified.
  request_count smallint NOT NULL DEFAULT 0,

  -- Number of times the platform sent this request to the user.
  attempt_count smallint NOT NULL DEFAULT 0,

  -- The current status of this request.
  object_status text NOT NULL DEFAULT 'enabled',

  -- The time when this request has been sent to the user for the first time.
  creation_time timestamptz(3) NOT NULL DEFAULT current_timestamp,

  -- The time of the most recent modification of one attribute of this request.
  update_time timestamptz(3) NOT NULL DEFAULT current_timestamp,

  -- The time when this request expires.
  expiration_time timestamptz(3) NOT NULL,

  -- The time of the last attempt in sending this request to the user.
  last_attempt_time timestamptz(3) NULL
);


/**
 * Represent the normalized keywords extracted from several attributes
 * of user accounts.
 */
CREATE TABLE account_index (
  -- The identification of a user account.
  account_id uuid NOT NULL,

-- A plain ASCII and lowercase representation of a word collected from
-- the full_name of the account.  Each keyword is at least 2-character
-- long.
  keyword text NOT NULL
);


/**
 * Represent requests from users who have forgotten their password and
 * who would like to reset their password.
 */
CREATE TABLE account_password_reset (
  -- Identification of the password reset request.  This identification
  -- can be used in a link sent to the user to allow him to change his
  -- password through a Web application.
  request_id uuid NOT NULL DEFAULT uuid_generate_v4(),

  -- "Number used once", a pseudo-random number issued when generating the
  -- request to allow the user to change his password through a mobile
  -- application.
  nonce text NULL,

  -- Identification of the account of the user that requested to change his
  -- forgotten password.
  account_id uuid NOT NULL,

  -- Identification of the client application that submitted on behalf of
  -- the end user the request to reset his password.
  app_id uuid NOT NULL,

  -- A locale that references the preferred language of the user.  A locale
  -- is expressed by a ISO 639-3 alpha-3 code  element, optionally followed
  -- by a dash character "-" and a ISO 3166-1 alpha-2 code.  For example:
  -- "eng" (which denotes a standard English), "eng-US" (which denotes an
  -- American  English).
  language varchar(6) NOT NULL DEFAULT 'eng',

  -- Name of the contact information that indicates the communication
  -- method to used for sending the reset password request to the user.
  -- This name is one of a set of predefined strings in respect with the
  -- electronic business card specification (vCard), such as:
  --
  -- * `EMAIL`: e-mail address.
  --
  -- * `PHONE`: phone number in E.164 numbering plan, an ITU-T recommendation
  --   which defines the international public telecommunication numbering
  --   plan used in the Public Switched Telephone Network (PSTN).
  property_name text NOT NULL,

  -- Value of this contact information representing by a string.
  property_value text NOT NULL,

  -- A JSON expression corresponding to the context in which this contact
  -- has been added and needs to be verified.
  context_payload text NULL,

  -- Number of times the user requested to reset his password before he
  -- finally changed it.
  request_count smallint NOT NULL DEFAULT 1,

  -- Number of times the platform sent an email to the user with an
  -- embedded link to let this user reset his password.
  attempt_count smallint NOT NULL DEFAULT 0,

  -- Current status of this request.
  --
  -- * `+object-status-deleted+`: The request has been fulfilled.
  --
  -- * `+object-status-disabled+`: The request has expired.
  --
  -- * `+object-status-enabled+`: The request is active.
  object_status text NOT NULL DEFAULT +object-status-enabled+,

  -- Time when the user requested to reset his forgotten password.
  creation_time timestamptz(3) NOT NULL DEFAULT current_timestamp,

  -- Time of the most recent modification of one or more attribute of
  -- this password reset request.
  update_time timestamptz(3) NOT NULL DEFAULT current_timestamp,

  -- Time when this request expires.
  expiration_time timestamptz(3) NOT NULL,

  -- Time of the last attempt in sending this request to the user.
  last_attempt_time timestamptz(3) NULL
);


/**
 * Represent the history of the past and current pictures of the user.
 */
CREATE TABLE account_picture (
  -- The identification of the picture.
  picture_id uuid NOT NULL,

  -- The identification of the user account that the picture is associated
  -- with.
  --
  -- @note: This column is null when the user account was hard-deleted.  A
  --     clean-up process will delete the files of all orphan pictures,
  --     before deleting the corresponding records.
  account_id uuid NULL,

  -- The identification of the account of the user who submitted the
  -- picture.
  --
  -- @note: This column is null when the submitter user account is hard-
  --     deleted.
  submitter_account_id uuid NULL,

  -- The identification of the organization of the user who submitted the
  -- picture.
  team_id uuid NULL,

  -- The time when the picture was captured.
  capture_time timestamptz(3) NULL,

  -- The number of pixel columns of the user's original photo image.
  image_width smallint NOT NULL,

  -- The number of pixel rows of the user's original photo image.
  image_height smallint NOT NULL,

  -- The size in bytes of the user's original photo image file.
  image_file_size int NOT NULL,

  -- The message digest of the binary data of the user's original photo
  -- image file.
  image_file_checksum text NOT NULL,

  -- Indicate whether the picture needs to be reviewed by someone who has
  -- authority on the online service used by the end users.
  is_review_required boolean NOT NULL DEFAULT false,

  -- Identification of the client application that uploaded the picture.
  app_id uuid NOT NULL,

  -- The exception describing the reason for which the picture may have
  -- been rejected:
  --
  -- * `NoFaceDetectedException`: No face has been detected in the photo.
  --
  -- * `MultipleFacesDetectedException``: Multiple faces have been detected
  --   in the photo.
  --
  -- * `MissingFaceFeaturesException` Some features are missing from the
  --   detected face.
  --
  -- * `ObliqueFacePoseException`: The head doesn't face the camera straight
  --   on.
  --
  -- * `OpenedMouthOrSmileException`: The mouth is not closed or with a
  --   smile.
  --
  -- * `AbnormalEyelidOpeningStateException`: An eyelid is widely opened,
  --   narrowed or closed.
  --
  -- * `UnevenlyOpenEyelidException`: An eye is more opened/closed than the
  --   other.
  rejection_exception text NULL,

  -- The current status of the picture:
  --
  -- * `deleted`: The photo has been rejected or deleted.
  --
  -- * `disabled`: The photo has been temporarily disabled by an
  --   administrator of the attendant's organization.
  --
  -- * `enabled`: The photo has been successfully processed.
  --
  -- * `pending`: The photo is being processed.
  object_status text NOT NULL DEFAULT +object-status-pending+,

  -- The time when this photo has been registered.
  creation_time timestamptz(3) NOT NULL DEFAULT current_timestamp,

  -- The time of the most recent modification of the status of this picture.
  update_time timestamptz(3) NOT NULL DEFAULT current_timestamp
);


/**
 * The list of user's preferences.
 *
 * Preferences, also confusingly known as _settings_, allow users to
 * change the functionality and behavior of an application.  Preferences
 * can affect background behavior, such as how often the application
 * synchronizes data with the cloud, or they can be more wide-reaching,
 * such as changing the contents and presentation of the user interface.
 *
 * A preference is identified with a symbolic name that follows the
 * package name style syntax, borrowed from the [reverse domain name
 * notation](https://en.wikipedia.org/wiki/Reverse_domain_name_notation>).
 *
 * Preference symbolic names SHOULD be written in all lower case with
 * underscores.  For instance as `com.example.my_preference`.
 *
 * Package name style syntax allows to group preferences by _sections_,
 * also known as _categories_:
 *
 * - ``io.xebus.notification.outward_trip.is_checkin_notification_enabled``
 * - ``io.xebus.notification.outward_trip.is_checkout_notification_enabled``
 * - ``io.xebus.notification.outward_trip.is_school_bus_departure_notification_enabled``
 * - ``io.xebus.notification.outward_trip.is_school_bus_arrival_notification_enabled``
 * - ``io.xebus.notification.outward_trip.school_bus_eta_notification_lead_time``
 *
 *
 * @note: If a _setting_ comes with a default value, then that _setting_
 *     is not a _preference_ until the user changes it.
 *
 * @note: Preferences defined with default values SHOULD be removed from
 *     the storage.  It's more unlikely that the default value of a
 *     preference changes over the time, meaning that we SHOULD not need
 *     to keep user preference that corresponds to the default value.
 */
CREATE TABLE account_preference (
  /**
   * The identifier of the account of the user who defined this
   * preference.
   */
  account_id uuid NOT NULL,

  /**
   * The identifier of the client application for which this preference is
   * specific.
   */
  app_id uuid NULL,

  /**
   * The code name of a user preference.
   */
  property_name text NOT NULL,

  /**
   * The string representation of the preference's value.
   */
  property_value text NOT NULL,

  /**
   * The time of the most recent modification of the value of this user's
   * preference.
   */
  update_time timestamptz(3) NOT NULL DEFAULT current_timestamp
);
