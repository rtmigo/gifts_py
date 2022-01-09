

import math
import unittest

from gifts import SmoothFts


class SmoothTest(unittest.TestCase):
    def test_from_example(self):
        # comparing internal values in Fts with values
        # from https://bit.ly/3zEDkMn

        def _reference():
            # https://bit.ly/3zEDkMn
            tf_1_problem = 1 / 3
            tf_1_of = 1 / 3
            tf_1_evil = 1 / 3
            D_all = 3
            d_problem = 2
            d_of = 1
            d_evil = 2
            tf_idf_problem = tf_1_problem * (
                    math.log((D_all + 1) / (d_problem + 1)) + 1)
            tf_idf_of = tf_1_of * (math.log((D_all + 1) / (d_of + 1)) + 1)
            tf_idf_evil = tf_1_evil * (math.log((D_all + 1) / (d_evil + 1)) + 1)
            print(f"idf_evil: {(math.log((D_all + 1) / (d_evil + 1)) + 1)}")
            print(f"tf_idf_evil: {tf_idf_evil}")

            denominator = math.sqrt(tf_idf_problem ** 2
                                    + tf_idf_of ** 2 + tf_idf_evil ** 2)
            return tf_idf_evil / denominator

        db = SmoothFts()
        doc1 = db.add(['problem', 'of', 'evil'])
        db.add(['evil', 'queen'])
        db.add(['horizon', 'problem'])

        self.assertAlmostEqual(doc1._tf['problem'], 1 / 3)
        self.assertAlmostEqual(doc1._tf['of'], 1 / 3)
        self.assertAlmostEqual(doc1._tf['evil'], 1 / 3)

        self.assertAlmostEqual(db.documents_count, 3)  # D_all
        self.assertAlmostEqual(db._d('problem'), 2)
        self.assertAlmostEqual(db._d('of'), 1)
        self.assertAlmostEqual(db._d('evil'), 2)

        self.assertAlmostEqual(db._word_to_idf('evil'), 1.2876820724517808)

        self.assertEqual(
            doc1._tf_idf('evil', db._word_to_idf),
            0.42922735748392693)

        self.assertAlmostEqual(_reference(),
                               0.5178561161676974)

        self.assertAlmostEqual(doc1.weight('evil', db._word_to_idf, 0),
                               0.5178561161676974)

        pass
