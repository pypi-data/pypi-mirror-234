from __future__ import annotations

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Extra

from .models import CampaignType, CreativeForm, capitalize


class ErirRequestType(Enum):
    First = 'First'
    Second = 'Second'


class ErirValidationErrorWebApiDto(BaseModel):
    class Config:
        extra = Extra.forbid
        alias_generator = capitalize
        allow_population_by_field_name = True

    stage: Optional[ErirRequestType] = None
    code: Optional[str] = None
    message: Optional[str] = None
    responseDt: Optional[str] = None


class TargetAudienceParamsWebApiDto(BaseModel):
    class Config:
        extra = Extra.forbid
        alias_generator = capitalize
        allow_population_by_field_name = True

    geo: Optional[str] = None


class CreateContainerWebApiDto(BaseModel):
    class Config:
        extra = Extra.forbid
        alias_generator = capitalize
        allow_population_by_field_name = True

    feedId: Optional[str] = None
    feedNativeCustomerId: Optional[str] = None
    finalContractId: Optional[str] = None
    initialContractId: Optional[str] = None
    name: Optional[str] = None
    nativeCustomerId: Optional[str] = None
    type: Optional[CampaignType] = None
    form: Optional[CreativeForm] = None
    targetAudience: Optional[str] = None
    targetAudienceParams: Optional[TargetAudienceParamsWebApiDto] = None
    description: Optional[str] = None
    isNative: Optional[bool] = None
    isSocial: Optional[bool] = None
    okvedCodes: Optional[List[str]] = None


class ResponseContainerWebApiDto(CreateContainerWebApiDto):
    id: Optional[str] = None
    erid: Optional[str] = None
    feedName: Optional[str] = None
    status: Optional[str] = None
    erirValidationError: Optional[ErirValidationErrorWebApiDto] = None


class GetContainerWebApiDto(BaseModel):
    class Config:
        extra = Extra.forbid
        alias_generator = capitalize
        allow_population_by_field_name = True

    id: Optional[str] = None
    nativeCustomerId: Optional[str] = None
    erid: Optional[str] = None
    feedNativeCustomerId: Optional[str] = None
    initialContractId: Optional[str] = None
    initialContractNumber: Optional[str] = None
    finalContractId: Optional[str] = None
    finalContractNumber: Optional[str] = None
    status: Optional[str] = None


class ResponseGetContainerWebApiDto(BaseModel):
    class Config:
        extra = Extra.forbid
        alias_generator = capitalize
        allow_population_by_field_name = True

    id: Optional[str] = None
    nativeCustomerId: Optional[str] = None
    erid: Optional[str] = None
    name: Optional[str] = None
    deedId: Optional[str] = None
    feedNativeCustomerId: Optional[str] = None
    feedName: Optional[str] = None
    finalContractId: Optional[str] = None
    initialContractId: Optional[str] = None
    status: Optional[str] = None
    type: Optional[str] = None
    form: Optional[str] = None
    targetAudience: Optional[str] = None
    targetAudienceParams: Optional[str] = None
    description: Optional[str] = None
    isNative: Optional[str] = None
    isSocial: Optional[str] = None
    okvedCodes: Optional[str] = None


class FeedElementMediaDataItem(BaseModel):
    class Config:
        extra = Extra.forbid
        alias_generator = capitalize
        allow_population_by_field_name = True

    fileName: Optional[str] = None
    fileContentBase64: Optional[str] = None
    srcUrl: Optional[str] = None
    description: Optional[str] = None
    isArchive: Optional[bool] = None


class FeedElementTextDataItem(BaseModel):
    class Config:
        extra = Extra.forbid
        alias_generator = capitalize
        allow_population_by_field_name = True

    textData: Optional[str] = None


class FeedElementWebApiDto(BaseModel):
    class Config:
        extra = Extra.forbid
        alias_generator = capitalize
        allow_population_by_field_name = True

    feedId: Optional[str] = None
    nativeCustomerId: Optional[str] = None
    description: Optional[str] = None
    advertiserUrls: Optional[List[str]] = None
    mediaData: Optional[List[FeedElementMediaDataItem]] = None
    textData: Optional[List[FeedElementTextDataItem]] = None


class CreateFeedElementsWebApiDto(BaseModel):
    class Config:
        extra = Extra.forbid
        alias_generator = capitalize
        allow_population_by_field_name = True

    feedId: Optional[str] = None
    feedName: Optional[str] = None
    feedElements: Optional[List[FeedElementWebApiDto]] = None
    feedNativeCustomerId: Optional[str] = None


