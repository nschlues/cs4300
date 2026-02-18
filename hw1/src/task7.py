## Package Management
## Nathan Schluessler
import requests

r = requests.get('https://httpbin.org/basic-auth/user/pass', auth=('user', 'pass'))
print(r.status_code)