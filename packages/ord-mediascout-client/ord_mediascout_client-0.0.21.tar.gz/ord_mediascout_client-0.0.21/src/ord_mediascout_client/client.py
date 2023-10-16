import logging
from typing import Any, Optional, Type

import requests
from pydantic.error_wrappers import ValidationError
from pydantic.main import BaseModel
from pydantic.tools import parse_raw_as
from requests.auth import HTTPBasicAuth

from .config import ORDMediascoutConfig
from .feed_models import (
    CreateContainerWebApiDto,
    CreateFeedElementsBulkWebApiDto,
    CreateFeedElementsWebApiDto,
    EditFeedElementWebApiDto,
    GetContainerWebApiDto,
    GetFeedElementsBulkInfo,
    GetFeedElementsWebApiDto,
    ResponseContainerWebApiDto,
    ResponseCreateFeedElementsBulkWebApiDto,
    ResponseEditFeedElementWebApiDto,
    ResponseFeedElementsWebApiDto,
    ResponseGetContainerWebApiDto,
    ResponseGetFeedElementsBulkInfo,
    ResponseGetFeedElementsWebApiDto,
)
from .models import (
    BadRequestWebApiDto,
    ClearInvoiceDataWebApiDto,
    ClientWebApiDto,
    CreateClientWebApiDto,
    CreateCreativeWebApiDto,
    CreatedCreativeWebApiDto,
    CreateFinalContractWebApiDto,
    CreateInitialContractWebApiDto,
    CreateInvoicelessStatisticsWebApiDto,
    CreateInvoiceWebApiDto,
    CreateOuterContractWebApiDto,
    CreatePlatformWebApiDto,
    CreativeGroupWebApiDto,
    CreativeWebApiDto,
    EditCreativeWebApiDto,
    EditFinalContractWebApiDto,
    EditInitialContractWebApiDto,
    EditInvoiceDataWebApiDto,
    EditInvoiceStatisticsWebApiDto,
    EditOuterContractWebApiDto,
    EditPlatformWebApiDto,
    EntityIdWebApiDto,
    FinalContractWebApiDto,
    GetClientsWebApiDto,
    GetCreativeGroupsWebApiDto,
    GetCreativesWebApiDto,
    GetFinalContractsWebApiDto,
    GetInitialContractsWebApiDto,
    GetInvoicelessPeriodsWebApiDto,
    GetInvoicesWebApiDto,
    GetOuterContractsWebApiDto,
    InitialContractWebApiDto,
    InvoicelessStatisticsWebApiDto,
    InvoiceSummaryWebApiDto,
    InvoiceWebApiDto,
    OuterContractWebApiDto,
    PlatformCardWebApiDto,
    SelfPromotionContractWebApiDto,
    SupplementInvoiceWebApiDto,
)


class APIError(Exception):
    pass


class BadResponseError(APIError):
    def __init__(self, response: requests.Response, error: Optional[BadRequestWebApiDto] = None):
        super().__init__(error and error.errorType or f'Bad response from API: {response.status_code}')
        self.response = response
        self.error = error


class UnexpectedResponseError(APIError):
    def __init__(self, response: requests.Response):
        super().__init__(f'Unexpected response with STATUS_CODE: {response.status_code}')
        self.response = response


