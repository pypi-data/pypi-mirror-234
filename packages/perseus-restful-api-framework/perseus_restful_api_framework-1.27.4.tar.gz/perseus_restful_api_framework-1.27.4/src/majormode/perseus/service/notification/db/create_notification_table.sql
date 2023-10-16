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

/**
 * Notifications to send to recipients, either users identified by their
 * account, either devices.
 */
CREATE TABLE notification (
  /**
   * The identifier of the notification.
   */
  notification_id uuid NOT NULL DEFAULT uuid_generate_v4(),

  /**
   * The type of the notification as selected by the sender that originated
   * this notification to the intended recipient, such as, for instance,
   * `on_something_happened`.
   */
  notification_type text NOT NULL,

  /**
   * The mode to deliver this notification to the recipients:
   *
   * - `pull` (default): Indicate that a notification message is
   *   delivered to the specified recipients when the request for the
   *   transmission of information is initiated by the receiver or client
   *   application, and then is responded by the publisher or server
   *   platform.
   *
   * - `push`: Indicate that a notification message is delivered to the
   *   specified recipients when the request for the transmission of
   *   information is initiated by the publisher or server platform and
   *   pushed out to the receiver or client application.
   */
  notification_mode text NOT NULL DEFAULT 'pull',

  /**
   * The identifier of the recipient that is issued this notification,
   * such as the identifier of a user account, or the identifier of a
   * device (e.g., International Mobile Equipment Identity (IMEI) for
   * Android device, an alphanumeric string for iOS device).
   */
  recipient_id text NOT NULL,

  /**
   * The identifier of the sender who originated the notification, either
   * the identifier of a user account, or the identifier of a device (e.g.,
   * International Mobile Equipment Identity (IMEI) for Android device,
   * an alphanumeric string for iOS device).
   */
  sender_id text NULL,

  /**
   * Any arbitrary JSON expression that provides information about the
   * context of this notification.
   */
  payload text NULL,

--  -- Indicate whether this message needs to be broadcast to every
--  -- registered users/devices interested in this message.  If so, the
--  -- column identifying a recipient is null.
 --  is_broadcast boolean NOT NULL DEFAULT false,

  /**
   * Indicate whether the notification has been read by the intended
   * recipient.
   */
  is_read boolean NOT NULL DEFAULT false,

  /**
   * The time when this notification is scheduled to be sent to the
   * intended recipient.  The notification is not visible to the intended
   * recipient prior to this time.  If not specified, the notification is
   * sent as soon as possible.
   */
  schedule_time timestamptz(3) NULL,

  /**
   * Indicate whether the schedule time is assumed to be in local time
   * of a particular device.  If so, the schedule time must be converted
   * to UTC, and the time zone information must be then stripped out to
   * provide a local time.  For instance, if the specified schedule time
   * is `2013-12-20 13:00:00+07` and `use_local_time` is set to `true`,
   * the schedule time is assumed to be the local time `2013-12-20 06:00:00`
   * for the region, i.e., time zone, of a particular user/device to send
   * the message to.
   */
  use_local_time boolean NULL DEFAULT false,

  /**
   * The time after which the notification expires, corresponding to the
   * lifespan of the notification.  When a notification expires, the
   * content is removed from the queue and is no longer available to the
   * recipient.  It is a best practice to set an expiration on all
   * notifications, using a time that makes sense for an application, to
   * ensure that the notification does not persist longer than it is
   * relevant.
   *
   * If `use_local_time` is set to `true`, this time is assumed to be in
   * local time of any particular user/device to push this message to.
   */
  expiration_time timestamptz(3) NULL,

  /**
   * The identifier of the application that initiated this notification.
   */
  app_id uuid NULL,

  /**
   * The package name of the applications to send the notification to,
   * using the reverse domain name notation.
   *
   * The package name can be fully or partially qualified to encompass one
   * particular variant or a set of applications of a same family.  For
   * instance:
   *
   * - `com.my_company.my_product` matches any application belonging to the
   *   specified product.
   *
   * - `com.my_company.my_product.android` matches any Android version of
   *   this product.
   *
   * - `com.my_company.my_product.android.lite` only matches the lite
   *   Android version of this product.
   */
--  package_name text NULL,

  /**
   * The current status of this notification.
   */
  object_status text NOT NULL DEFAULT 'enabled',

  /**
   * The time when the notification was registered.
   */
  creation_time timestamptz(3) NOT NULL DEFAULT current_timestamp,

  /**
   * The time of the most recent modification of one or more properties of
   * this notification.
   */
  update_time timestamptz(3) NOT NULL DEFAULT current_timestamp
);


