# Yoficator

> A Russian text yoficator (ёфикатор).

## What does it do?

It conservatively replaces every `е` to `ё` when it's unambiguously a case of the latter. 
No context is used; it relies entirely on a lack of dictionary entries for a correspondent "truly `е`" homograph. 

Yoficating Russian texts removes some unnecessary ambiguities.

To learn more, check Wikipedia in [English](https://en.wikipedia.org/wiki/Yoficator) 
or [Russian](https://ru.wikipedia.org/wiki/Ёфикатор).

## Usage

1. Build wheel:
   ```sh
   python setup.py bdist_wheel -d '/tmp'
   ```
2. Install wheel:
   ```sh
   pip install yoficator-0.1.0-py2-none-any.whl
   ```
3. Use:
   ```sh
   python -m yoficator  # [text-file-in-Russian | string-in-Russian]
   ```

## Examples

Running the command without arguments parses the test file:

```sh
python -m yoficator
```

Or just use it with a file or string:

```sh
python -m yoficator russianfile.txt    # prints to STDOUT
python -m yoficator russianfile.txt > russianfile-yoficated.txt
python -m yoficator "Где ее книга?"
```

## Limitations

- The code being conservative and not looking for context, it won't correct when a "truly `е`" homograph exists.
  Thus a "`все`" will never be corrected, because both `все` and `всё` exist as different words.
- Prone to wrongly yoficate other Cyrillic-based languages, such as Bulgarian, Ukrainian, Belarussian.
- It's not the fastest thing in the world, mind you. But does the job.

## [Changelog](changelog.md)
## [License (GPL 3)](license.md)
