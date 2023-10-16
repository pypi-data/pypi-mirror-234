# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), 
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.27.4] - 2023-10-09
## Changed
- Minor changes related to 3rd party libraries version

## [1.27.2] - 2023-07-11
# Changed
- Cleanse the Notification Service

## [1.27.1] - 2023-07-11
# Added
- Add user account's preferences management

## [1.27.0] - 2023-07-10
# Changed
- HTTP request handlers return a dictionary object itself instead of embedding it in a `{ "data": dict }`

## [1.26.17] - 2023-06-10
# Fixed
- Return the generated password when creating a new account without specifying a password

## [1.26.14] - 2023-06-10
# Fixed
- Fix the function that generates a password to comply with password complexity requirements

## [1.26.13] - 2023-06-06
# Fixed
- Fix the Account Service's method `get_accounts`

## [1.26.12] - 2023-05-29
# Added
- The Account Service's method `set_object_status` to change the status of an account

## [1.26.11] - 2023-05-25
# Added
- The Team Service's method `set_member_role` to change the role of a team member

## [1.26.10] - 2023-05-23
# Changed
- Allow to create an account without defining a password

## [1.26.9] - 2023-05-23
# Changed
- The Account Service's method `sign_up` allows passing a single contact information

## [1.26.8] - 2023-03-08
# Changed
- Remove the column `picture_time` from the table `account`

## [1.26.7] - 2023-02-15
# Fixed
- An issue that occurs when searching a picture that doesn't exist

## [1.26.6] - 2023-02-15
# Added
- Ensure that the capture time of a photo is not in the future

## [1.26.2] - 2023-02-09
# Changed
- The function `get_account` returns the picture information of the account in a child object

## [1.25.24] - 2023-02-02
### Added
- Add the function `AccountService.get_picture`

## [1.25.18] - 2023-01-30
### Fixed
- Fix the name of the function `AccountService.build_tree_path_name`

## [1.25.16] - 2023-01-30
### Fixed
- Fix an issue that occurs with HTTP request signature validation on development stage

## [1.25.12] - 2023-01-30
### Added
- Add the column `picture_time` to the table `account`
- Return the attribute `picture_time` in the information of the user who logs in

## [1.25.11] - 2023-01-17
### Changed
- The endpoint `version` doesn't require HTTP request signature anymore

## [1.25.9] - 2023-01-04
### Changed
- Update password complexity requirements

## [1.25.8] - 2022-11-24
### Fixed
- Doesn't force retrieving the application ID when signature is not mandatory

## [1.25.4] - 2022-11-23
### Changed
- Migrate to Pipenv to Poetry
### Fixed
- Fix circular module import issue

## [1.24.17] - 2022-11-23
### Fixed
- Fix the regular expression of the URL bits

## [1.24.16] - 2022-08-24
### Fixed
- Fix the regular expression that validates password compliance with complexity requirements

## [1.24.13] - 2022-04-27
### Added
- Display the environment stage in which the RESTful API server is run

## [1.24.11] - 2022-01-12
### Changed
- Update the password format requirements

## [1.24.10] - 2021-12-08
### Changed
- Remove a username in used from a deleted user account to assign it 
  to another user account

## [1.24.9] - 2021-12-04
### Added
- Add a method to set the username of a user account

## [1.24.8] - 2021-11-12
### Changed
- Fix sign-in with username

## [1.24.7] - 2021-08-31
### Added
- Add the identification of the user who uploads the picture for a user
- Add the identification of the organization of the user who uploads the 
  picture for a user
- Change the picture history logic

## [1.23.2] - 2021-08-26
### Changed
- Fix an argument name issue while migrating from the library `pylibmc` to `pymemcache`

## [1.23.1] - 2021-08-25
### Changed
- Fix an issue with casting a database value to a locale object
- Replace library `pylibmc` with `pymemcache`

## [1.23.0] - 2021-08-08
### Changed
- Change the interface of the class `BaseRdbmsService`

## [1.22.31] - 2021-07-21
### Changed
- Fix argument name `locale` of prosoponym functions

## [1.22.29] - 2021-07-08
### Changed
- Fix method `get_accounts`

## [1.22.27] - 2021-07-08
### Changed
- Add a parameter to require the validation of the password of a new account

## [1.22.24] - 2021-06-28
### Changed
- Rename the attribute `locale` of a user's account with `language`
- Rename the attributes `name` and `value` of a contact information with `property_name` and `property_value`

## [1.21.0] - 2021-06-27
### Added
- Nationality of a user

## [1.20.5] - 2021-06-22
### Added
- Add a method to find the hierarchy of areas that contains a location

## [1.20.2] - 2021-06-21
### Changed
- Remove useless parameter `app_id`

## [1.19.23] - 2021-06-16
### Changed
- Update the function that set the primary contact information of a user
### Added
- Add a function to set the preferred language of a user

## [1.19.16] - 2021-06-02
### Changed
- Fix an issue while indexing a new account after creation

