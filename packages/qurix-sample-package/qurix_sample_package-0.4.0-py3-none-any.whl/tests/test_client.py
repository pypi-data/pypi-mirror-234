from qurix.sample.package.client import SomeClient
import pytest


@pytest.fixture
def client() -> SomeClient:
    return SomeClient(name="sample")


def test_client_name(client: SomeClient):
    result = client.name
    assert result == "sample"
