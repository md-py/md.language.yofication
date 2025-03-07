# md.language.yofication

md.language.yofication component provides a cyrillic text yofication (ёфикация) API and CLI application.

This is remastered version of [Yoficator](https://github.com/unabashed/yoficator) 
originally developed by unabashed.

---

**What does it do ?**

It conservatively replaces every `е` to `ё` when it's unambiguously a case of the latter. No context is used; 
it relies entirely on a lack of dictionary entries for a correspondent "truly `е`" homograph.

Yoficating Russian texts removes some unnecessary ambiguities.

To learn more, check Wikipedia in [English](https://en.wikipedia.org/wiki/Yoficator)
or [Russian](https://ru.wikipedia.org/wiki/Ёфикатор).

---

**Limitations:**

- The code being conservative and not looking for context, it won't correct when a "truly `е`" homograph exists. Thus,
  a "`все`" will never be corrected, because both `все` and `всё` exist as different words.
- Prone to wrongly yoficate other Cyrillic-based languages, such as Bulgarian, Ukrainian, Belarussian.

## Architecure overview

[![architecture overview class diagram](docs/_static/architecture-overview.class-diagram.svg)](docs/_static/architecture-overview.class-diagram.svg)

## Installation

```sh
pip install md.language.yofication --index https://source.md.land/python/
```

## Usage

CLI Application provides next options:

- `--no-replace` (DEFAULT) — disables original files modification. Modified content is being printed
  to standard output (STDOUT). Conflicts with `--replace` option. Makes no sense when few files arguments are specified. 
- `--replace` — enables original files modifications. Conflicts with `--no-replace` option.
  Makes no sense when no files arguments were specified.

For more details see program help:

```sh
python3 -m md.language.yofication -h
```

Operations with files:

1. Prints the modified text content to standard output (STDOUT) **without changing the file** 
   (the `--no-replace` option is the default).
   ```sh
   python3 -m md.language.yofication ./file.txt  # prints to STDOUT
   ```
2. Replaces specified file with yoficated content
   ```sh
   python3 -m md.language.yofication --replace ./file.txt  # replace in-place
   python3 -m md.language.yofication --replace ./file.txt ./file2.txt ./file3.txt  # replaces files
   find . -type f -iname '*.txt' -exec python3 -m md.language.yofication --replace {} \+  # replaces files
   ```

Operation standard input (STDIN):

1. Reads text from standard input (STDIN) and writes modified text to standard output (STDOUT).
   ```sh
   cat ./file.txt | python3 -m md.language.yofication  # reads from STDIN, prints to STDOUT
   echo "Где ее книга?" | python3 -m md.language.yofication
   python3 -m md.language.yofication <<< "Где ее книга?"
   ```
2. Interactive mode: 
   ```
   $ python3 -m md.language.yofication
   Где ее книга?
   Где её книга?
   ```

## [Documentation](docs/index.md)
## [Changelog](changelog.md)
## [License (MIT)](license.md)
