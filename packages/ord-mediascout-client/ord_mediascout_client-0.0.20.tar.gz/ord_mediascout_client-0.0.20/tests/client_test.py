import pytest

from ord_mediascout_client import (
    ClientRelationshipType,
    CounterpartyStatus,
    CreateClientWebApiDto,
    GetClientsWebApiDto,
    LegalForm,
    ORDMediascoutClient,
    ORDMediascoutConfig,
)


@pytest.fixture
def client() -> ORDMediascoutClient:
    config = ORDMediascoutConfig()
    return ORDMediascoutClient(config)


def test_create_client(client: ORDMediascoutClient) -> None:
    request_data = CreateClientWebApiDto(
        createMode=ClientRelationshipType.DirectClient,
        legalForm=LegalForm.JuridicalPerson,
        inn='7720805643',
        name='Тест клиент2',
        mobilePhone='+79161234567',
        epayNumber='12333',
        regNumber='54556',
        oksmNumber='44563',
    )

    response_data = client.create_client(request_data)

    assert request_data.name == response_data.name
    assert request_data.inn == response_data.inn
    # assert request_data.mobilePhone == response_data.mobilePhone
    # assert request_data.epayNumber == response_data.epayNumber
    # assert request_data.regNumber == response_data.regNumber
    # assert request_data.oksmNumber == response_data.oksmNumber
    # assert request_data.createMode == response_data.createMode
    assert request_data.legalForm == response_data.legalForm
    assert response_data.id is not None
    assert response_data.status == CounterpartyStatus.Active


def test_get_clients(client: ORDMediascoutClient) -> None:
    request_data = GetClientsWebApiDto(status=CounterpartyStatus.Active)

    response_data = client.get_clients(request_data)

    for cli in response_data:
        assert cli.id is not None