class ORDMediascoutClient:
    def __init__(self, config: ORDMediascoutConfig):
        self.config = config
        self.auth = HTTPBasicAuth(self.config.username, self.config.password)
        self.headers = {'Content-Type': 'application/json-patch+json'}
        self.logger = logging.getLogger('ord_mediascout_client')

    def _call(
        self,
        method: str,
        url: str,
        obj: Optional[BaseModel] = None,
        return_type: Optional[Type[Any]] = None,
        **kwargs: dict[str, Any],
    ) -> Any:
        response = requests.request(
            method, f'{self.config.url}{url}', data=obj and obj.json(), auth=self.auth, headers=self.headers, **kwargs
        )

        self.logger.debug(
            f'API call: {method} {url}\n'
            f'Headers: {self.headers}\n'
            f'Body: {obj and obj.json(indent=4)}\n'
            f'Response: {response.status_code}\n'
            f'{response.text}'
        )
        match response.status_code:
            case 400 | 401:
                try:
                    bad_response = BadRequestWebApiDto.parse_raw(response.text)
                except ValidationError as e:
                    raise UnexpectedResponseError(response) from e
                raise BadResponseError(response, bad_response)
            case 500:
                raise BadResponseError(response)
            case 200 | 201:
                if return_type is not None:
                    try:
                        return parse_raw_as(return_type, response.text or '{}')
                    except ValidationError as e:
                        raise UnexpectedResponseError(response) from e
            case _:
                raise UnexpectedResponseError(response)

    # Clients
    def create_client(self, client: CreateClientWebApiDto) -> ClientWebApiDto:
        client: ClientWebApiDto = self._call(
            'post', f'{self.config.api_url_prefix}/Clients/CreateClient', client, ClientWebApiDto
        )
        return client

    def get_clients(self, parameters: GetClientsWebApiDto) -> list[ClientWebApiDto]:
        clients: list[ClientWebApiDto] = self._call(
            'post', f'{self.config.api_url_prefix}/Clients/GetClients', parameters, list[ClientWebApiDto]
        )
        return clients

    # Contracts
    def create_initial_contract(self, contract: CreateInitialContractWebApiDto) -> InitialContractWebApiDto:
        contract: InitialContractWebApiDto = self._call(
            'post', f'{self.config.api_url_prefix}/Contracts/CreateInitialContract', contract, InitialContractWebApiDto
        )
        return contract

    def edit_initial_contract(self, contract: EditInitialContractWebApiDto) -> InitialContractWebApiDto:
        contract: InitialContractWebApiDto = self._call(
            'post', f'{self.config.api_url_prefix}/Contracts/EditInitialContract', contract, InitialContractWebApiDto
        )
        return contract

    def get_initial_contracts(self, parameters: GetInitialContractsWebApiDto) -> list[InitialContractWebApiDto]:
        contracts: list[InitialContractWebApiDto] = self._call(
            'post',
            f'{self.config.api_url_prefix}/Contracts/GetInitialContracts',
            parameters,
            list[InitialContractWebApiDto],
        )
        return contracts

    def create_final_contract(self, contract: CreateFinalContractWebApiDto) -> FinalContractWebApiDto:
        contract: FinalContractWebApiDto = self._call(
            'post', f'{self.config.api_url_prefix}/Contracts/CreateFinalContract', contract, FinalContractWebApiDto
        )
        return contract

    def edit_final_contract(self, contract: EditFinalContractWebApiDto) -> FinalContractWebApiDto:
        contract: FinalContractWebApiDto = self._call(
            'post', f'{self.config.api_url_prefix}/Contracts/EditFinalContract', contract, FinalContractWebApiDto
        )
        return contract

    def get_final_contracts(self, parameters: GetFinalContractsWebApiDto) -> list[FinalContractWebApiDto]:
        contracts: list[FinalContractWebApiDto] = self._call(
            'post',
            f'{self.config.api_url_prefix}/Contracts/GetFinalContracts',
            parameters,
            list[FinalContractWebApiDto],
        )
        return contracts

    def create_outer_contract(self, contract: CreateOuterContractWebApiDto) -> OuterContractWebApiDto:
        contract: OuterContractWebApiDto = self._call(
            'post', f'{self.config.api_url_prefix}/Contracts/CreateOuterContract', contract, OuterContractWebApiDto
        )
        return contract

    def edit_outer_contract(self, contract: EditOuterContractWebApiDto) -> OuterContractWebApiDto:
        contract: OuterContractWebApiDto = self._call(
            'post', f'{self.config.api_url_prefix}/Contracts/EditOuterContract', contract, OuterContractWebApiDto
        )
        return contract

    def get_outer_contracts(self, parameters: GetOuterContractsWebApiDto) -> list[OuterContractWebApiDto]:
        contracts: list[OuterContractWebApiDto] = self._call(
            'post',
            f'{self.config.api_url_prefix}/Contracts/GetOuterContracts',
            parameters,
            list[OuterContractWebApiDto],
        )
        return contracts

    def create_self_promotion_contract(
        self, contract: SelfPromotionContractWebApiDto
    ) -> SelfPromotionContractWebApiDto:
        contract: SelfPromotionContractWebApiDto = self._call(
            'post',
            f'{self.config.api_url_prefix}/Contracts/CreateSelfPromotionContract',
            contract,
            SelfPromotionContractWebApiDto,
        )
        return contract

    def get_self_promotion_contracts(self) -> list[SelfPromotionContractWebApiDto]:
        contracts: list[SelfPromotionContractWebApiDto] = self._call(
            'post',
            f'{self.config.api_url_prefix}/Contracts/GetSelfPromotionContracts',
            None,
            list[SelfPromotionContractWebApiDto],
        )
        return contracts

    # Creatives
    def create_creative(self, creative: CreateCreativeWebApiDto) -> CreatedCreativeWebApiDto:
        creative: CreatedCreativeWebApiDto = self._call(
            'post', f'{self.config.api_url_prefix}/creatives/CreateCreative', creative, CreatedCreativeWebApiDto
        )
        return creative

    def edit_creative(self, creative: EditCreativeWebApiDto) -> CreativeWebApiDto:
        updated_creative: CreativeWebApiDto = self._call(
            'post', f'{self.config.api_url_prefix}/creatives/EditCreative', creative, CreativeWebApiDto
        )
        return updated_creative

    def get_creatives(self, parameters: GetCreativesWebApiDto) -> list[CreativeWebApiDto]:
        creatives: list[CreativeWebApiDto] = self._call(
            'post', f'{self.config.api_url_prefix}/creatives/GetCreatives', parameters, list[CreativeWebApiDto]
        )
        return creatives

    # Creative Group
    def edit_creative_group(self, creative_group: CreativeGroupWebApiDto) -> CreativeGroupWebApiDto:
        updated_creative_group: CreativeGroupWebApiDto = self._call(
            'post', f'{self.config.api_url_prefix}/creatives/EditCreativeGroup', creative_group, CreativeGroupWebApiDto
        )
        return updated_creative_group

    def get_creative_groups(self, parameters: GetCreativeGroupsWebApiDto) -> list[CreativeGroupWebApiDto]:
        creative_groups: list[CreativeGroupWebApiDto] = self._call(
            'post',
            f'{self.config.api_url_prefix}/creatives/GetCreativeGroups',
            parameters,
            list[CreativeGroupWebApiDto],
        )
        return creative_groups

    # Feeds
    def create_container(self, container: CreateContainerWebApiDto) -> ResponseContainerWebApiDto:
        container: ResponseContainerWebApiDto = self._call(
            'post', '/webapi/creatives/CreateContainer', container, ResponseContainerWebApiDto
        )
        return container

    def get_containers(self, parameters: GetContainerWebApiDto) -> list[ResponseGetContainerWebApiDto]:
        containers: list[ResponseGetContainerWebApiDto] = self._call(
            'post', '/webapi/creatives/GetContainers', parameters, list[ResponseGetContainerWebApiDto]
        )
        return containers

    def create_feed_elements(self, feed_elements: CreateFeedElementsWebApiDto) -> list[ResponseFeedElementsWebApiDto]:
        feed_elements: list[ResponseFeedElementsWebApiDto] = self._call(
            'post', '/webapi/creatives/CreateFeedElements', feed_elements, list[ResponseFeedElementsWebApiDto]
        )
        return feed_elements

    def edit_feed_element(self, feed_element: EditFeedElementWebApiDto) -> ResponseEditFeedElementWebApiDto:
        feed_element: ResponseEditFeedElementWebApiDto = self._call(
            'post', '/webapi/creatives/EditFeedElement', feed_element, ResponseEditFeedElementWebApiDto
        )
        return feed_element

    def get_feed_elements(self, parameters: GetFeedElementsWebApiDto) -> list[ResponseGetFeedElementsWebApiDto]:
        feed_elements: list[ResponseGetFeedElementsWebApiDto] = self._call(
            'post', '/webapi/creatives/GetFeedElements', parameters, list[ResponseGetFeedElementsWebApiDto]
        )
        return feed_elements

    def create_feed_elements_bulk(
        self, feed_elements_bulk: CreateFeedElementsBulkWebApiDto
    ) -> ResponseCreateFeedElementsBulkWebApiDto:
        feed_elements_bulk: ResponseCreateFeedElementsBulkWebApiDto = self._call(
            'post',
            '/webapi/creatives/CreateFeedElementsBulk',
            feed_elements_bulk,
            ResponseCreateFeedElementsBulkWebApiDto,
        )
        return feed_elements_bulk

    def get_feed_elements_bulk_info(
        self, feed_elements_bulk_info: GetFeedElementsBulkInfo
    ) -> ResponseGetFeedElementsBulkInfo:
        feed_elements_bulk_info: ResponseGetFeedElementsBulkInfo = self._call(
            'post',
            '/webapi/creatives/GetFeedElementsBulkInfo',
            feed_elements_bulk_info,
            ResponseGetFeedElementsBulkInfo,
        )
        return feed_elements_bulk_info

    # Invoices
    def create_invoice(self, invoice: CreateInvoiceWebApiDto) -> EntityIdWebApiDto:
        entity: EntityIdWebApiDto = self._call(
            'post', f'{self.config.api_url_prefix}/Invoices/CreateInvoice', invoice, EntityIdWebApiDto
        )
        return entity

    def edit_invoice(self, invoice: EditInvoiceDataWebApiDto) -> InvoiceWebApiDto:
        invoice: InvoiceWebApiDto = self._call(
            'post', f'{self.config.api_url_prefix}/Invoices/EditInvoice', invoice, InvoiceWebApiDto
        )
        return invoice

    def overwrite_invoice(self, invoice: EditInvoiceStatisticsWebApiDto) -> None:
        self._call('post', f'{self.config.api_url_prefix}/Invoices/OverwriteInvoice', invoice)

    def clear_invoice(self, invoice: ClearInvoiceDataWebApiDto) -> None:
        self._call('post', f'{self.config.api_url_prefix}/Invoices/ClearInvoice', invoice)

    def supplement_invoice(self, invoice: SupplementInvoiceWebApiDto) -> EntityIdWebApiDto:
        entity: EntityIdWebApiDto = self._call(
            'post', f'{self.config.api_url_prefix}/Invoices/SupplementInvoice', invoice, EntityIdWebApiDto
        )
        return entity

    def get_invoices(self, parameters: GetInvoicesWebApiDto) -> list[InvoiceWebApiDto]:
        invoices: list[InvoiceWebApiDto] = self._call(
            'post', f'{self.config.api_url_prefix}/Invoices/GetInvoices', parameters, list[InvoiceWebApiDto]
        )
        return invoices

    def get_invoice_summary(self, entity: EntityIdWebApiDto) -> InvoiceSummaryWebApiDto:
        invoice_summary: InvoiceSummaryWebApiDto = self._call(
            'post', f'{self.config.api_url_prefix}/Invoices/GetInvoiceSummary', entity, InvoiceSummaryWebApiDto
        )
        return invoice_summary

    def confirm_invoice(self, entity: EntityIdWebApiDto) -> None:
        self._call('post', f'{self.config.api_url_prefix}/Invoices/ConfirmInvoice', entity)

    def delete_invoice(self, entity: EntityIdWebApiDto) -> None:
        self._call('post', f'{self.config.api_url_prefix}/Invoices/DeleteInvoices', entity)

    # WebApiPlatform
    def create_platform(self, platform: CreatePlatformWebApiDto) -> EntityIdWebApiDto:
        entity: EntityIdWebApiDto = self._call(
            'post', f'{self.config.api_url_prefix}/Platforms/CreatePlatform', platform, EntityIdWebApiDto
        )
        return entity

    def edit_platform(self, platform: EditPlatformWebApiDto) -> PlatformCardWebApiDto:
        updated_platform: PlatformCardWebApiDto = self._call(
            'post', f'{self.config.api_url_prefix}/Platforms/EditPlatform', platform, PlatformCardWebApiDto
        )
        return updated_platform

    # Statistics
    def create_statistics(self, statistics: CreateInvoicelessStatisticsWebApiDto) -> None:
        statistics: None = self._call(
            'post', f'{self.config.api_url_prefix}/Statistics/CreateStatistics', statistics, None
        )
        return statistics

    def get_statistics(self, parameters: GetInvoicelessPeriodsWebApiDto) -> list[InvoicelessStatisticsWebApiDto]:
        statistics: list[InvoicelessStatisticsWebApiDto] = self._call(
            'post',
            f'{self.config.api_url_prefix}/Statistics/GetStatistics',
            parameters,
            list[InvoicelessStatisticsWebApiDto],
        )
        return statistics

    # PING
    def ping(self) -> bool:
        tmp_auth, self.auth = self.auth, None
        self._call('get', '/webapi/Ping')
        self.auth = tmp_auth
        return True

    def ping_auth(self) -> bool:
        self._call('get', '/webapi/PingAuth')
        return True
