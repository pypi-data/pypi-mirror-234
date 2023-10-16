# ua-generator

A random user-agent generator for Python >= 3.6

# Features
* No external user-agent list. No downloads.
* Templates are hardcoded into the code.
* Platform and browser versions are based on real releases.
* Client hints (Sec-CH-UA fields).

# Installing
```bash
pip3 install -U yan-random-useragent
```

# Basic usage
```python
import generate_random_ua

ua = generate_random_ua()
print(ua) # Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/15.2 Safari/604.1.38
```
# Author
Jasson Nguyen (admin@taocuaba.com)