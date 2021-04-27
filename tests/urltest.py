import urllib.request
import pytest


def test_invalid_url():
    """
    Test that error message is shown when invalid url is given
    """
    url = "http://127.0.0.1:5000/urlinfo/1/infectedsite:3000/"
    r = urllib.request.urlopen(url).read()
    assert r == b'Hostname under test not Valid'

def test_url_not_infected():
    """
    Test that the url is not infected
    """
    url = "http://127.0.0.1:5000/urlinfo/1/infectedsite.org:3000/abcd"
    r = urllib.request.urlopen(url).read()
    assert r == b'{"host_infected":false,"host_unsafe":false,"status":200,"url_infected":false}\n'

def test_url_infected():
    """
    Test that url is infected. All parts of url are infected
    """
    url = "http://127.0.0.1:5000/urlinfo/1/www.infected1.com:4000/malwarequery=2"
    r = urllib.request.urlopen(url).read()
    assert r == b'{"host_infected":true,"host_unsafe":true,"status":200,"url_infected":true}\n'

def test_unsafe_no_port_url():
    """
    Test that if port is not specified, but hostname is in list of infected host ids,
    host_infected is true
    """
    url = "http://127.0.0.1:5000/urlinfo/1/www.infected1.com/malwarequery=2"
    r = urllib.request.urlopen(url).read()
    assert r == b'{"host_infected":true,"host_unsafe":true,"status":200,"url_infected":true}\n'

def test_unsafe_host_port_not_query():
    """
    Test host and port are in list of infected but, whole url is not.
    In this case url_infected is set to false but host_infected is true
    """
    url = "http://127.0.0.1:5000/urlinfo/1/www.infected1.com/abcd"
    r = urllib.request.urlopen(url).read()
    assert r == b'{"host_infected":true,"host_unsafe":true,"status":200,"url_infected":false}\n'

def test_no_query():
    """
    Test if query is not specified.
    In this case url_infected is set to false but host_infected is true if infected.
    """
    url = "http://127.0.0.1:5000/urlinfo/1/www.infected1.com:4000/"
    r = urllib.request.urlopen(url).read()
    assert r == b'{"host_infected":true,"host_unsafe":true,"status":200,"url_infected":false}\n'

def test_unsafe_host_safe_port():
    """
    Test that host is infected but port is not in list of infected ports.
    In this case host_unsafe is true, host_infected is false.
    """
    url = "http://127.0.0.1:5000/urlinfo/1/www.infected1.com:8000/malwarequery=2"
    r = urllib.request.urlopen(url).read()
    assert r == b'{"host_infected":false,"host_unsafe":true,"status":200,"url_infected":true}\n'

