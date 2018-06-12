# Given a words.txt file containing a newline-delimited list of dictionary
# words, please implement the Anagrams class so that the get_anagrams() method
# returns all anagrams from words.txt for a given word.
#
# Requirements:
#   - Optimise the code for fast retrieval
#   - Write more tests
#   - Thread safe implementation

import sys
import unittest
from collections import defaultdict

class Anagrams(object):
    def __init__(self, wordsfile='words.txt'):
        with open(wordsfile, 'r') as f:
            self.words = self._collate(f.readlines())

    def _collate(cls, words):
        # Collate word-iterator into a basic lookup table.
        d = defaultdict(list)
        for w in words:
            d[cls._squash(w)].append(w.strip())
        return d

    def _squash(cls, word):
        # Prep word for lookup.
        return tuple(sorted(word.strip()))

    def get_anagrams(self, word):
        """
        :param str word: Word to lookup
        :rtype: List[Str]
        :returns: List of anagrams for given word, empty if none found.
        """
        return self.words.get(self._squash(word), [])


class TestAnagrams(unittest.TestCase):

    def test_anagrams(self):
        anagrams = Anagrams()
        self.assertEqual(anagrams.get_anagrams('plates'), ['palest', 'pastel', 'petals', 'plates', 'staple'])
        self.assertEqual(anagrams.get_anagrams('eat'), ['ate', 'eat', 'tea'])
        self.assertEqual(anagrams.get_anagrams('Zurich'), ['Zurich'])
        self.assertEqual(anagrams.get_anagrams('zzzzzzzzzzzzz'), [])


if __name__ == '__main__':
    unittest.main()
