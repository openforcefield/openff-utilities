# Release History

Releases follow versioning as described in
[PEP440](https://www.python.org/dev/peps/pep-0440/#final-releases), where

* `major` increments denote a change that may break API compatibility with previous `major` releases
* `minor` increments add features but do not break API compatibility
* `micro` increments represent bugfix releases or improvements in documentation

Dates are given in YYYY-MM-DD format.

Please note that all releases prior to a version 1.0.0 are considered pre-releases and many API changes will come before a stable release.

## Current development

### Breaking changes

* #108: Drop support for Python 3.10

## 0.1.14 - 2025-01-27

### New features

* #90: Add support for `pixi` when fetching package versions in virtual environments

### Maintenance changes

* #95: Test on Python 3.13
* #94: Consolidate Python config files

## 0.1.13 - 2024-12-02

### Breaking changes and behavior changes

* #92: Failures to call `conda` or similar executables now raise a warning (`CondaExecutableNotFoundWarning`) instead of an exception (`CondaExecutableNotFoundError`)
