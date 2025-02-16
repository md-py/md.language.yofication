#!/usr/bin/env python3
import os.path
import re
import typing

# Metadata
__author__ = 'https://md.land/md'
__version__ = '0.1.0'
__all__ = (
    # Metadata
    '__author__',
    '__version__',
    # Type
    'DictionaryType',
    # Contract
    'LoadDictionaryInterface',
    'DictionaryInterface',
    'YoficateInterface',
    # Implementation
    'BytesStreamLoadDictionary',
    'TextFileLoadDictionary',
    'Bz2TextFileLoadDictionary',
    'MappingDictionary',
    'RegularExpressionYoficate',
    'DefaultYoficate',
    # functions
    'get_builtin_dictionary',
)

# Type
DictionaryType = typing.Mapping[str, str]


# Contract
class LoadDictionaryInterface:
    def load(self, file_path: str) -> DictionaryType:
        raise NotImplementedError

    def supports(self, file_path: str) -> bool:
        raise NotImplementedError


class DictionaryInterface:
    """ Generalizes search logic from concrete associative mapping implementation """
    def find(self, word: str) -> typing.Optional[str]:
        """
        Returns yoficated word in lowercase if found, None otherwise.
        Warning: word argument value is case-sensitive "
        """
        raise NotImplementedError

    def has(self, word: str) -> bool:
        """
        Returns True, if word could be yoficated. False otherwise.
        Warning: word argument value is case-sensitive
        """
        raise NotImplementedError


class YoficateInterface:
    def text(self, text: str) -> str:
        """ Performs words yofication in text """
        raise NotImplementedError

    def word(self, word: str) -> str:
        """ Performs words yofication in text """
        raise NotImplementedError


# Implementation
class BytesStreamLoadDictionary:
    # format = ColonSeparatedRelation
    def load(self, stream: typing.IO[bytes], encoding: str = 'utf-8') -> DictionaryType:
        dictionary: typing.Dict[str, str] = {}

        for line in iter(stream):
            key, value = line.decode(encoding).rstrip('\n').lower().split(':', 1)
            assert len(key) == len(value), f'replacement is not identical: `{key}` -> `{value}`'
            dictionary[key] = value

        return dictionary


class TextFileLoadDictionary(LoadDictionaryInterface):
    def __init__(self, bytes_stream_load_dictionary: BytesStreamLoadDictionary) -> None:
        self._bytes_stream_load_dictionary = bytes_stream_load_dictionary

    def load(self, file_path: str) -> DictionaryType:
        if not self.supports(file_path):
            raise RuntimeError('File is not supported for loading')

        with open(file_path, 'rb') as stream:
            return self._bytes_stream_load_dictionary.load(stream=stream)

    def supports(self, file_path: str) -> bool:
        return file_path.lower().endswith('.txt')


class Bz2TextFileLoadDictionary(LoadDictionaryInterface):
    def __init__(self, bytes_stream_load_dictionary: BytesStreamLoadDictionary) -> None:
        import bz2
        self._bz2 = bz2
        self._bytes_stream_load_dictionary = bytes_stream_load_dictionary

    def load(self, file_path: str) -> DictionaryType:
        if not self.supports(file_path):
            raise RuntimeError('File is not supported for loading')

        with self._bz2.open(file_path) as stream:
            return self._bytes_stream_load_dictionary.load(stream=stream)

    def supports(self, file_path: str) -> bool:
        return file_path.lower().endswith('.txt.bz2')


class MappingDictionary(DictionaryInterface):
    def __init__(self, dictionary: DictionaryType) -> None:
        self._dictionary = {}
        for ye_word, yo_word in dictionary.items():
            self._dictionary[ye_word.lower()] = yo_word.lower()

    def find(self, word: str) -> typing.Optional[str]:
        return self._dictionary.get(word, None)

    def has(self, word: str) -> bool:
        return word in self._dictionary


class RegularExpressionYoficate(YoficateInterface):
    def __init__(self, dictionary: DictionaryInterface) -> None:
        self._dictionary = dictionary
        self._e_word_regexp = re.compile('([а-я]*е[а-я]*)', re.IGNORECASE)

    def text(self, text: str) -> str:
        return self._e_word_regexp.sub(lambda e_word_match: self.word(word=e_word_match.group(0)), text)

    def word(self, word: str) -> str:
        yo_word = self._dictionary.find(word=word.lower())
        if yo_word is None:
            return word

        assert len(word) == len(yo_word), (
            f'Dictionary has malformed word for `{word}`. Replacement must have same length'
        )

        # copy case
        yo_word_sequence = list(yo_word)
        for i, e_word_letter in enumerate(word):
            if e_word_letter.isupper():
                yo_word_sequence[i] = yo_word_sequence[i].upper()
        return ''.join(yo_word_sequence)


DefaultYoficate = RegularExpressionYoficate

# functions
_builtin_dictionary: typing.Optional[MappingDictionary] = None
def get_builtin_dictionary(locale: typing.Literal['ru_RU'] = 'ru_RU') -> MappingDictionary:
    """ Returns built-in yoficate dictionary """
    global _builtin_dictionary
    if _builtin_dictionary:
        return _builtin_dictionary

    # load dictionary from file and place to cache
    dictionary_path = os.path.abspath(os.path.dirname(__file__)) + f'/_data/dictionary.{locale}.txt.bz2'
    bytes_stream_load_dictionary = BytesStreamLoadDictionary()
    load_dictionary_from_bz_text_file = Bz2TextFileLoadDictionary(
        bytes_stream_load_dictionary=bytes_stream_load_dictionary
    )

    dictionary = load_dictionary_from_bz_text_file.load(file_path=dictionary_path)
    _builtin_dictionary= MappingDictionary(dictionary=dictionary)
    return _builtin_dictionary
