import urllib.request
import pytest


def test_url_not_infected():
    url = "http://127.0.0.1:5000/urlinfo/1/infectedsite.org:3000/abcd"
    r = urllib.request.urlopen(url).read()
    assert r == b'{"query_infected":false,"status":200,"url_infected":false,"url_unsafe":false}\n'
    print(urllib.request.urlopen(url).read())

def test_url_infected():
    url = "http://127.0.0.1:5000/urlinfo/1/www.infected1.com/malwarequery=2"
    r = urllib.request.urlopen(url).read()
    assert r == b'{"query_infected":true,"status":200,"url_infected":false,"url_unsafe":true}\n'
    print(urllib.request.urlopen(url).read())