/**
 * Devices registered to the push notification service, interested in
 * receiving asynchronous messages from one or more application services
 * hosted on the server platform.
 */
CREATE TABLE notification_device (
  /**
   * The registration identifier of a device to the push notification
   * service.
   */
  registration_id uuid NOT NULL DEFAULT uuid_generate_v4(),

  /**
   * The identifier of the device, which depends on the device platform.
   *
   * On Android, it used to be the International Mobile Equipment Identity
   * (IMEI) number of the device.  Android 10 (API level 29) adds
   * restrictions for non-resettable identifiers, which include both IMEI
   * and serial number.  It is now a hashed version of some hardware
   * identifiers, or a 64-bit number (expressed as a hexadecimal string),
   * unique to each combination of app-signing key, user, and device.
   * Values of this identifier are scoped by signing key and user.  The
   * value may change if a factory reset is performed on the device or if
   * an APK signing key changes.
   *
   * On iOS, it is a unique identifier of the iOS device, previously the
   * Unique Device Identifier (UDID) of the device, which is a 40-character
   * string that is tied to this specific Apple device.  It could be a
   * SecureUDID, which is an open-source sandboxed UDID solution aimed at
   * solving the main privacy issues that caused Apple to deprecate UDIDs.
   */
  device_id text NOT NULL,

  /**
   * Token that identifies the device by the push notification provider of
   * the device platform:
   *
   * - Android: token identifying the device to push the notification to,
   *   i.e., the registration ID.  A device token is an opaque identifier of
   *   a device that Google Firebase Cloud Messaging (FCM) gives to the
   *   device when it first connects with it.  The device shares the device
   *   token with its provider.  The device token is analogous to a phone
   *   number; it contains information that enables FCM to locate the device
   *   on which the client application is installed.  FCM also uses it to
   *   authenticate the routing of a notification.
   *
   * - iOS: token identifying the iOS device to push the notification to.  A
   *   device token is an opaque identifier of a device that APNs gives to
   *   the device when it first connects with it.  The device shares the
   *   device token with its provider.  Thereafter, this token accompanies
   *   each notification from the provider.  The device token is analogous to
   *   a phone number; it contains information that enables APNs to locate
   *   the device on which the client application is installed.  APNs also
   *   uses it to authenticate the routing of a notification.  A device token
   *   is not the same thing as the device UDID returned by the
   *   `uniqueIdentifier` property of `UIDevice`.
   (/)
  device_token text NOT NULL,

  /**
   * The mobile platform of the device:
   *
   * - `ios`: Apple iOS
   *
   * - `android`: Google Android
   *
   * - `windows`: Windows Phone
   */
  device_platform text NOT NULL,

  /**
   * Identification of the application that registered this device for
   * receiving notifications.
   */
  app_id uuid NOT NULL,

  /**
   * The identifier of the user account currently linked with this device.
   * Notifications to be pushed to this user will be pushed to all the
   * devices linked with this user, depending on the package name defined
   * for each notification.
   */
  account_id uuid NULL,

--  /**
--   * Difference between the location of the device and UTC (Universal Time
--   * Coordinated).  UTC is also known as GMT or Greenwich Mean Time or Zulu
--   * Time.
--   */
--  utc_offset int NULL,

  /**
   * The preferred language to receive new content in.  This parameter is
   * not used if the device registered to push notification service on
   * behalf of a user, but the preferred language of this user.
   *
   * A locale corresponds to a tag respecting RFC 4646, expressed by a ISO
   * 639-3 alpha-3 code element, optionally followed by a dash character `-`
   * and a ISO 3166-1 alpha-2 code.  For example: "eng" (which denotes a
   * standard English), "eng-US" (which denotes an American English).
   */
  language varchar(6) NULL,

  /**
   * The current status of the registration of this device to push
   * notification service for this mobile application.
   */
  object_status text NOT NULL DEFAULT 'enabled',

  /**
   * The time when this device registered to push notification.
   */
  creation_time timestamptz(3) NOT NULL DEFAULT current_timestamp,

  /**
   * The time of the most recent modification of one or more properties of
   * this registration.
   */
  update_time timestamptz(3) NOT NULL DEFAULT current_timestamp
);
