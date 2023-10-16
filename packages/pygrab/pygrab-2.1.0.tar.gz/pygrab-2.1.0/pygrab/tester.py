import pygrab
import requests

# ========================================================================================================================================
title = " Get Request "
print(f'{title:=^80}')

res = pygrab.get("https://www.google.com")
try:
    assert isinstance(res, requests.Response)
except Exception as err:
    print(err)

print("="*80, '\n'*3)


# ========================================================================================================================================
title = " Get Request with Tor "
print(f'{title:=^80}')

ip0 = pygrab.get('http://ip-api.com/json').json()['query']
pygrab.Tor.start_tor()
ip1 = pygrab.get('http://ip-api.com/json').json()['query']

res = pygrab.get("https://www.google.com")
try:
    assert isinstance(res, requests.Response)
    assert pygrab.tor_status()
    assert pygrab.Tor.tor_status()
    assert ip0 != ip1
except Exception as err:
    print(err)

pygrab.Tor.end_tor()

print("="*80, '\n'*3)



# ========================================================================================================================================
title = " POST Request with Tor "
print(f'{title:=^80}')

data = {'key': 'value'}
pygrab.Tor.start_tor()
res = pygrab.post("https://httpbin.org/post", data=data)
try:
    assert isinstance(res, requests.Response)
    assert res.json()['form']['key'] == 'value'
except Exception as err:
    print(err)
pygrab.Tor.end_tor()

print("="*80, '\n'*3)

# ========================================================================================================================================
title = " Custom Headers "
print(f'{title:=^80}')

headers = {'User-Agent': 'PyGrab'}
res = pygrab.get("https://httpbin.org/headers", headers=headers)

try:
    assert res.json()['headers']['User-Agent'] == 'PyGrab'
except Exception as err:
    print(err)

print("="*80, '\n'*3)

# ========================================================================================================================================
title = " Reconnect to Tor Network "
print(f'{title:=^80}')

pygrab.Tor.start_tor()
ip0 = pygrab.get('http://ip-api.com/json').json()['query']
pygrab.Tor.start_tor()
ip1 = pygrab.get('http://ip-api.com/json').json()['query']

try:
    assert ip0 != ip1
except Exception as err:
    print(err)
pygrab.Tor.end_tor()

print("="*80, '\n'*3)

# ========================================================================================================================================
title = " JavaScript Site Scraping "
print(f'{title:=^80}')

# Assuming the site requires JavaScript and PyGrab can handle it
res = pygrab.get("https://edhrec.com/", enable_js=True)

try:
    assert "Commander of the Day" in res.text
except Exception as err:
    print(err)
print("="*80, '\n'*3)

# ========================================================================================================================================
title = " Session Handling "
print(f'{title:=^80}')

session = pygrab.Session()
res1 = session.get("https://httpbin.org/cookies/set?name=value")
res2 = session.get("https://httpbin.org/cookies")

try:
    assert res2.json()['cookies']['name'] == 'value'
except Exception as err:
    print(err)

print("="*80, '\n'*3)

# ========================================================================================================================================
title = " JavaScript Site Scraping w Tor "
print(f'{title:=^80}')

pygrab.Tor.start_tor()
# Assuming the site requires JavaScript and PyGrab can handle it
res = pygrab.get("https://edhrec.com/", enable_js=True)

try:
    assert "Commander of the Day" in res.text
except Exception as err:
    print(err)
print("="*80, '\n'*3)


# ========================================================================================================================================
title = " Session Handling w Tor "
print(f'{title:=^80}')

session = pygrab.Session()
res1 = session.get("https://httpbin.org/cookies/set?name=value")
res2 = session.get("https://httpbin.org/cookies")

try:
    assert res2.json()['cookies']['name'] == 'value'
except Exception as err:
    print(err)
print("="*80, '\n'*3)

# ========================================================================================================================================
title = " HEAD Request with Tor "
print(f'{title:=^80}')

res_head = pygrab.head("https://www.google.com")
res_get = pygrab.get("https://www.google.com")

try:
    assert isinstance(res_head, requests.Response)
    assert res_head.status_code == 200 or res_head.status_code == 403
    # Since it's a HEAD request, there should be no content
    if res_head.status_code == 403: assert res_head.content == b''
except Exception as err:
    print(err)

print("="*80, '\n'*3)


# ========================================================================================================================================
title = " Scan ip with Tor "
print(f'{title:=^80}')

res = pygrab.scan_ip('10.0.0.1')
lst = pygrab.scan_iprange('10.0.0.1-225')

pygrab.Tor.end_tor()

print("="*80, '\n'*3)


# ========================================================================================================================================
title = " Session.get() "
print(f'{title:=^80}')

s1 = requests.Session()
s2 = pygrab.Session()

try:
    assert s1.get('https://www.google.com').text[:100] == s2.get('https://www.google.com').text[:100]
except Exception as err:
    print(err)
print("="*80, '\n'*3)

# ========================================================================================================================================
title = " Session.post() "
print(f'{title:=^80}')

s1 = requests.Session()
s2 = pygrab.Session()

data = {'key': 'value'}
url = 'https://httpbin.org/post'

try:
    assert s1.post(url, data=data).text == s2.post(url, data=data).text
except Exception as err:
    print(err)

print("="*80, '\n'*3)


# ========================================================================================================================================
title = " Session.put() "
print(f'{title:=^80}')

s1 = requests.Session()
s2 = pygrab.Session()

data = {'key': 'value'}
url = 'https://httpbin.org/put'

try:
    assert s1.put(url, data=data).text == s2.put(url, data=data).text
except Exception as err:
    print(err)
print("="*80, '\n'*3)



# ========================================================================================================================================
title = " Session.delete() "
print(f'{title:=^80}')

s1 = requests.Session()
s2 = pygrab.Session()

url = 'https://httpbin.org/delete'

try:
    assert s1.delete(url).text == s2.delete(url).text
except Exception as err:
    print(err)
print("="*80, '\n'*3)


# ========================================================================================================================================
title = " Session with Custom Headers "
print(f'{title:=^80}')

s1 = requests.Session()
s2 = pygrab.Session()

headers = {'User-Agent': 'my-app'}
s1.headers.update(headers)
s2.headers.update(headers)

url = 'https://www.google.com'
try:
    assert s1.get(url).text[:100] == s2.get(url).text[:100]
except Exception as err:
    print(err)

print("="*80, '\n'*3)

# ========================================================================================================================================
title = " Session.get() with Tor "
print(f'{title:=^80}')

s1 = requests.Session()
s2 = pygrab.Session()

pygrab.Tor.start_tor()

ip0 = s1.get('http://ip-api.com/json').json()['query']
ip1 = s2.get('http://ip-api.com/json').json()['query']

try:
    assert ip0 != ip1
except Exception as err:
    print(err)

pygrab.Tor.end_tor()

print("="*80, '\n'*3)