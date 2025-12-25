import os.path
import sys
import argparse
import typing
import concurrent.futures


import md.language.yofication

__all__ = (
    'ApplicationEchoLines',
    'ApplicationReplaceLines',
    'create_cli_parser',
    'main',
)


class ApplicationEchoLines:
    def __init__(self, yoficate: md.language.yofication.YoficateInterface) -> None:
        self._yoficate = yoficate

    def run(self, input_stream: typing.IO[str]) -> None:
        try:
            for line in iter(input_stream):
                print(self._yoficate.text(text=line.rstrip('\n')))
        except (KeyboardInterrupt, EOFError):
            pass


class ApplicationReplaceLines:
    def __init__(self, yoficate: md.language.yofication.YoficateInterface) -> None:
        self._yoficate = yoficate

    def run(self, file_path_list: typing.List[str]) -> None:
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            for file_path in file_path_list:
                executor.submit(self._replace_file, file_path=file_path)

    def _replace_file(self, file_path: str) -> None:
        directory, filename = os.path.split(file_path)

        with open(file_path) as source_stream, open(f'{directory}/.tmp.{filename}', 'w') as destination_stream:
            for line in source_stream:
                destination_stream.write(self._yoficate.text(text=line))

        os.rename(file_path, f'{directory}/{filename}.bak.before-yofication')
        os.rename(f'{directory}/.tmp.{filename}', file_path)
        os.remove(f'{directory}/{filename}.bak.before-yofication')


def create_cli_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog='md.language.yofication',
        description='Yofication program replaces cyrillic letter "е" with letter "ё" in word where it should be.',
    )
    parser.add_argument('file_path', nargs='*', help='file to yoficate')

    # dictionary_group = parser.add_mutually_exclusive_group()
    # dictionary_group.add_argument('--locale', action='store', choices=['ru_RU'], default='ru_RU')
    # dictionary_group.add_argument('--dictionary', action='store', default=None)

    replace_group = parser.add_mutually_exclusive_group()
    replace_group.add_argument(
        '--replace',
        action='store_true',
        default=False,
        help='Replaces files with yoficated content'
    )
    replace_group.add_argument(
        '--no-replace',
        action='store_true',
        default=True,
        help=(
            'DEFAULT: Prints yoficated file content instead of replace. '
            'Exits with error, if few `file_path` arguments passed.'
        )
    )
    return parser


def main(arguments: typing.Sequence[str]) -> int:
    # | FILES | REPLACE | RESULT            |
    # |-------|---------|-------------------|
    # | =0    | 0       | OK (STDIN/STDOUT) |
    # | =0    | 1       | ERROR             |
    # | =1    | 0       | OK (STDOUT)       |
    # | =1    | 1       | OK (REPLACE)      |
    # | >1    | 0       | ERROR             |
    # | >1    | 1       | OK (REPLACE)      |

    parser = create_cli_parser()
    parsed_arguments = parser.parse_args(arguments)
    locale: typing.Literal['ru_RU'] = 'ru_RU'  # todo add support in further versions

    file_path_count = len(parsed_arguments.file_path)

    # validate
    if parsed_arguments.replace:
        if file_path_count == 0:
            print('Error: no files specified to replace', file=sys.stderr)
            return 1
    else:
        if file_path_count > 1:
            print('Error: using `--no-replace` option with many files makes no sense', file=sys.stderr)
            return 1

    # act
    builtin_dictionary = md.language.yofication.get_builtin_dictionary(locale=locale)
    yoficate = md.language.yofication.DefaultYoficate(dictionary=builtin_dictionary)

    if not parsed_arguments.replace:
        # todo consider to separate to `--interactive/-i` and `-`$
        application: ApplicationEchoLines = ApplicationEchoLines(yoficate=yoficate)
        if file_path_count == 0:
            application.run(input_stream=sys.stdin)
            return 0

        assert file_path_count == 1
        with open(parsed_arguments.file_path[0], 'r') as stream:
            application.run(input_stream=stream)
        return 0

    assert parsed_arguments.replace and file_path_count >= 1
    application: ApplicationReplaceLines = ApplicationReplaceLines(yoficate=yoficate)  # type: ignore[no-redef]
    application.run(file_path_list=parsed_arguments.file_path)  # type: ignore[call-arg]
    return 0


if __name__ == '__main__':
    exit_code = main(sys.argv[1:])
    exit(exit_code)
