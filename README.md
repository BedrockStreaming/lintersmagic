# Linters magic
Magic function for pycodestyle module in Jupyter-Lab or Databricks notebooks.

Current version: 0.1.4

Versions of dependencies:
- python: 3.8
- pycodestyle: 2.8.0
- ipython: 8.1.1

**Note that we've tested it only on Databricks notebooks**

# Installation

```
pip install lintersmagic
```

# Usage
Enable the magic function by using the lintersmagic module in a cell

`%load_ext lintersmagic`

## To check a cell once:
use the function as first line in your cell to check compliance with `pycodestyle` as such:

`%%pycodestyle`

## To auto check each cell:
If you want this compliance checking turned on by default for each cell then run this magic line function in an empty cell:

`%pycodestyle_on`

You only need to call this once (observe the single `%`).

To turn off the auto-checking for each cell use:

`%pycodestyle_off`

## Config options for `%pycodestyle_on` (version >= 0.5)

1. The option `--ignore` or `-i` will add the the named error(s) to the ignore list

Example to ignore the errors `E225` and `E265`:
```
%pycodestyle_on --ignore E225,E265
``` 
Remember to _avoid_ spaces between declaring multiple errors.

2. With the option `--max_line_length` or `-m` the max-line-length can be customised.

Example to set the line length to `119` characters instead of the default `79`:

```
%pycodestyle_on --max_line_length 119
```

The options can be combined as well. 


See notebooks in notebook directory for example use cases, as such:
### Pycodestyle ([notebook](https://github.com/BedrockStreaming/lintersmagic/blob/main/notebook/examples.ipynb))
![Notebook examples](img/pycodestyle.png)

## Contribution

### Dependencies and package

Handled by Poetry ([documentation](https://python-poetry.org/))

To get a new package:

```
poetry build
```

To install the dependencies:

```
poetry install
```

To publish a new version:

```
poetry publish
```

### Tests

```
poetry run ipython tests/*.py
```

### Useful links

- This project adds a magic function in Ipython. Here is the documentation:
  [Built-in magic commands](https://ipython.readthedocs.io/en/stable/interactive/magics.html)

- This project uses a callback with magic functions. Here is the documentation:
  [IPython Events](https://ipython.readthedocs.io/en/stable/config/callbacks.html)
