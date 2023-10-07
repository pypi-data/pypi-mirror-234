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
from pydantic import BaseModel, StrictInt
from perian.models.bandwidth import Bandwidth

class Cpu(BaseModel):
    """
    Cpu
    """
    threads: Optional[StrictInt] = 0
    cores: Optional[StrictInt] = 0
    speed: Optional[Bandwidth] = None
    __properties = ["threads", "cores", "speed"]

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
    def from_json(cls, json_str: str) -> Cpu:
        """Create an instance of Cpu from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of speed
        if self.speed:
            _dict['speed'] = self.speed.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> Cpu:
        """Create an instance of Cpu from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return Cpu.parse_obj(obj)

        _obj = Cpu.parse_obj({
            "threads": obj.get("threads") if obj.get("threads") is not None else 0,
            "cores": obj.get("cores") if obj.get("cores") is not None else 0,
            "speed": Bandwidth.from_dict(obj.get("speed")) if obj.get("speed") is not None else None
        })
        return _obj


