# Did I forget any imports?

[![pipeline status](https://gitlab.com/marvin.vanaalst/difai/badges/main/pipeline.svg)](https://gitlab.com/marvin.vanaalst/difai/-/commits/main)
[![coverage report](https://gitlab.com/marvin.vanaalst/difai/badges/main/coverage.svg)](https://gitlab.com/marvin.vanaalst/difai/-/commits/main)
[![PyPi](https://img.shields.io/pypi/v/difai)](https://pypi.org/project/difai/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![Downloads](https://pepy.tech/badge/difai)](https://pepy.tech/project/difai)

DIFAI searches for import statements for all the python and jupyter notebook files in the current directory. It then uses `pip freeze` to get your installed versions and `pip-compile` to generate a `requirements.txt` file containing all of your dependencies and their depdendencies including hashes for a reproducible build.

## Run

Simply call `difai` in the current folder.
You can change the input (where the `.py` and `.ipynb` files are read) and output (where the `requirement.in` and `requirements.txt` files are written) folders using
`--in-path` and `--out-path` respectively.
In order to exclude certain packages from the search, you can use the `--exclude` option.

## Pipeline

<div class="center">

```mermaid
graph TB
    A[glob] --> B
    A --> C
    B[.py] --> D
    C[.ipynb] -->|nbconvert| B
    D[AST]  --> E
    X[pip freeze] --> E
    E[requirements.in] -->|pip tools| F
    F[requirements.txt]
```

</div>
