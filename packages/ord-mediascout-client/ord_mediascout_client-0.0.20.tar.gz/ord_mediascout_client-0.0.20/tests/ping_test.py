import pytest

from ord_mediascout_client import ORDMediascoutClient, ORDMediascoutConfig


@pytest.fixture
def client() -> ORDMediascoutClient:
    config = ORDMediascoutConfig()
    return ORDMediascoutClient(config)


def test_ping(client: ORDMediascoutClient) -> None:
    assert client.ping()


def test_ping_auth(client: ORDMediascoutClient) -> None:
    assert client.ping_auth()
