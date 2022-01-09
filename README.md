# [gifts](https://github.com/rtmigo/gifts_py)

Searching for elements that have the **common features** with the query.

For example:

```python3
query = ['A', 'B']

elements = [
    ['N', 'A', 'M'],  # common features: 'A'
    ['C', 'B', 'A'],  # common features: 'A', 'B'  
    ['X', 'Y']  # no common features
]
```

In this case, the search with return `['C', 'B', 'A']` and `['N', 'A',
'M']` in that particular order.

## Use for full-text search

Finding documents that contain words from the query.

```python3
from gifts import SmoothFts

fts = SmoothFts()

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

In the examples above, the words were literally words as strings. But they can
be any objects suitable as `dict` keys.

```python3
from gifts import SmoothFts

fts = SmoothFts()

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

### SmoothFts

```python3
from gifts import SmoothFts
```

It uses logarithmic [tf-idf](https://en.wikipedia.org/wiki/Tf%E2%80%93idf) for
weighting the words
and [cosine similarity](https://en.wikipedia.org/wiki/Cosine_similarity)
for scoring the matches.

### SimpleFts

```python3
from gifts import SimpleFts
```

Minimalistic approach: weigh, multiply, compare. This object is noticeably
faster than `SmoothFts`.

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

## See also

The [skifts](https://github.com/rtmigo/skifts_py#readme) package 
implements the same algorithm, but uses [scikit-learn](https://scikit-learn.org) 
for better performance.
