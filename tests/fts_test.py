# SPDX-FileCopyrightText: (c) 2022 Artёm IG <github.com/rtmigo>
# SPDX-License-Identifier: MIT

from gifts import Fts

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
            '(Wait)')
        self.assertEqual(
            db.search(['wait', 'postman'], prioritize_number_of_words_matched=True)[0],
            "Wait Mister Postman")

        self.assertEqual(
            len(db.search(['jabberwocky'])), 0)

    def test_empty_query(self):
        db = Fts()
        for doc in [
            [2, 3],
            [1, 2, 3],
            [1, 3, 4, 2]
        ]:
            db.add(doc_id=str(doc), words=doc)

        db.search([1]) # no problem
        with self.assertRaises(ValueError):
            db.search([])

    def test_nums(self):

        db = Fts()
        for doc in [
            [2, 3],
            [1, 2, 3],
            [1, 3, 4, 2]
        ]:
            db.add(doc_id=str(doc), words=doc)

        # при поиске единицы найдем самую короткую последовательность
        # с ней
        r = db.search([1])
        self.assertEqual(len(r), 2)
        self.assertEqual(r[0], '[1, 2, 3]', )

        # числа [2, 3] есть в каждой из последовательностей.
        # Короткие будут первыми
        q = [2, 3]
        r = db.search(q)
        self.assertEqual(len(r), 3)
        self.assertEqual(r[0], '[2, 3]')
        self.assertEqual(r[1], '[1, 2, 3]')

        # число 4 в сочетании с 1 есть только в одной последовательности.
        # Она будет первой
        q = [4, 1]
        r = db.search(q)
        self.assertEqual(len(r), 2)
        self.assertEqual(r[0], '[1, 3, 4, 2]')
        self.assertEqual(r[1], '[1, 2, 3]')

    def test_number_of_matched_words(self):

        db = Fts()
        for doc in [
            [1, 2, 3],
            [3, 2, 1],
            [1, 9, 5], # !
            [2, 3, 1],
            [1, 3, 2],

        ]:
            db.add(doc_id=str(doc), words=doc)

        q = [1, 2, 3, 5]

        r = db.search(q)
        # всего два совпадения, но приоритетное слово
        self.assertEqual(r[0], '[1, 9, 5]')

        # в обычном режиме найдем что-то другое
        r = db.search(q, prioritize_number_of_words_matched=True)
        self.assertNotEqual(r[0], '[1, 9, 5]')



        #r = db.search(q, prioritize_number_of_matched_words=False)
        #self.assertEqual(len(r), 2)
        #self.assertEqual(r[0], '[1, 3, 4, 2]')
        #self.assertEqual(r[1], '[1, 2, 3]')

    def test_word_popularity(self):

        db = Fts()
        for doc in [
            [1, 2],
            [1, 3],
            [7, 5],
            [1, 4],
            [9, 8]
        ]:
            db.add(doc_id=str(doc), words=doc)

        # не будет ни одного полного совпадения, но первым найдется
        # совпадение с редкой пятеркой

        q = [1, 5]
        r = db.search(q)
        self.assertEqual(len(r), 4)
        self.assertEqual(r[0], '[7, 5]')

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
