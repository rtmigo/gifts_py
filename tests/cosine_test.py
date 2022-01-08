import unittest

from gifts._cosine_similarity import cosine_similarity


class TestCosine(unittest.TestCase):
    def test(self):
        # https://www.learndatasci.com/glossary/cosine-similarity/
        d1 = [0, 0, 0, 1, 1, 1, 1, 1, 2, 1, 2, 0, 1, 0]
        d2 = [0, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1]
        d3 = [1, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]
        self.assertAlmostEqual(
            cosine_similarity(d1, d2),
            0.6885303726590963)
        self.assertAlmostEqual(
            cosine_similarity(d1, d3),
            0.21081851067789195)
        self.assertAlmostEqual(
            cosine_similarity(d2, d3),
            0.2721655269759087)