class ResponseFeedElementsWebApiDto(BaseModel):
    class Config:
        extra = Extra.forbid
        alias_generator = capitalize
        allow_population_by_field_name = True

    id: Optional[str] = None
    nativeCustomerId: Optional[str] = None
    feedId: Optional[str] = None
    feedNativeCustomerId: Optional[str] = None
    feedName: Optional[str] = None
    status: Optional[str] = None
    description: Optional[str] = None
    advertiserUrls: Optional[List[str]] = None
    erirValidationError: Optional[ErirValidationErrorWebApiDto] = None
    clickId: Optional[str] = None


class EditFeedElementWebApiDto(BaseModel):
    class Config:
        extra = Extra.forbid
        alias_generator = capitalize
        allow_population_by_field_name = True

    id: Optional[str] = None
    nativeCustomerId: Optional[str] = None
    feedId: Optional[str] = None
    feedNativeCustomerId: Optional[str] = None
    feedName: Optional[str] = None
    description: Optional[str] = None
    advertiserUrls: Optional[List[str]] = None
    mediaData: Optional[List[FeedElementMediaDataItem]] = None
    textData: Optional[List[FeedElementTextDataItem]] = None


class ResponseEditFeedElementWebApiDto(BaseModel):
    class Config:
        extra = Extra.forbid
        alias_generator = capitalize
        allow_population_by_field_name = True

    id: Optional[str] = None
    nativeCustomerId: Optional[str] = None
    feedId: Optional[str] = None
    feedNativeCustomerId: Optional[str] = None
    feedName: Optional[str] = None
    status: Optional[str] = None
    description: Optional[str] = None
    advertiserUrls: Optional[str] = None


class GetFeedElementsWebApiDto(BaseModel):
    class Config:
        extra = Extra.forbid
        alias_generator = capitalize
        allow_population_by_field_name = True

    id: Optional[str] = None
    nativeCustomerId: Optional[str] = None
    feedNativeCustomerId: Optional[str] = None
    status: Optional[str] = None


class ResponseGetFeedElementsWebApiDto(BaseModel):
    class Config:
        extra = Extra.forbid
        alias_generator = capitalize
        allow_population_by_field_name = True

    id: Optional[str] = None
    nativeCustomerId: Optional[str] = None
    feedId: Optional[str] = None
    feedNativeCustomerId: Optional[str] = None
    feedName: Optional[str] = None
    description: Optional[str] = None
    advertiserUrls: Optional[List[str]] = None
    status: Optional[str] = None
    erirValidationError: Optional[ErirValidationErrorWebApiDto] = None
    clickId: Optional[str] = None


class CreateFeedElementsBulkWebApiDto(BaseModel):
    class Config:
        extra = Extra.forbid
        alias_generator = capitalize
        allow_population_by_field_name = True

    feedElements: Optional[List[FeedElementWebApiDto]] = None
    feedId: Optional[str] = None
    feedNativeCustomerId: Optional[str] = None
    feedName: Optional[str] = None


class ResponseCreateFeedElementsBulkWebApiDto(BaseModel):
    class Config:
        extra = Extra.forbid
        alias_generator = capitalize
        allow_population_by_field_name = True

    id: Optional[str] = None


class GetFeedElementsBulkInfo(ResponseCreateFeedElementsBulkWebApiDto):
    pass


class FeedElementMediaWebApiDto(BaseModel):
    class Config:
        extra = Extra.forbid
        alias_generator = capitalize
        allow_population_by_field_name = True

    fileName: Optional[str] = None
    srcUrl: Optional[str] = None
    mediaDownloadError: Optional[str] = None


class BulkFeedElementWebApiDto(FeedElementWebApiDto):
    feedElementId: Optional[str] = None
    feedElementStatus: Optional[str] = None
    feedElementDto: Optional[CreateFeedElementsBulkWebApiDto] = None
    status: Optional[str] = None
    feedElementCreatingErrors: Optional[List[str]] = None
    feedElementMedias: Optional[List[FeedElementMediaWebApiDto]] = None


class ResponseGetFeedElementsBulkInfo(BaseModel):
    class Config:
        extra = Extra.forbid
        alias_generator = capitalize
        allow_population_by_field_name = True

    feedElements: Optional[List[BulkFeedElementWebApiDto]] = None
