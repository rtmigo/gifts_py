from fts import Fts

_mr_postman = """
    Oh yes, wait a minute Mister Postman
    (Wait)
    Wait Mister Postman
    Please Mister Postman, look and see
    (Oh yeah)
    If there's a letter in your bag for me
    (Please, Please Mister Postman)
    Why's it takin' such a long time
    (Oh yeah)
    For me to hear from that boy of mine
    There must be some word today
    From my boyfriend so far away
    Please Mister Postman, look and see
    If there's a letter, a letter for me
    I've been standin' here waitin' Mister Postman
    So patiently
    For just a card, or just a letter
    Sayin' he's returnin' home to me
    Mister Postman, look and see
    (Oh yeah)
    If there's a letter in your bag for me
    (Please, Please Mister Postman)
    Why's it takin' such a long time
    (Oh yeah)
    For me to hear from that boy of mine
    So many days you passed me by
    See the tears standin' in my eyes
    You didn't stop to make me feel better
    By leavin' me a card or a letter
    Mister Postman, look and see
    If there's a letter in your bag for me
    (Please, Please Mister Postman)
    Why's it takin' such a long time
    Wait a minute
    Wait a minute
    Wait a minute
    Wait a minute
    (Mister Postman)
    Mister Postman, look and see
"""
import re
import unittest
from typing import List


def _words(text: str) -> List[str]:
    return [w.lower() for w in re.findall(r'\w+', text)]


class TestFts(unittest.TestCase):
    def test(self):

        db = Fts()
        for line in set(_mr_postman.splitlines()):
            db.add(doc_id=line.strip(), words=_words(line))

        for lst in db._word_to_docs.values():
            self.assertEqual(len(lst), len(set(wd.doc_id for wd in lst)))

        def docs_containing_word(word):
            return len(db._word_to_docs.get(word, 0))

        self.assertLess(docs_containing_word('patiently'),
                        docs_containing_word('please'))
        self.assertLess(docs_containing_word('please'),
                        docs_containing_word('a'))

        self.assertEqual(
            db.search(['wait'])[0],
            '(Wait)')

        self.assertEqual(
            db.search(['minute'])[0],
            'Wait a minute')

        self.assertEqual(
            db.search(['yeah'])[0],
            '(Oh yeah)')

        self.assertEqual(
            db.search(['please', 'postman'])[0],
            "(Please, Please Mister Postman)")

        self.assertEqual(
            db.search(['wait', 'postman'])[0],
            "Wait Mister Postman")

        self.assertEqual(
            len(db.search(['jabberwocky'])), 0)

    def test_not_unique_id(self):
        fts = Fts()
        fts.add(['a', 'b', 'c'], doc_id='id1')
        with self.assertRaises(ValueError):
            fts.add(['d', 'e', 'f'], doc_id='id1')

    def test_not_passing_id(self):
        fts = Fts()
        ids = set()
        ids.add(fts.add(['a', 'b', 'c']))
        ids.add(fts.add(['d', 'e']))
        ids.add(fts.add(['f', 'g']))
        self.assertEqual(len(ids), 3)
