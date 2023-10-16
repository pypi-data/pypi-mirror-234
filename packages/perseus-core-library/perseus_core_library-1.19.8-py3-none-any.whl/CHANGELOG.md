# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [1.19.8] - 2023-10-08
### Fixed
- Constant `ANTIALIAS` was removed in Pillow 10.0.0, replaced with `LANCZOS`

## [1.19.7] - 2023-10-07
### Added
- Convert a string to a Version object

## [1.19.6] - 2023-10-03
### Fixed
- Patch a timestamp with time zone that would have been passed in a URL without encoding plus symbol

## [1.19.4] - 2023-07-27
### Changed
- Support E.123 notation for international telephone numbers

## [1.19.3] - 2023-06-14
### Fixed
- Fix the function `string_to_keywords` to filter keywords that are not composed of the minimal required number of characters

## [1.19.2] - 2023-04-04
### Added
- Add the functions `set_up_logger` and `get_console_handler` in the new module `majormode.perseus.utils.logging`

## [1.19.0] - 2023-02-08
### Added
- Move the class `ISO8601DateTime` to the new module `majormode.perseus.model.date`
- Add the class `Picture` in the new module `majormode.perseus.model.picture`

## [1.18.24] - 2022-11-28
### Added
- Add the method `cast_string_to_logging_level`

## [1.18.21] - 2022-11-23
### Added
- Add missing `pipfile` package

## [1.18.20] - 2022-11-09
### Changed
- Migrate from pipenv to Poetry
### Fixed
- Fix the the function `build_tree_file_path_name` that didn't include a path separation 

## [1.18.17] - 2022-08-03
### Added
- Add the function `string_to_natural_number` of the module `cast`
- Add regular expression that matches a natural number including zero

## [1.18.14] - 2022-04-30
### Added
- Add the module `setup_util`

## [1.18.13] - 2022-04-30
### Added
- Add the function `Version.from_file`

## [1.18.12] - 2022-04-29
### Added
- Add the function `macaddr_to_string` 

## [1.18.11] - 2021-08-08
### Added
- Allow passing an undefined username to class `ConnectionProperties`'s 
  constructor

## [1.18.9] - 2021-08-08
### Added
- Add class `ConnectionProperties`

## [1.18.7] - 2021-08-06
### Changed 
- Update the return type of the function `Locale.from_string`

## [1.18.6] - 2021-08-05
### Changed 
- Rename ISO-639 constants
- Add functions to validate country and language codes

## [1.18.5] - 2021-06-28
### Changed
- Fix an issue that occurs with specifying a language with a ISO 693-1 code

## [1.18.2] - 2021-06-27
### Added
- Add the list of ISO 693-2 codes for the representation of names of languages
- Add the list of ISO 693-3 codes for the representation of names of languages
- Add the list of ISO 3166-1 Alpha-2 codes for the representation of names of countries
- Verify the ISO 693-2/-3 code of a language when building a new locale object
- Verify the ISO 3166-1 Alpha-2 codes of a country when building a new locale object
### Changed
- Provide a descriptive message when raising the exception `Locale.MalformedLocaleException`

## [1.18.0] - 2021-06-27
### Changed
- Rename the class `Contact`'s attributes `name` and `value` with `property_name` and `property_values`

## [1.17.3] - 2021-06-15
### Added
- Add the module `zip_util`

## [1.17.2] - 2021-06-08
### Added
- Fix the function `string_to_enumeration` when the value is already an item of the enumeration

## [1.17.0] - 2021-06-07
### Added
- Remove base classes of agent classes

## [1.16.7] - 2021-05-28
### Added
- Add the enumeration `DevicePlatform`

## [1.16.6] - 2021-05-26
### Added
- Fix the User-Agent regular expression to match mobile device name including parentheses

## [1.16.5] - 2021-05-25
### Added
- Change the User-Agent regular expression to match fancy operating system version

## [1.16.4] - 2021-05-25
### Added
- Add enumeration `LoggingLevelLiteral`
- Add constant `LOGGING_LEVELS` that maps `LoggingLevelLiteral` items to `logging` values

## [1.16.3] - 2021-05-24
### Changed
- Update the function `string_to_keywords` to accept a list of strings

## [1.16.2] - 2021-05-20
### Changed
- Check if latitude and longitude are defined before objectifying the attributes of a location-like object

## [1.16.1] - 2021-04-27
### Added
- Add enumeration `NotificationMode`

## [1.16.0] - 2021-04-20
### Changed
- Remove email model and utilities

## [1.15.9] - 2021-04-20
### Added
- Add a method to check whether a string corresponds to a phone number
- Add a method to check whether a string corresponds to a username

## [1.15.8] - 2021-04-01
### Added
- Add a method to check whether a string corresponds to a phone number
- Add a method to check whether a string corresponds to a username

## [1.15.5] - 2021-04-01
### Added
- Set default values for contact attributes `is_primary`, `is_verified`, and `visibility`

## [1.15.4] - 2021-03-11
### Added
- Add the class `WeightedGeoPointCluster`

## [1.15.3] - 2020-12-12
### Added
- Add method `__str__` to class `Object`

## [1.2.0] - 2019-06-17
### Added
- Remove unsupported Python 2.7 library `statvfs`.

## [1.0.0] - 2019-06-16
### Added
Initial import.