## [1.19.15] - 2021-06-02
### Changed
- Add an optional argument `connection` to the method that returns a list of notifications

## [1.19.11] - 2021-05-28
### Added
- Add a method to reset the password of a user account on behalf of an administrator

## [1.19.8] - 2021-05-28
### Changed
- Fix a bug in the function to suspend or reactive a member of an organization

## [1.19.7] - 2021-05-28
### Changed
- Rework device registration to push notification service

## [1.19.4] - 2021-05-27
### Changed
- Add a method to suspend or reactive the account of an organization member.

## [1.19.1] - 2021-05-27
### Changed
- Fix the detection of the API server process's name

## [1.19.0] - 2021-05-27
### Changed
- Remove notification service HTTP handler

## [1.18.11] - 2021-05-27
### Changed
- Include the new environment variables loader using .env file

## [1.17.38] - 2021-05-26
### Added
- Refactor the launch and termination script 

## [1.17.32] - 2021-05-25
### Added
- Limit the helper function to reindex the accounts from the parent table `account` 

## [1.17.31] - 2021-05-25
### Added
- Add a helper function to reindex all the accounts (another technology, such as Elasticsearch, should be used for indexing accounts)

## [1.17.30] - 2021-05-07
### Changed
- Return information about the account that has been created or updated
- Check the signature of any HTTP request when provided

## [1.17.28] - 2021-05-05
### Added
- Option to disable the requirement of the full name to be formatted according to the lexical name related to the culture of the person

## [1.17.26] - 2021-05-01
### Changed
- Hack the registration process of a new user account to allow an agent sending an email to the user with his credential to connect to the service 

## [1.17.18] - 2021-04-29
### Added
- Method to upsert a new or existing account

## [1.17.12] - 2021-04-23
### Changed
- Fix passing the optional argument `tag` to the method `RdbmsConnection.acquire_connection`

## [1.17.11] - 2021-04-22
### Changed
- Change the scope of the method `store_picture_image_file` to public
- Change the scope of the method `update_password_reset_request` to public

## [1.17.8] - 2021-04-12
### Changed
- Change the name of the bucket containing user account's picture (avatar)

## [1.17.6] - 2021-04-12
### Changed
- Handle multiple password reset requests from a same user
- Fix the disabled or deleted status of a password reset request

## [1.17.3] - 2021-04-12
### Changed
- Allow body message for HTTP request with HTTP methods other than POST and PUT

## [1.16.12] - 2021-04-12
### Changed
- Add a method to assert whether a password reset request exists and has not expired

## [1.16.9] - 2021-04-11
### Changed
- Support Cross-Origin Resource Sharing (CORS)

## [1.16.4] - 2021-04-08
### Changed
- Refactor the sign-in methods to return the contact information of the user
- Return the first name, last name, and contact information of the user who signs in

## [1.15.14] - 2021-04-04
### Added
- Add a method to return the list of teams that a user belongs to

## [1.15.11] - 2021-04-03
### Added
- Add methods to request the reset of a forgotten password

## [1.14.6] - 2021-03-31
### Added
- Add an option `is_name_unique` to the team creation method
- Remove the application ID from the creation of a team

## [1.14.3] - 2021-03-31
### Added
- Class `ArgumentObject` to easily parse JSON objects passed in the body message of HTTP request
- Reformat first name, last name, and full name when creating a new user account

## [1.13.3] - 2021-03-30
### Added
- Method to add a user to a team
- Method to hard- or soft-delete a user account
- Method to hard- or soft-delete a member from a team
- Method to upload the new logo image of a team
- Add visibility of team's contact information

### Changed
- Method to upload the picture of an account

## [1.12.2] - 2021-03-25
### Changed
- By default, allow a user to change his password 

## [1.12.1] - 2021-03-25
### Added
- Check conflicting argument values when creating a new user account
- Fix HTTP request argument list of objects parsing

## [1.12.0] - 2021-03-24
### Added
- Automatically generate a password when a user account is created without specifying a password
- Add an option to indicate whether user must change his password at the next login
- Add an option to indicate whether the user can change his password
- Add an option to indicate whether the password of the user never expires

## [1.11.9] - 2021-03-22
### Added
- Save the last login time of a user

## [1.11.8] - 2021-03-15
### Added
- Method to build the Uniform Resource Locator of a team's logo

### Changed
- Move teams' logos from CDN folder `team` to `logo`

## [1.11.7] - 2021-01-04
### Changed
- Change the default and maximum user login session duration (token lifetime)

## [1.11.6] - 2020-12-10
### Changed
- Fix argument `account_id` in function `NotificationServiceHttpHandler.register_device`

## [1.11.5] - 2020-12-10
### Changed
- Implement class `Object`'s method `__str__`

## [1.11.1] - 2020-12-10
### Changed
- Replace function `jsonify` with `stringify`

## [1.11.0] - 2020-10-16
### Changed
- Replace %xx escapes from the query string with their single-character equivalent to verify HTTP signature

## [1.0.0] - 2019-06-20
### Added
- Initial import
