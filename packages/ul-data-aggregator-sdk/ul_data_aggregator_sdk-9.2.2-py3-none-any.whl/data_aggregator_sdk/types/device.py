from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID

from ul_api_utils.api_resource.api_response_payload_alias import ApiBaseUserModelPayloadResponse
from ul_api_utils.api_resource.api_response import JsonApiResponsePayload

from data_aggregator_sdk.constants.enums import DeviceModificationTypeEnum, NetworkSysTypeEnum, NetworkTypeEnum, \
    ProtocolEnum, ResourceKind


class ApiDataGatewayResponse(ApiBaseUserModelPayloadResponse):
    name: str


class ApiDataGatewaysNetworkResponse(ApiBaseUserModelPayloadResponse):
    name: str
    type_network: NetworkTypeEnum
    data_gateway_id: UUID
    data_gateway: ApiDataGatewayResponse
    sys_type: NetworkSysTypeEnum
    specifier: Optional[str]
    params: Optional[Dict[str, Any]]


class ApiProtocolResponse(JsonApiResponsePayload):
    id: UUID
    date_created: datetime
    date_modified: datetime
    name: str
    type: ProtocolEnum


class ApiDataGatewayNetworkDevicePayloadResponse(JsonApiResponsePayload):
    id: UUID
    date_created: datetime
    date_modified: datetime
    uplink_protocol_id: UUID
    downlink_protocol_id: UUID
    data_gateway_network_id: UUID
    mac: int
    key_id: Optional[UUID]
    device_id: UUID
    uplink_encryption_key: Optional[str]
    downlink_encryption_key: Optional[str]
    encryption_key: Optional[str]
    protocol: ApiProtocolResponse
    network: Optional[ApiDataGatewaysNetworkResponse]


class ApiDeviceMeteringTypeResponse(JsonApiResponsePayload):
    id: UUID
    date_created: datetime
    date_modified: datetime

    sys_name: str
    name_ru: str
    name_en: str


class ApiDeviceModificationTypeResponse(JsonApiResponsePayload):
    id: UUID
    date_created: datetime
    date_modified: datetime

    sys_name: str
    name_ru: str
    name_en: str
    type: DeviceModificationTypeEnum
    metering_type_id: UUID
    device_metering_type: ApiDeviceMeteringTypeResponse


class ApiDeviceModificationResponse(JsonApiResponsePayload):
    id: UUID
    date_created: datetime
    date_modified: datetime
    name: Optional[str]
    device_modification_type_id: Optional[UUID]
    device_modification_type: ApiDeviceModificationTypeResponse


class ApiDeviceMeterPayloadResponse(ApiBaseUserModelPayloadResponse):
    device_channel_id: UUID
    value_multiplier: Optional[float]
    unit_multiplier: Optional[float]
    kind: ResourceKind


class ApiDeviceChannelPayloadResponse(ApiBaseUserModelPayloadResponse):
    inactivity_limit: Optional[int]
    serial_number: int
    device_meter: List[ApiDeviceMeterPayloadResponse]


class ApiDeviceManufacturerResponse(JsonApiResponsePayload):
    id: UUID
    date_created: datetime
    date_modified: datetime

    name: str


class ApiImportDeviceResponse(ApiBaseUserModelPayloadResponse):
    manufacturer_serial_number: str
    firmware_version: Optional[str]
    hardware_version: Optional[str]
    date_produced: Optional[datetime]
    device_manufacturer: ApiDeviceManufacturerResponse
    device_modification: ApiDeviceModificationResponse
    device_channel: List[ApiDeviceChannelPayloadResponse]
    data_gateway_network_device: Optional[ApiDataGatewayNetworkDevicePayloadResponse]
