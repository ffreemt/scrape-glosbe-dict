# scrape-glosbe-dict
[![pytest](https://github.com/ffreemt/scrape-glosbe-dict/actions/workflows/routine-tests.yml/badge.svg)](https://github.com/ffreemt/scrape-glosbe-dict/actions)[![python](https://img.shields.io/static/v1?label=python+&message=3.8%2B&color=blue)](https://www.python.org/downloads/)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)[![PyPI version](https://badge.fury.io/py/scrape_glosbe_dict.svg)](https://badge.fury.io/py/scrape_glosbe_dict)

Scrape a glosbe dict

## Install it

```shell
pip install scrape-glosbe-dict

# pip install git+https://github.com/ffreemt/scrape-glosbe-dict
# poetry add git+https://github.com/ffreemt/scrape-glosbe-dict
# git clone https://github.com/ffreemt/scrape-glosbe-dict && cd scrape-glosbe-dict
```

## Use it
```bash
scrape-glosbe-dict head-word-file  # default english-chinese

# or python -m scrape_glosbe_dict head-word-file

# scrape-glosbe-dict head-word-file -f de # german-chinese
```

head word file formt: one word/phrase per line, empty lines will be ignored.

output will be saved to a tsv file.

## Docs
```bash
python -m scrape_glosbe_dict --help
```
```bash
Usage: python -m scrape_glosbe_dict [OPTIONS] head-word-file

Arguments:
  head-word-file  Head word file, one word/phrase per line, each will be used
                  to fetch corresponding definitons from https://glosbe.com/.
                  [required]

Options:
  -f, --from-lang TEXT  Source language, check https://glosbe.com/ for valid
                        value, e.g. https://glosbe.com/en/zh implies
                        from_lang='en'.  [default: en]
  -t, --to-lang TEXT    Target language, check https://glosbe.com/ for valid
                        value, e.g. https://glosbe.com/en/zh implies
                        to_lang='zh'.  [default: zh]
  -v, --verbose         Show output in the process.
  -V, --version         Show version info and exit.
  --help                Show this message and exit.
```

## Miscellany

* A retry mechanism (via pypi `tenacity`) is built-in to fetch info from glosbe. Refer to the source file for details.
* Local cache (via pypi `joblib`) is used so that you can interrupt anytime and contniue later.
* Scraping is often frowneds upon and sometimes can result in your IP banned from the website. Use this package at your own discretion.
