# coding: utf-8

"""
    FastAPI

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)

    The version of the OpenAPI document: 0.1.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json


from typing import Optional
from pydantic import BaseModel, StrictStr
from perian.models.availability import Availability
from perian.models.cpu_data import CpuData
from perian.models.flavor_type import FlavorType
from perian.models.gpu_data import GpuData
from perian.models.memory import Memory
from perian.models.network import Network
from perian.models.price_data import PriceData
from perian.models.provider import Provider
from perian.models.region import Region
from perian.models.storage_data import StorageData

class Flavor(BaseModel):
    """
    Flavor
    """
    pid: Optional[StrictStr] = None
    provider: Optional[Provider] = None
    region: Optional[Region] = None
    reference_id: Optional[StrictStr] = ''
    description: Optional[StrictStr] = ''
    cpu: Optional[CpuData] = None
    gpu: Optional[GpuData] = None
    ram: Optional[Memory] = None
    storage: Optional[StorageData] = None
    network: Optional[Network] = None
    price: Optional[PriceData] = None
    availability: Optional[Availability] = None
    type: Optional[FlavorType] = None
    __properties = ["pid", "provider", "region", "reference_id", "description", "cpu", "gpu", "ram", "storage", "network", "price", "availability", "type"]

    class Config:
        """Pydantic configuration"""
        allow_population_by_field_name = True
        validate_assignment = True

    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.dict(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Flavor:
        """Create an instance of Flavor from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of provider
        if self.provider:
            _dict['provider'] = self.provider.to_dict()
        # override the default output from pydantic by calling `to_dict()` of region
        if self.region:
            _dict['region'] = self.region.to_dict()
        # override the default output from pydantic by calling `to_dict()` of cpu
        if self.cpu:
            _dict['cpu'] = self.cpu.to_dict()
        # override the default output from pydantic by calling `to_dict()` of gpu
        if self.gpu:
            _dict['gpu'] = self.gpu.to_dict()
        # override the default output from pydantic by calling `to_dict()` of ram
        if self.ram:
            _dict['ram'] = self.ram.to_dict()
        # override the default output from pydantic by calling `to_dict()` of storage
        if self.storage:
            _dict['storage'] = self.storage.to_dict()
        # override the default output from pydantic by calling `to_dict()` of network
        if self.network:
            _dict['network'] = self.network.to_dict()
        # override the default output from pydantic by calling `to_dict()` of price
        if self.price:
            _dict['price'] = self.price.to_dict()
        # override the default output from pydantic by calling `to_dict()` of availability
        if self.availability:
            _dict['availability'] = self.availability.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> Flavor:
        """Create an instance of Flavor from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return Flavor.parse_obj(obj)

        _obj = Flavor.parse_obj({
            "pid": obj.get("pid"),
            "provider": Provider.from_dict(obj.get("provider")) if obj.get("provider") is not None else None,
            "region": Region.from_dict(obj.get("region")) if obj.get("region") is not None else None,
            "reference_id": obj.get("reference_id") if obj.get("reference_id") is not None else '',
            "description": obj.get("description") if obj.get("description") is not None else '',
            "cpu": CpuData.from_dict(obj.get("cpu")) if obj.get("cpu") is not None else None,
            "gpu": GpuData.from_dict(obj.get("gpu")) if obj.get("gpu") is not None else None,
            "ram": Memory.from_dict(obj.get("ram")) if obj.get("ram") is not None else None,
            "storage": StorageData.from_dict(obj.get("storage")) if obj.get("storage") is not None else None,
            "network": Network.from_dict(obj.get("network")) if obj.get("network") is not None else None,
            "price": PriceData.from_dict(obj.get("price")) if obj.get("price") is not None else None,
            "availability": Availability.from_dict(obj.get("availability")) if obj.get("availability") is not None else None,
            "type": obj.get("type")
        })
        return _obj


