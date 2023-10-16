<!-- These are examples of badges you might want to add to your README:
     please update the URLs accordingly

[![Project generated with PyScaffold](https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold)](https://pyscaffold.org/)
[![Built Status](https://api.cirrus-ci.com/github/<USER>/biocgenerics.svg?branch=main)](https://cirrus-ci.com/github/<USER>/biocgenerics)
[![ReadTheDocs](https://readthedocs.org/projects/biocgenerics/badge/?version=latest)](https://biocgenerics.readthedocs.io/en/stable/)
[![Coveralls](https://img.shields.io/coveralls/github/<USER>/biocgenerics/main.svg)](https://coveralls.io/r/<USER>/biocgenerics)
[![Conda-Forge](https://img.shields.io/conda/vn/conda-forge/biocgenerics.svg)](https://anaconda.org/conda-forge/biocgenerics)
[![Twitter](https://img.shields.io/twitter/url/http/shields.io.svg?style=social&label=Twitter)](https://twitter.com/biocgenerics)
-->

# BiocGenerics

[![PyPI-Server](https://img.shields.io/pypi/v/biocgenerics.svg)](https://pypi.org/project/biocgenerics/)
[![Monthly Downloads](https://pepy.tech/badge/biocgenerics/month)](https://pepy.tech/project/biocgenerics)
![Unit tests](https://github.com/BiocPy/generics/actions/workflows/pypi-test.yml/badge.svg)

This package aims to provide common generics, much like R/Bioconductor. These generics allow users to operate on different objects is a consistent and reliable way.

## Install

Install package from [PyPI](https://pypi.org/project/biocgenerics/)

```shell
pip install biocgenerics
```

## Combine

Combine provide multiple functions to concatenate sequences and array-like objects.

- `combine_seqs`: Combine 1-dimensional sequences or vector-like objects.
- `combine_rows`: Combine n-dimensional or DataFrame like objects along the first dimension.
- `combine_cols`: Combine n-dimensional or DataFrame like objects along the second dimension.

```python
from biocgenerics import combine_seqs, combine_rows

# example to combine multiple sequences
x = [1, 2, 3]
y = [0.1, 0.2]

print(combine_seqs(x, y))

# Works across types as well,
# e.g. sparse and dense matrices

num_cols = 20
x = np.ones(shape=(10, num_cols))
y = sp.identity(num_cols)

print(combine_rows(x, y))
```

Additionally, the `combine` generic, automatically dispatches to either `combine_seqs` or `combine_cols` methods depending on the inputs.

## Set and Access names

Reliably access row and column names of **Dataframe**-like objects.

- `rownames`: Access row names of the object.
- `set_rownames`: Set new row names.
- `colnames`: Access column names.
- `set_colnames`: Set new column names.

```python
import pandas as pd
from biocgenerics import rownames

df1 = pd.DataFrame([["a", 1], ["b", 2]], columns=["letter", "number"])

rownames(df1)
```

Check out the [S4Vectors](https://github.com/Bioconductor/S4Vectors) package for more information.

<!-- pyscaffold-notes -->

## Note

This project has been set up using PyScaffold 4.4. For details and usage
information on PyScaffold see https://pyscaffold.org/.
