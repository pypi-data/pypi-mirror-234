# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [v0.0.5] - 2023-10-11
### Added
- End-to-end tests for the CLI command
- `version` command
- Better request dumping in debug mode

### Fixed
- Requests to API endpoints that don't expect a request payload
- Updated Python build system to use pyproject.toml
- Changed linter from Flake8 to Black
- Use `isort`

### Added

- Support for DELETE requests
- Workflow to run tests on PR triggers
- Support for Annotations API
- Support for Events API
- Support for `developer` version

### Fixed

- Pinned flake8 to a version that works with pytest-flake8

## [v0.0.4] - 2022-05-04

### Added

- Support for object pagination in SET/UPDATE requests

## [v0.0.3] - 2021-04-21

### Added

- Tests (lint and rudimentary doctest)
- Travis support
- More doc
- PR template

### Fixed

- Release-support code
- Bugs due to incorrect merge conflict resolution impacting all but api-data

## [v0.0.2] - 2021-04-20

- New PyPI release including actual code...

## [v0.0.1] - 2021-04-20
### Added

- This ChangeLog!
- lrn-cli: Support for api-author, api-items, api-questions and api-reports
- lrn-cli: Support for usrequest
- lrn-cli command
