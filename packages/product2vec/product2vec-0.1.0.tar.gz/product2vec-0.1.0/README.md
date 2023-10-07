[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![pipeline](https://github.com/TheoVall-DS/product2vec/actions/workflows/python-app.yml/badge.svg)](https://github.com/TheoVall-DS/product2vec/actions/workflows/python-app.yml)
[![codecov](https://codecov.io/gh/TheoVall-DS/product2vec/graph/badge.svg?token=QYUC5D65PT)](https://codecov.io/gh/TheoVall-DS/product2vec)

# product2vec

product2vec is a Python library that implements Product2Vec model. It is capable of finding complements and substitutes among products given shopping baskets. Current implementation is based on the original paper: https://ssrn.com/abstract=3519358

# Installation

```
pip install product2vec
```

# Usage

```
>>> from product2vec import Product2Vec
>>> # toy dataset with two baskets and 4 products
>>> data = [
...     ['coffee', 'cookies', 'chocolate'],
...     ['tea', 'cookies', 'chocolate'],
... ]
>>> prod2vec = Product2Vec(vector_size=3, min_count=1, sample=0, seed=1, workers=1)
>>> _ = prod2vec.fit(data)
>>> prod2vec.show_substitutes(product='tea', topn=2)
[('coffee', 0.024425969), ('chocolate', 0.023691988)]
>>> prod2vec.show_complements(product='cookies', topn=2)
[('chocolate', 0.5030633), ('coffee', 0.5007087)]
```

Refer to `usage_example.ipynb` which can be found in GitHub repository for short model description and elaborate usage.

# Contributing

If you spot any bugs or have suggestions don't hesitate to open an issue.
