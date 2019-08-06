# pygeckodriver
## Installation:
```
# From PyPI
pip install pygeckodriver
```
## Usage:
```
from selenium import webdriver
from pygeckodriver import geckodriver_path

bs = webdriver.Chrome(executable_path=geckodriver_path)
bs.get('https://www.pypi.org')
```
