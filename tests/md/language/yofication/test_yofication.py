import unittest
import unittest.mock

import md.language.yofication


class TestMappingDictionary:
    def test_find(self) -> None:
        # arrange
        dictionary = {'трехмерный': 'трёхмерный'}

        # act
        mapping_dictionary = md.language.yofication.MappingDictionary(dictionary=dictionary)

        # assert
        assert mapping_dictionary.find(word='трехмерный') == 'трёхмерный'
        assert mapping_dictionary.find(word='четырехзвездный') is None

    def test_has(self) -> None:
        # arrange
        dictionary = {'трехмерный': 'трёхмерный'}

        # act
        mapping_dictionary = md.language.yofication.MappingDictionary(dictionary=dictionary)

        # assert
        assert mapping_dictionary.has(word='трехмерный') is True
        assert mapping_dictionary.has(word='четырехзвездный') is False

    def test_find_partly_yoficated(self) -> None:
        # arrange
        dictionary = {'четырехзвездный': 'четырёхзвёздный'}

        # act
        mapping_dictionary = md.language.yofication.MappingDictionary(dictionary=dictionary)

        # assert
        assert mapping_dictionary.find(word='четырёхзвёздный') == 'четырёхзвёздный'
        assert mapping_dictionary.find(word='четырехзвёздный') == 'четырёхзвёздный'
        assert mapping_dictionary.find(word='четырёхзвездный') == 'четырёхзвёздный'
        assert mapping_dictionary.find(word='четырехзвездный') == 'четырёхзвёздный'

    def test_has_partly_yoficated(self) -> None:
        # arrange
        dictionary = {'четырехзвездный': 'четырёхзвёздный'}

        # act
        mapping_dictionary = md.language.yofication.MappingDictionary(dictionary=dictionary)

        # assert
        assert mapping_dictionary.has(word='четырёхзвёздный') is True
        assert mapping_dictionary.has(word='четырехзвёздный') is True
        assert mapping_dictionary.has(word='четырёхзвездный') is True
        assert mapping_dictionary.has(word='четырехзвездный') is True


class TestRegularExpressionYoficate(unittest.TestCase):
    def test_word(self) -> None:
        # arrange
        def yoficate_word_mock(word: str) -> str:
            if word.lower() == 'четырехзвездный':
                return 'четырёхзвёздный'
            return word

        # arrange
        mapping_dictionary = unittest.mock.Mock(spec=md.language.yofication.DictionaryInterface)
        mapping_dictionary.find = unittest.mock.Mock(side_effect=yoficate_word_mock)
        mapping_dictionary.has = unittest.mock.Mock(return_value=True)

        # act
        yoficate = md.language.yofication.RegularExpressionYoficate(dictionary=mapping_dictionary)
        yoficated_text = yoficate.word(word='четырехзвездный')

        # assert
        assert 'четырёхзвёздный' == yoficated_text

    def test_word_preserve_letter_cases(self) -> None:
        # arrange
        def yoficate_word_mock(word: str) -> str:
            assert word.islower()
            if word.lower() == 'четырехзвездный':
                return 'четырёхзвёздный'
            return word

        # arrange
        mapping_dictionary = unittest.mock.Mock(spec=md.language.yofication.DictionaryInterface)
        mapping_dictionary.find = unittest.mock.Mock(side_effect=yoficate_word_mock)
        mapping_dictionary.has = unittest.mock.Mock(return_value=True)

        # act
        yoficate = md.language.yofication.RegularExpressionYoficate(dictionary=mapping_dictionary)
        yoficated_text = yoficate.word(word='чЕТырЕХзвеЗДНый')

        # assert
        assert 'чЕТырЁХзвёЗДНый' == yoficated_text

    def test_text(self) -> None:
        # arrange
        def yoficate_word_mock(word: str) -> str:
            if word.lower() == 'трехмерный':
                return 'трёхмерный'
            if word.lower() == 'четырехзвездный':
                return 'четырёхзвёздный'
            return word

        # arrange
        mapping_dictionary = unittest.mock.Mock(spec=md.language.yofication.DictionaryInterface)
        mapping_dictionary.find = unittest.mock.Mock(side_effect=yoficate_word_mock)
        mapping_dictionary.has = unittest.mock.Mock(return_value=True)

        # act
        yoficate = md.language.yofication.RegularExpressionYoficate(dictionary=mapping_dictionary)
        yoficated_text = yoficate.text(
            text='трехмерный тРехмерныЙ test четырехзвездный трЕхмеРНый чЕТыРЕХзвЕЗдный четырёхЗВЁЗДНый'
        )

        # assert
        assert 'трёхмерный тРёхмерныЙ test четырёхзвёздный трЁхмеРНый чЕТыРЁХзвЁЗдный четырёхЗВЁЗДНый' == yoficated_text


if __name__ == '__main__':
    unittest.main()
