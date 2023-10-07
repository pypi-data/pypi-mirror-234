# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html)[^1].

<!---
Types of changes

- Added for new features.
- Changed for changes in existing functionality.
- Deprecated for soon-to-be removed features.
- Removed for now removed features.
- Fixed for any bug fixes.
- Security in case of vulnerabilities.

-->

## [2.1.1] - 2023-10-06

### Fixed

* User Tasks: libreflow bookmarks now works according with kitsu episodes

## [2.1.0] - 2023-09-19

### Added

* A hidden parameter to actions for creating films, sequences and shots from Kitsu to filter theses entities by name.
* Two options to the `CreateKitsuFilms` action to create shots and sequences in the created episodes.
* Added the new asset level in the librairies
* Code and display names for specic naming conventions of Andarta
* New backend script for handle installation and updates of Libreflow
* Default dialog size for Import Files

### Changed

* User tasks can now handle episodes and is updated to the new flow
* Versioneer has been updated to 0.28, fixing the version number issues making the install anoying at Andarta
* UI elements in the main project page
* Readme to match new steps for install
* Import Files handle the new asset level

### Fixed

* Upload to Kitsu and create film/sequences/shots now allows to use TVShows kitsu projects
* Get episodes in Kitsu with sufixes in names
* Create assets in the updated lib from Kitsu
* User Tasks: Fallback to the old URL for Kitsu My Tasks page

## [2.0.0] - 2023-07-24

Define a flow up and ready to use.
