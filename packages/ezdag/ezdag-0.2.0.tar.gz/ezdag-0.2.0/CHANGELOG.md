# Changelog

## [Unreleased]

## [0.2.0] - 2023-10-06

### Added

- Allow users to give submit description options using native Python
  types rather than understanding the correct formatting for each option
- Allow executables not found in PATH

### Changed

- Change requirements option to submit_description in Layer, keeping
  old option for backwards compatibility with a deprecation warning
- Allow customizable node name formatting from DAG
- Change default node name separator to avoid issues with common executable
  delimiters

### Removed

- Remove dynamic_memory option in Layer, as it had many implicit assumptions
  which are particularly brittle
- Remove periodic_release default in Layer

### Fixed

- Ensure node input/outputs are consistent for nodes upon Layer instantiation
- Avoid overwriting submit descriptors in Layer

## [0.1.0] - 2023-01-25

- Initial release.

[unreleased]: https://git.ligo.org/patrick.godwin/ezdag/-/compare/v0.1.0...main
[0.1.0]: https://git.ligo.org/patrick.godwin/ezdag/-/tags/v0.1.0
