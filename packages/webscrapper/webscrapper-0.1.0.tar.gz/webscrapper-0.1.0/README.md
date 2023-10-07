# Web Scrapper API client for python

This is python client library for https://scrapper.scurra.space/

This module provide 2 functions with same functionality.
get_page and get_page_async for async python.


## Installation

```
pip install webscrapper
```

## Example usage:

```python
from webscrapper.client import get_page

result = get_page(url, api_key="__YOUR_API_KEY__", use_selenium=True)
print(result['html'])
```
