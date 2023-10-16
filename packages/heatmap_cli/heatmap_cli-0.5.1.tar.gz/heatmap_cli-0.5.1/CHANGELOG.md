# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [0-based versioning](https://0ver.org/).

## [Unreleased]

## v0.5.1 (2023-10-08)

### Added

- Support Python 3.12.0

### Fixed

- Fix total number of heatmap not showing

## v0.5.0 (2023-10-01)

### Added

- Add `-a` or `--annotate` flag to add count to each heatmap region
- Add `-q` or `--quiet` flag to suppress logging
- Add `flake8-print` and `flake8-simplify` for `pre-commit` check
- Add `heatmap` as alias to `heatmap_cli`

### Changed

- Refactor annotated count calculation
- Set annotated font size to 8 to better readability

## v0.4.5 (2023-09-24)

### Fixed

- Add missing `flake8` related deps in dev environment

### Changed

- Allow to generate number of heatmaps by setting `--demo` option
- Filter log record from subprocess by default (`debug` flag is disabled)
- Shorten the logging message when generating PNG file to fit screen width
- Sort test coverage report by coverage percentage

## v0.4.4 (2023-09-17)

### Fixed

- Fix logging not working in child process by switching pooling method from
  spawn to fork
- Suppress `nargs` incompatible type warning

## v0.4.3 (2023-09-11)

### Fixed

- Fix incorrect log format

## v0.4.2 (2023-09-10)

### Changed

- Refactor setting default CSV filename for `--demo` flag

### Fixed

- Use correct `pyenv` wording in contributing doc
- Fix logging not using the config from command line flag

## v0.4.1 (2023-09-03)

### Added

- Optimize heatmaps generation using pooling
- Use generated sample CSV file upon `--demo` flag

### Changed

- Prepend sequence number to output PNG filename
- Refactor colormaps initialization
- Show all colormaps in help message upon `-v`, or `--verbose` flag
- Switch `pytest-console-script` to `scripttest` due to failure to capture
  worker logs

### Fixed

- Ignore default `output` folder

## v0.4.0 (2023-08-27)

### Added

- Add `-dm` or `--demo` flag to generate all heatmaps by colormap
- Add `-od` or `--output-dir` option to set a default output folder for
  generated heatmaps

### Changed

- Bump Python versions for `pyenv`
- Changelog url should comes before issue url

### Fixed

- Fix two underscores in PNG filename

## v0.3.2 (2023-08-20)

### Changed

- Generate multiple heatmaps at once by different colormaps through `-cm`
  option

## v0.3.1 (2023-08-13)

### Changed

- Add logging for `-wk` related usages
- Sort URLs in project config

### Fixed

- Fix incorrect changelog URL
- Fix title without proper spacing

## v0.3.0 (2023-08-06)

### Added

- Add additional default hook for `pre-commit`
- Add `-cm` or `--cmap` option to set a default colormap

### Changed

- Rename test files based on the right term
- Add missing tests for `-wk` option

### Fixed

- Fix incorrect coverage configs
- Fix incorrect changelog URL

## v0.2.2 (2023-07-30)

### Added

- Add changelog URL to help message
- Add missing documentation for functions

### Changed

- Set title and PNG filename to year only when week is set to 52
- Reset DataFrame index after the last filtering step
- Move some coverage configs to `tox.ini` file

### Fixed

- Fix incorrect header level in changelog
- Fix incorrect source module in coverage config file

## v0.2.1 (2023-07-28)

### Changed

- Move `coverage` config from `tox` to its own file
- Reset DataFrame index after filtering

### Fixed

- Show verbose log of last date of current week
- Fix incorrect header level in changelog

## v0.2.0 (2023-07-23)

### Added

- Add `yr` or `--year` argument to filter CSV data by year
- Add `wk` or `--week` argument to filter CSV data until week of the year
- Add additional pre-commit default checks
- Show generated PNG filename upon completion

### Changed

- Group all `sphinx` related deps under the `doc` category
- Standardize `tox` environment names

### Fixed

- Fix incorrect ignored coverage module
- Suppress logging from `matplotlib` in `debug` mode

## v0.1.3 (2023-07-16)

### Fixed

- Fix missing `pylint` dependency when running `pre-commit`
- Ignore word when running `codespell` pre-commit hook

## v0.1.2 (2023-07-11)

### Changed

- Link to license from contributing doc
- Use the same output folder for `sphinx` doc generation
- Revise `pyenv` installation with plugins in contributing doc
- Install `heatmap_cli` as editable installation in `pipenv` dev env

## v0.1.1 (2023-07-09)

### Fixed

- Fix missing dependencies on `pipx` installation
- Fix incorrect module name in `pre-commit` hooks

## v0.1.0 (2023-07-08)

### Added

- Initial public release
