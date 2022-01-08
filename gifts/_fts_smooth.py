# SPDX-FileCopyrightText: (c) 2022 Artёm IG <github.com/rtmigo>
# SPDX-License-Identifier: MIT

import uuid
from collections import defaultdict, Counter
from math import log, sqrt
from typing import Iterable, List, Optional, TypeVar, Generic, Dict, Callable, \
    Collection

from gifts._cosine_similarity import cosine_similarity

TWord = TypeVar('TWord')


def _idf(docs_with_word: int, docs_total: int) -> float:
    """Inverse document frequency. Gives lower values for frequently used
    words.

    Here, the variant of the formula used in SciKit (https://bit.ly/3zEDkMn)
    is closest to "inverse document frequency smooth" from
    [Wikipedia](https://en.wikipedia.org/wiki/Tf%E2%80%93idf).
    """
    assert docs_with_word <= docs_total
    return log((docs_total + 1) / (docs_with_word + 1)) + 1


def _tf(word_occured_in_doc: int, total_words_in_doc: int) -> float:
    """Term frequency of a word in certain document.

    See: https://bit.ly/3zEDkMn
    """

    assert word_occured_in_doc <= total_words_in_doc
    return word_occured_in_doc / total_words_in_doc


class _Document(Generic[TWord]):
    def __init__(self, doc_id: Optional[str], words: List[TWord]):
        self.doc_id = doc_id
        self._words = words
        counts = Counter(self._words)
        words_in_doc = len(self._words)
        assert sum(counts.values()) == len(self._words)
        self._tf: Dict[TWord, float] = \
            dict((word, _tf(word_occurrences, words_in_doc))
                 for (word, word_occurrences)
                 in counts.items())
        self._word_to_weight: Optional[Dict[TWord, float]] = None
        self._weights_version: Optional[int] = None

    @property
    def unique_words(self) -> Collection[TWord]:
        return self._tf.keys()

    def weight(self,
               word: TWord,
               idf: Callable[[TWord], float],
               idf_version: int) \
            -> float:
        """Returns the normalized weight of `word` in the current document.

        It is a smoothed version of TF-IDF, as used is SciKit-Learn and
        described at https://bit.ly/3zEDkMn V_norm.

        Basically it is a euclidean norm like:
            V[i] / sqrt(V[1]**2 + V[2]**2 + ... + V[n]**2)
        where V[i] is a TF-IDF of term i
        """
        # We cannot calculate the weight when creating a document: at that time,
        # we still do not have statistics on all (other) documents and the
        # frequency of words in them. And now we have been given information
        # about the frequency by the `idf` argument.
        if self._word_to_weight is None or self._weights_version != idf_version:
            # Either we never calculated the weights, or the word frequency
            # information has been updated. In any case, the weights must
            # be recalculated.
            #
            # Now we will compute euclidean norm for all words in document.
            # Numerator will be different for each word, denominator will be
            # the same for all words. We prefer to compute weights for all
            # words at once to avoid recomputing denominator
            unique_words = self._tf.keys()
            denominator = sqrt(sum(self._tf_idf(w, idf) ** 2
                                   for w in unique_words))
            self._word_to_weight = dict(
                (w, self._tf_idf(w, idf) / denominator)
                for w in unique_words)
            self._weights_version = idf_version

        assert self._weights_version == idf_version
        return self._word_to_weight.get(word, 0)

        # https://stackoverflow.com/a/46812408

    def _tf_idf(self, word: TWord, idf: Callable[[TWord], float]) -> float:
        return self._tf.get(word, 0) * idf(word)

    # def normalized_term_weight(self, word: TWord) -> float:


class SmoothFts(Generic[TWord]):
    def __init__(self):
        self._id_to_doc: Dict[str, _Document] = {}
        self._word_to_docs: Dict[TWord, List[_Document]] = defaultdict(list)

        self._db_version = 0
        """Updates each time when we add or remove document."""

    @property
    def words_count(self) -> int:
        return len(self._word_to_docs)

    @property
    def documents_count(self) -> int:
        return len(self._id_to_doc)

    def add(self, words: List[TWord],
            doc_id: Optional[str] = None) -> _Document:
        """Adds a document to the database and returns its ID."""
        if doc_id is None:
            doc_id = str(uuid.uuid4())
        if doc_id in self._id_to_doc:
            raise ValueError(f"Id '{doc_id}' is not unique")

        self._db_version += 1  # todo test

        document = _Document(doc_id, words)
        self._id_to_doc[doc_id] = document
        for word in document.unique_words:
            self._word_to_docs[word].append(document)

        return document

    def _d(self, word: TWord) -> int:
        docs_with_word = self._word_to_docs.get(word)
        if docs_with_word is not None:
            return len(docs_with_word)
        return 0

    def _word_to_idf(self, word: TWord) -> float:
        # docs_with_word = self._word_to_docs.get(word)
        return _idf(
            docs_with_word=self._d(word),
            docs_total=self.documents_count)

    def _docs_containing_any_word_from(self, words: Iterable[TWord]) \
            -> Collection[_Document]:
        matched_docs = {}
        for word in words:
            for doc in self._word_to_docs.get(word) or []:
                matched_docs[doc.doc_id] = doc
        return matched_docs.values()

    def search(self, query: List[TWord]) -> List[str]:
        """Returns IDs of documents that include at least one word from `query`.
        More relevant matches will be at the top of the list.

        `prioritize_words_count` determines whether the documents with the most
        words from the query should always be ranked higher. If `False`, the
        number of matches may be outweighed by the rarity of matched words
        or their frequency in the document.
        """

        if len(query) <= 0:
            raise ValueError

        query_doc = _Document(doc_id=None, words=query)

        def term_to_weight(doc: _Document, word: TWord) -> float:
            return doc.weight(word, self._word_to_idf, self._db_version)

        matches = []

        # finding all documents containing at least one word from query
        for match_doc in self._docs_containing_any_word_from(
                query_doc.unique_words):
            # listing all unique words in both query and vector
            all_words = list(set(match_doc.unique_words) |
                             set(query_doc.unique_words))
            query_vector = [term_to_weight(query_doc, w) for w in all_words]
            doc_vector = [term_to_weight(match_doc, w) for w in all_words]
            assert len(doc_vector) == len(query_vector)
            score = cosine_similarity(doc_vector, query_vector)

            assert match_doc.doc_id is not None
            matches.append((score, match_doc.doc_id))

        matches.sort(reverse=True)
        return [doc_id for score, doc_id in matches]
