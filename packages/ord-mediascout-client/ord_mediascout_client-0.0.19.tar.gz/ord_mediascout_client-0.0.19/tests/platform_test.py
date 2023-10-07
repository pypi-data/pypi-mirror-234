import random

import pytest

from ord_mediascout_client import CreatePlatformWebApiDto, ORDMediascoutClient, ORDMediascoutConfig, PlatformType


@pytest.fixture
def client() -> ORDMediascoutClient:
    config = ORDMediascoutConfig()
    return ORDMediascoutClient(config)


# НЕ работает в режиме "get or create", только "create" с новым url, потому url и название генерятся
def test_create_platform(client: ORDMediascoutClient) -> None:
    rnd = random.randrange(111, 999)
    request_data = CreatePlatformWebApiDto(
        name='Test Platform {}'.format(rnd),
        type=PlatformType.Site,
        url='http://www.testplatform{}.ru/'.format(rnd),
        isOwner=False,
    )

    response_data = client.create_platform(request_data)

    assert response_data.id is not None
