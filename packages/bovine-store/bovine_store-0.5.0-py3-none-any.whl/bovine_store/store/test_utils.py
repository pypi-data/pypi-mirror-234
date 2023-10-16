from .utils import domain_from_host


def test_domain_from_host():
    assert domain_from_host(None) == "localhost"
    assert domain_from_host("https://example.com") == "example.com"
