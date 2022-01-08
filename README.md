# [gifts](https://github.com/rtmigo/gifts_py)

Searching for elements that have the **common features** with the query.

For example:

```python3
query = ['A', 'B']

elements = [
    ['N', 'A', 'M'],  # common features: 'A'
    ['C', 'B', 'A'],  # common features: 'A', 'B'  
    ['X', 'Y']        # no common features
]
```

In this case, the search with return `['C', 'B', 'A']` and `['N', 'A', 
'M']` in that particular order.

## Use for full-text search

Finding documents that contain words from the query.

```python3
from gifts import Fts

fts = Fts()

fts.add(["wait", "mister", "postman"],
        doc_id="doc1")

fts.add(["please", "mister", "postman", "look", "and", "see"],
        doc_id="doc2")

fts.add(["oh", "yes", "wait", "a", "minute", "mister", "postman"],
        doc_id="doc3")

# print IDs of documents in which at least one word of the query occurs, 
# starting with the most relevant matches
for doc_id in fts.search(['postman', 'wait']):
    print(doc_id)
```

## Use for abstract data mining

In the examples above, the words were literally words as strings. But they 
can be any objects suitable as `dict` keys.

```python3
from gifts import Fts

fts = Fts()

fts.add([3, 1, 4, 1, 5, 9, 2], doc_id="doc1")
fts.add([6, 5, 3, 5], doc_id="doc2")
fts.add([8, 9, 7, 9, 3, 2], doc_id="doc3")

for doc_id in fts.search([5, 3, 7]):
    print(doc_id)
```

## Implementation details

When ranking the results, the algorithm takes into account::

- the number of matching words
- the rarity of such words in the database
- the frequency of occurrence of words in the document

It uses [tf-idf](https://en.wikipedia.org/wiki/Tf%E2%80%93idf) for weighting the
words
and [cosine similarity](https://en.wikipedia.org/wiki/Cosine_similarity)
for scoring the matches. In other words, the classic search engine approach.

A similar results can be achieved with libraries like
[scikit](https://scikit-learn.org), and it will probably be much more efficient
for large datasets.

The only advantage of the [gifts](https://github.com/rtmigo/gifts_py) package is
its compactness, pure Python code and no external dependencies.

## Install

### pip

```bash
pip3 install git+https://github.com/rtmigo/gifts_py#egg=gifts
```

### setup.py

```python3
install_requires = [
    "gifts@ git+https://github.com/rtmigo/gifts_py"
]
```