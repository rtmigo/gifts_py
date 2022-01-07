# [gifts](https://github.com/rtmigo/gifts_py)

Searching elements that have the maximum number of features that match the
features in the query.

An illustrative example: full-text search, where we search for documents that
contain words from the query.

The algorithm takes into account:

- the number of matching words
- the rarity of such words in the database
- the frequency of occurrence of words in the document

## Example

```python3
from gifts import Fts

fts = Fts()

fts.add(["wait", "mister", "postman"],
        doc_id="doc1")
fts.add(["oh", "yes", "wait", "a", "minute", "mister", "postman"],
        doc_id="doc2")
fts.add(["please", "mister", "postman", "look", "and", "see",
         "if", "there's", "a", "letter",
         "in", "your", "bag", "for", "me"],
        doc_id="doc3")

# print IDs of documents in which at least one word of the query occurs, 
# starting with the most relevant documents
for doc_id in fts.search(['postman', 'wait']):
    print(doc_id)
```

In the example above, the words were literally words as strings. But they can 
be any
objects suitable as `dict` keys.

```python3
from gifts import Fts

fts = Fts()

fts.add([3, 1, 4, 1, 5, 9, 2], doc_id="doc1")
fts.add([6, 5, 3, 5], doc_id="doc2")
fts.add([8, 9, 7, 9, 3, 2], doc_id="doc3")

for doc_id in fts.search([5, 3, 7]):
    print(doc_id)
```

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