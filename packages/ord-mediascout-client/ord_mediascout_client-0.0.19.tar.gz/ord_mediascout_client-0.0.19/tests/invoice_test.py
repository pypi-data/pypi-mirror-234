import random

import pytest

from ord_mediascout_client import (
    CreateInvoiceWebApiDto,
    GetInvoicesWebApiDto,
    InvoiceInitialContractItemWebApiDto,
    InvoicePartyRole,
    InvoiceStatisticsByPlatformsItemWebApiDto,
    InvoiceStatus,
    ORDMediascoutClient,
    ORDMediascoutConfig,
    PlatformType,
)


@pytest.fixture
def client() -> ORDMediascoutClient:
    config = ORDMediascoutConfig()
    return ORDMediascoutClient(config)


# НЕ работает в режиме "get or create", только "create" с новым номером, потому number генерится
def test_create_invoice(client: ORDMediascoutClient) -> None:
    request_data = CreateInvoiceWebApiDto(
        number='INV-{}'.format(random.randrange(11111111, 99999999)),
        date='2023-03-20',
        contractorRole=InvoicePartyRole.Rr,
        clientRole=InvoicePartyRole.Ra,
        amount=20000.00,
        vatIncluded=True,
        startDate='2023-03-23',
        endDate='2023-03-23',
        finalContractId='CTiwhIpoQ_F0OEPpKj8vWKGg',
        initialContractsData=[
            InvoiceInitialContractItemWebApiDto(
                initialContractId='CTKLAzsvgYREmK0unGXLsCTg', amount=1000.00, vatIncluded=True
            )
        ],
        statisticsByPlatforms=[
            InvoiceStatisticsByPlatformsItemWebApiDto(
                initialContractId='CTKLAzsvgYREmK0unGXLsCTg',
                erid='Pb3XmBtzsxtPgHUnh4hEFkxvF9Ay6CSGDzFnCHt',
                platformUrl='http://www.testplatform.ru',
                platformName='Test Platform 1',
                platformType=PlatformType.Site,
                platformOwnedByAgency=False,
                impsPlan=10000,
                impsFact=10,
                startDatePlan='2023-04-03',
                startDateFact='2023-04-03',
                endDatePlan='2023-04-03',
                endDateFact='2023-04-03',
                amount=1000.00,
                price=0.5,
                vatIncluded=True,
            )
        ],
    )

    response_data = client.create_invoice(request_data)

    assert response_data.id is not None


def test_get_invoices(client: ORDMediascoutClient) -> None:
    request_data = GetInvoicesWebApiDto(status=InvoiceStatus.Active)

    response_data = client.get_invoices(request_data)

    for invoice in response_data:
        assert invoice.id is not None
