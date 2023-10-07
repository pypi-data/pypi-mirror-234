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


from typing import Optional, Union
from pydantic import BaseModel, StrictFloat, StrictInt
from perian.models.currency import Currency

class Price(BaseModel):
    """
    Price
    """
    per_hour: Optional[Union[StrictFloat, StrictInt]] = 0.0
    unit: Optional[Currency] = None
    __properties = ["per_hour", "unit"]

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
    def from_json(cls, json_str: str) -> Price:
        """Create an instance of Price from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> Price:
        """Create an instance of Price from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return Price.parse_obj(obj)

        _obj = Price.parse_obj({
            "per_hour": obj.get("per_hour") if obj.get("per_hour") is not None else 0.0,
            "unit": obj.get("unit")
        })
        return _obj


