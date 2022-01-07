# [fts](https://github.com/rtmigo/fts_py)

A minimalistic algorithm for ranking elements that have the maximum number of 
features that match the features in the query.

An illustrative example: full-text search, where we search for documents that 
contain words from the query.

The algorithm takes into account:
- the number of matching words
- the rarity of such words in the database
- the frequency of occurrence of words in the document

## Install

### pip

```bash
pip3 install git+https://github.com/rtmigo/fts_py#egg=fts
```

### setup.py

```python3
install_requires = [
    "fts@ git+https://github.com/rtmigo/fts_py"
]
```