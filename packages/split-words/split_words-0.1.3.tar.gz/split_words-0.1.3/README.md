[![pytest](https://github.com/ffreemt/split-words/actions/workflows/routine-tests.yml/badge.svg)](https://github.com/ffreemt/split-words/actions)[![python](https://img.shields.io/static/v1?label=python+&message=3.8%2B&color=blue)](https://www.python.org/downloads/)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)[![PyPI version](https://badge.fury.io/py/split-words.svg)](https://badge.fury.io/py/split-words)

# split-words

[`CharSplit`](https://github.com/dtuggener/CharSplit) repacked with `poetry`, published as `pypi` `split-words`--
all credit goes to the original author.
```
pip install split-words
```
```
# replace charsplit with split_words in the following, e.g.
from split_words import Splitter
...
```

## CharSplit - An *ngram*-based compound splitter for German
[url](https://github.com/dtuggener/CharSplit)

Splits a German compound into its body and head, e.g.
> Autobahnraststätte -> Autobahn - Raststätte

Implementation of the method decribed in the appendix of the thesis:

Tuggener, Don (2016). *Incremental Coreference Resolution for German.* University of Zurich, Faculty of Arts.

**TL;DR**: The method calculates probabilities of ngrams occurring at the beginning, end and in the middle of words and identifies the most likely position for a split.

The method achieves ~95% accuracy for head detection on the [Germanet compound test set](http://www.sfs.uni-tuebingen.de/lsd/compounds.shtml).

A model is provided, trained on 1 Mio. German nouns from Wikipedia.

### Usage ###
**Train** a new model:
```bash
training.py --input_file --output_file
```
from command line, where `input_file` contains one word (noun) per line and `output_file` is a json file with computed n-gram probabilities.

**Compound splitting**

In python

```python
>> from charsplit import Splitter
>> splitter = Splitter()
>> splitter.split_compound("Autobahnraststätte")
```
returns a list of all possible splits, ranked by their score, e.g.
```python
[(0.7945872450631273, 'Autobahn', 'Raststätte'),
(-0.7143290887876655, 'Auto', 'Bahnraststätte'),
(-1.1132332878581173, 'Autobahnrast', 'Stätte'), ...]
```
By default, `Splitter` uses the data from the file `charsplit/ngram_probs.json`. If you retrained the model, you may specify a custom file with
```python
>> splitter = Splitter(ngram_path=<json_data_file_with_ngram_probs>)
```

