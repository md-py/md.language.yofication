#!/usr/bin/env python3
import os
import sys
import re

#-------------------------------------------------------------------------#
#
#                         ▗▀▖▗       ▐
#                   ▌ ▌▞▀▖▐  ▄ ▞▀▖▝▀▖▜▀ ▞▀▖▙▀▖  ▛▀▖▌ ▌
#                   ▚▄▌▌ ▌▜▀ ▐ ▌ ▖▞▀▌▐ ▖▌ ▌▌  ▗▖▙▄▘▚▄▌
#                   ▗▄▘▝▀ ▐  ▀▘▝▀ ▝▀▘ ▀ ▝▀ ▘  ▝▘▌  ▗▄▘
#
# Description:
#    This is a Russian text yoficator (ёфикатор).
#
#    It conservatively replaces every "е" to "ё" when it's unambiguously
#    a case of the latter. No context is used; it relies entirely on a lack
#    of dictionary entries for a correspondent "truly е" homograph.
#
#    Yoficating Russian texts remove some unnecessary ambiguity.
#    https://en.wikipedia.org/wiki/Yoficator
#    https://ru.wikipedia.org/wiki/Ёфикатор
#
#    Syntax: yoficator.py [text-file-in-Russian | string-in-Russian]
#
#    Depends on yoficator.dic, which is used for the lookup.
#
#    Limitations:
#    * The code being conservative and not looking for context, it won't correct
#      when a "truly е" homograph exists. Thus a "все" will never be corrected,
#      because both все and всё exist as different words.
#    * Prone to wrongly yoficate other Cyrillic-based languages, such as
#      Bulgarian, Ukrainian, Belarussian.
#    * It's not the fastest thing in the world, mind you. But does the job.
#
#-------------------------------------------------------------------------
#
# Found this useful? Appalling? Appealing? Please let me know.
# The Unabashed welcomes your impressions.
#
# You will find the
#   unabashed
# at the location opposite to
#   moc • thgimliam
#
#-------------------------------------------------------------------------
#
# License:
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#
#--------------------------------------------------------------------------#


if __name__ == '__main__':
    # TODO Better handle lowercase, uppercase
    dictionary_file_path = os.path.abspath(os.path.dirname(__file__)) + '/_data/yoficator.dic'

    if len(sys.argv) > 1:
        # Is the input a filename?
        if os.path.isfile(sys.argv[1]):
            text = open(sys.argv[1]).read()
        # Else we will assume it's a string
        else:
            text = sys.argv[1]
    else:
        print('Error: No file specified', file=sys.stderr)
        exit(1)

    dictionary = {}

    # Splitter / tokenizer
    splitter = re.compile(r'(\s+|\w+|\W+|\S+)')

    with open(dictionary_file_path) as stream:
        for line in iter(stream):
            if ':' in line:
                key, value = line.split(':')
                dictionary[key] = value.rstrip('\n')

    for token in splitter.finditer(text):
        if token in dictionary:
            print(dictionary[token], end='')
        else:
            print(token, end='')
