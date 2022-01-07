# SPDX-FileCopyrightText: (c) 2022 Artёm IG <github.com/rtmigo>
# SPDX-License-Identifier: MIT

import uuid
from collections import defaultdict, Counter
from dataclasses import dataclass
from typing import Iterable, List, Optional, TypeVar, Generic, Dict, NamedTuple

TWord = TypeVar('TWord')


class _WeightedDoc(NamedTuple):
    doc_id: str
    """Document id"""
    weight: float


@dataclass
class _Match:
    doc_id: str
    """Document id"""
    sum_weight: float
    words_matched: int


class Fts(Generic[TWord]):
    def __init__(self):
        self._word_to_docs: Dict[TWord, List[_WeightedDoc]] = defaultdict(list)
        self._ids = set()

    def add(self, words: Iterable[TWord], doc_id: Optional[str] = None) -> str:
        """Adds a document to the database and returns its ID."""
        if doc_id is None:
            doc_id = str(uuid.uuid4())
        if doc_id in self._ids:
            raise ValueError(f"Id '{doc_id}' is not unique")
        self._ids.add(doc_id)
        ctr = Counter(words)
        total = sum(ctr.values())
        for word, count_in_this_doc in ctr.items():
            assert count_in_this_doc >= 1
            assert count_in_this_doc <= total
            assert doc_id is not None
            self._word_to_docs[word].append(
                _WeightedDoc(doc_id=doc_id, weight=count_in_this_doc / total))
        return doc_id

    def search(self, query: Iterable[TWord]) -> List[str]:
        query_word_to_count = Counter(query)

        candidates: Dict[str, _Match] = {}
        for word, word_occurences_in_query in query_word_to_count.items():
            docs_with_word = self._word_to_docs.get(word) or []
            for weighted_by_word in docs_with_word:
                # `weighted_by_word` - это часть базы. Мы сейчас возьмем
                # сведения из это объекта и оставим его неизменным в базе.
                # `weighted_by_word` содержит ссылку на документ,
                # где встретилось слово `word` из запроса, а также весовой
                # коэффициент 0..1 этого слова относительно конкретного
                # документа (вес больше, если слово в документе встречалось
                # чаще)
                assert 0 < weighted_by_word.weight <= 1

                # `match` - это объект, используемый только при анализе
                # данного запроса. Он соответствует отдельному документу.
                # Перебирая все слова из запроса, мы возвращаемся к одним и
                # тем же `match`, обновляя их поля
                match = candidates.get(weighted_by_word.doc_id)
                if match is None:
                    match = _Match(
                        sum_weight=0,
                        words_matched=0,
                        doc_id=weighted_by_word.doc_id)
                    candidates[weighted_by_word.doc_id] = match
                match.sum_weight += (
                        weighted_by_word.weight
                        * word_occurences_in_query
                        / len(docs_with_word))
                match.words_matched += 1

        def sorting_key(match: _Match):
            return match.words_matched, match.sum_weight, match.doc_id

        result = sorted(candidates.values(), key=sorting_key, reverse=True)
        return [r.doc_id for r in result]
