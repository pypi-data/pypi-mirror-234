# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project attempts to adhere to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
### Fixed
### Changed
### Removed

## [0.5.4] - 2023-10-10
### Fixed
- Catch empty files in ImgDownloader.is_image. (#177)

## [0.5.3] - 2023-10-08
### Added
- order --timeout option. (#174)
### Fixed
- SD Login button finder. (#176)
### Changed
- Use ruff for lint testing. (#173)
### Removed

## [0.5.2] - 2023-09-30
### Added
### Fixed
### Changed
### Removed
- "Confirmed" column from `sheet-image` XLSX files. (#169)

## [0.5.1] - 2023-09-29
### Added
### Fixed
### Changed
- Migrated documentation from README to docs. (#167)
### Removed

## [0.5.0] - 2023-09-27
### Added
### Fixed
### Changed
- **BREAKING**: Change CLI to support command chaining. (#140)
### Removed

## [0.4.1] - 2023-09-26
### Added
- CONFIG: [asg.spreadsheet.mkthumbs] fields to enable user adjustment. (#95)
- CONFIG: [asg.spreadsheet.sheet_image] fields to enable user adjustment. (#95)
- CONFIG: [asg.scraper.headless] field to enable headless scraper. (#159)
- CI: Deploy stage to create gitlab pages. (#158)
### Fixed
- SlideGenerator: Fix bucket_prefix for generated image files on Windows. (#164)
- SlideGenerator: Fix creating `test_bucket_prefix` directory in path of execution. (#164)
- CONFIG: Deep merge of CFG when loading configuration file from disk.
- README: Updated for v0.4.0. (#158)
- Mkthumbs: enabled `artemis_logo.png` to be included in package builds. (#160)
### Changed
### Removed

## [0.4.0] - 2023-09-23
### Added
- Support for Excel WORKBOOK/WORKSHEET to `artemis_sg scrape`. (#137)
- Support for Excel WORKBOOK/WORKSHEET to `artemis_sg generate`. (#137)
### Fixed
- Refactored pytest fixtures into conftest.py.
- Refactored mock.side_effect instances into mock.return_values.
### Changed
- **BREAKING**: Move vendor data storage from `vendors.json` to `config.toml`. (#152)
- **BREAKING**: Make `--worksheet` an optional argument for `artemis_sg scrape`. (#139)
- **BREAKING**: Make `--worksheet` an optional argument for `artemis_sg generate`. (#139)
- Replace usage of `imghdr` library with `puremagic`. (#103)
- **BREAKING**: Make `--worksheet` an optional argument for `artemis_sg sheet-image`. (#138)
- **BREAKING**: Make `--worksheet` an optional argument for `artemis_sg order`. (#138)
### Removed
- Support for `vendors.json`. (#152)

## [0.3.0] - 2023-09-19
### Added
### Fixed
### Changed
- **BREAKING**: Move configuration to `$user_config_dir/config.toml`. (#151)
- Set configuration files to be in `user_config_dir`. (#142)
- Set data files to be in `user_data_dir`. (#142)
- Changed module name from `artemis_slide_generator` to `artemis_sg`. (#147)
### Removed

## [0.2.5] - 2023-09-14

### Added
- Support in `pyproject.toml` for package build and publish via `hatch`. (#143)
- `Spreadsheet.sheet_image()`: Dynamically set column width with a max of about 500px. (#95)
- Docstrings to `app_creds.py`. (#89,#104)
- Documentation for installing via PowerShell. (#136)

### Fixed
- `ImgDownloader.download()`: No longer hard-coded to '.jpg'.  Handle all file
  types. The Windows `PermissionError: [WinError 32]` has been addressed. (#14)
- Test `cli.mkthumbs`:  Correct image-directory assumption.
- Test `cli.sheet_image`: Fix path for Windows.
- Test: Close test db fixture file to prevent `PermissionError: [WinError 32]`
  on Windows.

### Changed
- Project name for builds to `artemis_sg`. (#143)
- Appended `namespace` variables to logging messages. (#88)

### Removed


## [0.2.4] - 2023-08-24

### Fixed
- `sheet_image`: `isbn` values are coerced to integers if they come in as
  floating point numbers (#101).

## [0.2.3] - 2023-08-23

### Fixed
- `sheet-image`: `isbn_key` and `row01` values are upper-cased before compare
  (#90).

## [0.2.2] - 2023-08-23

### Removed
- Reverted: `ImgDownloader.download()`: No longer hard-coded to '.jpg'.  Handle
  all file types. (#14)
  - This triggered `PermissionError: [WinError 32]` on Windows.

## [0.2.1] - 2023-08-21

### Added
- CLI: `--email` option to the `order` sub-command.  This is used to
  impersonate customers for the 'tb' vendor (#70).
- Use "TBCODE" for item if no "ISBN" (#5).

### Fixed
- Docs: `sheet-image` examples using the `--output` option have been amended
  for clarity (#37).
- Tests: Fixed slow scraper tests (#83).
- Tests: Enable app_creds tests (#84).
- Linting errors.
- `mkthumbs`: Support any filename (#64).
- `ImgDownloader.download()`: No longer hard-coded to '.jpg'.  Handle all file
  types. (#14)

### Changed
- `sheet_image`: Create "Confirmed" column to the right of the "Order" column
  of generated spreadsheet (#34).
- `sheet_image`: Copy cell format from "ISBN_KEY" header cell to the header
  cells of created columns (#75).
- Refactor `gcloud.upload()` out of `gcloud.main()` (#47).
- Spreadsheet: Use variable for namespace in log messages.

### Removed
- `GCLoud`: replace `PIL` with `imghdr` for image file validation.

## [0.2.0] - 2023-08-16

### Added
- CHANGELOG
- Unit test for `Spreadsheet.sheet-image()` (#28).
- Unit test for `BLACKLIST_KEYS` in `SlideGenerator` (#25).
- For `GJScraper.load_login_page`, load search page first in an attempt to cache Publishers.
- CLI: `artemis_sg order [OPTIONS] VENDOR WORKBOOK WORKSHEET` command to construct web orders.
  - Valid vendor codes are: "tb", "gj", and "sd".
  - Scraper: for the above vendor scrapers, the following methods were added:
    - `load_login_page()`
    - `login()`
    - `add_to_cart()`
    - `load_cart_page()`

### Fixed
- Linting errors.

### Changed
- Internally, use search page for `GJScraper.load_item_page()` when logged in (#58).
- Scraper: `load_item_page()` methods now return a boolean.
- Update formatting of GitLab issue template.

### Removed

## [0.1.5] - 2023-08-11

### Added
- Output examples to `sheet-image` documentation in README (#37).
- GitLab issue templates (#62).

### Fixed
- `mkthumbs`: Ignore image files without basename (e.g. ".jpg") (#59).

### Changed
- Move ISBN validation into `ImageDownloader` class (#53).
- Allow non-ISBN values in `ImageDownloader` (#53), `mkthumbs` (#54), `sheet-image` (#60).

### Removed
- Use of webdriver-manager (#50).

## [0.1.4] - 2023-07-28

### Fixed
- Catch `TimeoutException` in `SDScraper.load_item_page()` (#38).

### Removed
- `TODO.md` in favor of tracking work via
   [GitLab issues](https://gitlab.com/johnduarte/artemis_slide_generator/-/issues)

## [0.1.3] - 2023-07-23

### Added
- `GJScraper` class with custom implementations of `BaseScraper` methods (#4).
- Failover to `GJScraper` in `scraper.main()` when vendor is "gj".

### Fixed
- Catch `UnidentifiedImageError` in `Spreadsheet.mkthumbs()` (#43).

## [0.1.2] - 2023-07-23

### Added
- `SDScraper` class with custom implementations of `BaseScraper` methods (#38).
- Failover to `SDScraper` in `scraper.main()` when vendor is "sd".

### Fixed
- Missing `ASG_VENDOR_DATAFILE` definition within `.env` in README (#36).
- Uppercase `isbn_key` when read from `ASG_VENDOR_DATAFILE` to ensure it is in
  the same state as the keys defined in `Item` (#39).

## [0.1.1] - 2023-07-21

### Added
- ISBN as plain text to generated slides (#9).

## [0.1.0] - 2023-07-11

### Changed
- **BREAKING**: CLI commands `scrape`, `generate` now take requiered SHEET_ID and SHEET_TAB arguments.
- **BREAKING**: Convert `database.json` to `vendors.json` and change the data structure.
- **BREAKING**: Use `.env` to define `ASG_VENDOR_DATAFILE`.
- Update documentation for changes above.

## [0.0.2] - 2023-07-18

### Added
- Mandatory VENDOR CLI argument for `sheet-image` command.
- Make `ImgDownloader.download()` idempotent in order to not re-download images.
- Have `Slidegenerator` clean up the text images created during run.
- `BaseScraper.delay()` to allow tuning sleep calls for scraper operations.

### Fixed
- `vendor` import in `spreadsheet.py`.
- Catch invalid ISBN values in `spreadsheet.sheet_image()`.
- Catch exception if TB item data does not contain "LINK" data.
- `TBScraper` indentation error that prevented image URLs from being appended as expected.

### Changed
- Create only one Google API token for project rather than one per vendor.
- Default slide title is now set to "New Arrivals".
- Default `sheet-image` output file set to "out.xlsx".
- Refactoring of `slide_generator.py`.

### Removed
- CLI options for `scrape` and `generate`: `--vendor-database`, `--scraped-items-database`.
- CLI options for `sheet-image`: `--image-directory`.


## [0.0.1] - 2023-07-10

### Added
- CLI interface with the following commands:
  - `artemis_sg scrape`
  - `artemis_sg download`
  - `artemis_sg upload`
  - `artemis_sg generate`
  - `artemis_sg sheet_image`
  - `artemis_sg mkthumbs`
- Documentation via README.
- Object oriented structure to code-base.
- LICENSE for GPL-3.0 or later.

### Removed
- Script interface for slide generation.

[unreleased]: https://gitlab.com/johnduarte/artemis_slide_generator/compare/v0.5.4....main
[0.5.4]: https://gitlab.com/johnduarte/artemis_slide_generator/compare/v0.5.3...v0.5.4
[0.5.3]: https://gitlab.com/johnduarte/artemis_slide_generator/compare/v0.5.2...v0.5.3
[0.5.2]: https://gitlab.com/johnduarte/artemis_slide_generator/compare/v0.5.1...v0.5.2
[0.5.1]: https://gitlab.com/johnduarte/artemis_slide_generator/compare/v0.5.0...v0.5.1
[0.5.0]: https://gitlab.com/johnduarte/artemis_slide_generator/compare/v0.4.1...v0.5.0
[0.4.1]: https://gitlab.com/johnduarte/artemis_slide_generator/compare/v0.4.0...v0.4.1
[0.4.0]: https://gitlab.com/johnduarte/artemis_slide_generator/compare/v0.3.0...v0.4.0
[0.3.0]: https://gitlab.com/johnduarte/artemis_slide_generator/compare/v0.2.5...v0.3.0
[0.2.5]: https://gitlab.com/johnduarte/artemis_slide_generator/compare/v0.2.4...v0.2.5
[0.2.4]: https://gitlab.com/johnduarte/artemis_slide_generator/compare/v0.2.3...v0.2.4
[0.2.3]: https://gitlab.com/johnduarte/artemis_slide_generator/compare/v0.2.2...v0.2.3
[0.2.2]: https://gitlab.com/johnduarte/artemis_slide_generator/compare/v0.2.1...v0.2.2
[0.2.1]: https://gitlab.com/johnduarte/artemis_slide_generator/compare/v0.2.0...v0.2.1
[0.2.0]: https://gitlab.com/johnduarte/artemis_slide_generator/compare/v0.1.5...v0.2.0
[0.1.5]: https://gitlab.com/johnduarte/artemis_slide_generator/compare/v0.1.4...v0.1.5
[0.1.4]: https://gitlab.com/johnduarte/artemis_slide_generator/compare/v0.1.3...v0.1.4
[0.1.3]: https://gitlab.com/johnduarte/artemis_slide_generator/compare/v0.1.2...v0.1.3
[0.1.2]: https://gitlab.com/johnduarte/artemis_slide_generator/compare/v0.1.1...v0.1.2
[0.1.1]: https://gitlab.com/johnduarte/artemis_slide_generator/compare/v0.1.0...v0.1.1
[0.1.0]: https://gitlab.com/johnduarte/artemis_slide_generator/compare/v0.0.2...v0.1.0
[0.0.2]: https://gitlab.com/johnduarte/artemis_slide_generator/compare/v0.0.1...v0.0.2
[0.0.1]: https://gitlab.com/johnduarte/artemis_slide_generator/-/tags/v0.0.1
