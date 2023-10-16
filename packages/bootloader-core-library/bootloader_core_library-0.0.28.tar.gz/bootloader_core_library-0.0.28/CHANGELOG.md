# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), 
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.27] - 2023-09-08
### Added
- Add Unity core classes enumeration

## [0.0.27] - 2023-09-07
### Added
- The properties `asset_class` and `asset_class_name` to the Unity `Asset` class

## [0.0.26] - 2023-09-07
### Fixed
- The core attribute of an asset are immutable

## [0.0.25] - 2023-09-07
### Fixed
- Rename the attributes `file_checksum` and `file_size` with  `data_checksum` and `data_size`

## [0.0.24] - 2023-09-06
### Changed
- Change the library packages structure

## [0.0.15] - 2023-08-03
### Added
- Add the method `has_standard_class` to the class `UnrealEngineAsset`

## [0.0.12] - 2023-08-03
### Added
- Warn when an Unreal Engine class is not mapped with a humanly readable name (cf. enumeration `UnrealEngineAssetClass`)

## [0.0.11] - 2023-08-02
### Fixed
- Add setters to the class `UnrealEngineRecordAssetFile`

## [0.0.9] - 2023-08-02
### Fixed
- Add missing attribute `asset_id` in the JSON serialization

## [0.0.8] - 2023-08-02
### Fixed
- Fix the method `to_json` to include the complete list of the asset's attributes

## [0.0.7] - 2023-08-02
### Added
- Add the method `__str__` to stringify the representation of an asset or an asset file

## [0.0.6] - 2023-08-02
### Added
- Add the properties `object_status`, `references`, `tags`, `update_time`, and `version_code`

## [0.0.5] - 2023-08-02
### Added
- Allow the properties `asset_name` and `package_name` to be updated

## [0.0.4] - 2023-08-02
### Fixed
- Fix the property `asset` of the class `UnrealEngineAbstractAssetFile`

## [0.0.3] - 2023-08-02
### Changed
- Update Unreal Engine classes to support both asset's database record and file system

## [0.0.2] - 2023-08-02
### Changed
- Update both Unreal Engine class and class enumeration

## [0.0.1] - 2023-08-01
### Added
- Initial import
