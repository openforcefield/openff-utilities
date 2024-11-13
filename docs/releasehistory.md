# Release History

Releases follow versioning as described in
[PEP440](https://www.python.org/dev/peps/pep-0440/#final-releases), where

* `major` increments denote a change that may break API compatibility with previous `major` releases
* `minor` increments add features but do not break API compatibility
* `micro` increments represent bugfix releases or improvements in documentation

Dates are given in YYYY-MM-DD format.

Please note that all releases prior to a version 1.0.0 are considered pre-releases and many API changes will come before a stable release.

## Current development

### Breaking changes and behavior changes

* Failures to call `conda` or similar executables now raise a warning (`CondaExecutableNotFoundWarning`) instead of an exception (`CondaExecutableNotFoundError`)