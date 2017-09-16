# Change Log
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [Unreleased]

## [0.1.8] - 2017-09-16
### Added
- tools/json_update.py
- helpers/common.py

### Changed
- Refactor all project typos
- Project structure cleanup

## [0.1.7] - 2017-06-24
### Added
- Script argument parser and help menu
- Local Pciid json used on connection timeout to pci-ids.ucw.cz
- Moved main script functions to helpers/kext_reader.py

### Changed
- Updated README.md documentation
- Fixed alphanumeric sorting

## [0.1.6] - 2017-06-21
### Changed
- Output for macOS 10.12.6 beta4 (16G18a)
- Pciid DB error handling 

## [0.1.5] - 2017-06-15
### Changed
- All pci id values stored as integers

## [0.1.4] - 2017-06-14
### Fixed
- Duplicates pciid's in output

### Changed
- Output for macOS 10.12.6 beta3 (16G16b)

## [0.1.3] - 2017-06-06
### Fixed
- Use sort function for consistent name ordering of kexts in output

## [0.1.2] - 2017-05-21
### Added
- Report AMDLegacySupport.kext plist

## [0.1.1] - 2017-05-20
### Added
- CHANGELOG.md and version numbers
- Moved output example to output.md

### Changed
- sysout is now in markdown format

## [0.1.0] - 2017-05-17
- Initial realease
