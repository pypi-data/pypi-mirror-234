/**
 * Copyright (C) 2019 Majormode.  All rights reserved.
 *
 * Permission is hereby granted, free of charge, to any person obtaining
 * a copy of this software and associated documentation files (the
 * "Software"), to deal in the Software without restriction, including
 * without limitation the rights to use, copy, modify, merge, publish,
 * distribute, sublicense, and/or sell copies of the Software, and to
 * permit persons to whom the Software is furnished to do so, subject to
 * the following conditions:
 *
 * The above copyright notice and this permission notice shall be
 * included in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 * EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
 * MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
 * IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
 * CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
 * TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
 * SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */

--(defconstant +application-stage-sandbox+ 'sandbox')
--(defconstant +application-stage-live+ 'live')

/**
 * Represent an application, also referred as a *client application*,
 * is a Web application, a desktop application, a mobile application,
 * or any other communication program, that needs to access, generally
 * on behalf of a end-user, to remote services on another computer
 * system, known as a server, by way of a network.
 *
 * An application is given an Application Programming Interface (API)
 * key that the client application integrates to be able to access the
 * remote services that the server platform supports.  This key is a
 * string that tied to such an application, like a `User-Agent`
 * string, for instance.
 *
 * An API key is different from the identification of the application
 * this key is associated with as a key can be revoked or changed by
 * another, for instance, when the secret key has been revealed.
 */
CREATE TABLE application
(
  -- The identification of the application.
  app_id uuid NOT NULL DEFAULT uuid_generate_v4(),

  -- The official name of the application.
  app_name text NOT NULL,

  -- The package name of this application, using the following reverse
  -- domain name notation:
  --
  --     <tld>.<company>.<product>[.<platform>[.<component>]]
  --
  -- where the package segment names are:
  --
  -- * `tld`: top-level domain, usually `com` or `org`.
  --
  -- * `company`: code name of the company who produces this application.
  --
  -- * `product`: code name of the product this application belongs to,
  --   also known as the application family
  --
  -- * `platform`: cf. column `platform`.
  --
  -- * `component`: code name of a version of this application, such as a
  --   a lite (free) or full (paid) versions, or any custom version.
  --
  -- A package name needs to be unique.  Each package segment name can
  -- contain any lowercase latin character ('a' through 'z'), number, and
  -- underscore ('_').  Each package segment name must only start with
  -- letters.
  --
  -- A package name allows several applications that share a set of
  -- functionalities and a user base to be grouped under a same "branding
  -- umbrella".  Grouping applications of a same family allows sending
  -- notifications to a user whatever version(s) and platform(s) of the
  -- application he uses.
  package_name text NULL,

  -- The platform on which the application is running, such as, but not
  -- limited to:
  --
  -- * `console`
  -- * `console:linux`
  -- * `console:mac`
  -- * `console:windows`
  -- * `desktop`
  -- * `desktop:linux`
  -- * `desktop:mac`
  -- * `desktop:windows`
  -- * `mobile`
  -- * `mobile:android`
  -- * `mobile:ios`
  -- * `mobile:windows`
  -- * `server`
  -- * `server:rest`
  -- * `server:web`
  platform text NOT NULL,

  -- The identification of the picture/logo representing this application.
  picture_id uuid NULL,

  -- A unique string used by the Consumer to identify itself to the Service
  -- Provider.
  consumer_key text NOT NULL,

  -- A secret used by the Consumer to establish ownership of the Consumer
  -- Key.
  consumer_secret text NOT NULL,

  -- The identification of the account of the user who registered the
  -- application.
  account_id uuid NOT NULL,

  -- The identification of the organization on behalf of this application
  -- has been registered to.
  team_id uuid NULL,

  -- The logical name of the environment stage which the application is
  -- deployed in:
  --
  -- * `sandbox`
  -- * `live+`
  stage text NOT NULL DEFAULT +application-stage-sandbox+,

  -- The current status of the application.
  object_status text NOT NULL DEFAULT +object-status-enabled+,

  -- The time when the application has been registered.
  creation_time timestamptz(3) NOT NULL DEFAULT current_timestamp,

  -- The time of the most recent modification of one or more properties
  -- of the application.
  update_time timestamptz(3) NOT NULL DEFAULT current_timestamp
);
