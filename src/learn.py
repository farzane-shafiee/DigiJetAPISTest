from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import requests


session = requests.Session()
retry = Retry(connect=3, backoff_factor=1)
adapter = HTTPAdapter(max_retries=retry)
session.mount('https://demo-dknow-api.digikala.com/user/login-register/', adapter)
# session.mount('https://', adapter)
payload = dict(
            phone="555"
        )
rsp= session.post('https://demo-dknow-api.digikala.com/user/login-register/', payload)
print(rsp.json())

