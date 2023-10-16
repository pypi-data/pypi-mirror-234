# pychromedriver
## Installation:
```
# From PyPI
pip install pychromedriver
```
## Usage:
```
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from pychromedriver import chromedriver_path

bs = webdriver.Chrome(service=Service(chromedriver_path))
bs.get('https://www.pypi.org')
```
