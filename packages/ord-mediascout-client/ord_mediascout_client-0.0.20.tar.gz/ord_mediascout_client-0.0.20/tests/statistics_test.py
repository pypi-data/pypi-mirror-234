import pytest

from ord_mediascout_client import (
    CreateInvoicelessStatisticsWebApiDto,
    GetInvoicelessPeriodsWebApiDto,
    InvoicelessStatisticsByPlatformsItemWebApiDto,
    ORDMediascoutClient,
    ORDMediascoutConfig,
)

# Setup test data
_erid = 'Kra23f3QL'
_platformUrl = 'http://www.testplatform.ru'
_platformName = 'Test Platform 1'
_platformType = 'Site'
_platformOwnedByAgency = False
_impsPlan = 10000
_impsFact = 100
_startDatePlan = '2023-06-01'
_startDateFact = '2023-06-01'
_endDatePlan = '2023-06-20'
_endDateFact = '2023-06-20'
_amount = 50000
_price = 5
_vatIncluded = True


@pytest.fixture
def client() -> ORDMediascoutClient:
    config = ORDMediascoutConfig()
    return ORDMediascoutClient(config)


def test_create_statistics(client: ORDMediascoutClient) -> None:
    request_data = CreateInvoicelessStatisticsWebApiDto(
        statistics=[
            InvoicelessStatisticsByPlatformsItemWebApiDto(
                erid=_erid,
                platformUrl=_platformUrl,
                platformName=_platformName,
                platformType=_platformType,
                platformOwnedByAgency=_platformOwnedByAgency,
                impsPlan=_impsPlan,
                impsFact=_impsFact,
                startDatePlan=_startDatePlan,
                startDateFact=_startDateFact,
                endDatePlan=_endDatePlan,
                endDateFact=_endDateFact,
                amount=_amount,
                price=_price,
                vatIncluded=_vatIncluded,
            )
        ]
    )

    response_data = client.create_statistics(request_data)

    assert response_data is None


def test_get_statistics(client: ORDMediascoutClient) -> None:
    request_data = GetInvoicelessPeriodsWebApiDto(dateStart='2023-01-01', dateEnd='2023-06-21', status='Creating')

    response_data = client.get_statistics(request_data)

    for statistic in response_data:
        assert statistic.id is not None
