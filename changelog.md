# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

- [ ] feature: implement r/w stream edit using reading by chunks instead of by lines 
- [ ] enhancement: change dictionary format: better compress
- [ ] feature: extend dictionary: add more words, handle separately lower/upper-cased specific words
- [ ] feature: add lint option
- [ ] feature: add replacement stats

## [0.1.1] — 2025-03-02
### Fixed

- fix: dictionary word lookup for party yoficated words, e.g. `четырЕхзвЁздный`, `четырЁхзвЕздный`

## [0.1.0] — 2025-02-16

`md.language.yofication` package initial version

# Archived versions

<details><summary>archived "yoficator" package versions</summary>

## 0.1.7 — 2025-02-15
### Changed

- [x] replace dictionary file with bz2-archived version (decrease file size in 8.1 times)

## 0.1.6 — 2025-02-15
### Changed

- [x] optimize regexp pattern

## 0.1.5 — 2025-02-15
### Changed

- [x] refactoring: dictionary file renamed: `yoficator/_data/yoficator.dic` to `yoficator/_data/dictionary.ru_RU.txt`

## 0.1.4 — 2025-02-15
### Changed

- [x] upgrade to python3

## 0.1.3 — 2025-02-15
### Removed

- [x] refuse from `regex` as dependency in favor of standard `re`

## 0.1.2 — 2025-02-15
### Removed

- [x] remove unused `pprint` statement

## 0.1.1 — 2025-02-15
### Removed

- [x] remove "tests" (demo) functionality

## 0.1.0 — 2025-02-15
### Added

- [x] added `changelog`, `license` files

### Changed

- [x] refactoring: project directory structure changed, added `setup.py` file for packaging

## Unversioned — 2015-11-17

Initial release

</details>

[0.1.1]: https://github.com/md-py/md.language.yofication/releases/tag/0.1.1
[0.1.0]: https://github.com/md-py/md.language.yofication/releases/tag/0.1.0
