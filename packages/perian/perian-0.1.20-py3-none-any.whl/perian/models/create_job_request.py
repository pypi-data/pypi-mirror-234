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
from perian.models.docker_registry_credentials import DockerRegistryCredentials
from perian.models.docker_run_parameters import DockerRunParameters
from perian.models.os_storage_config import OSStorageConfig

class CreateJobRequest(BaseModel):
    """
    CreateJobRequest
    """
    flavor_id: Optional[StrictStr] = None
    os_storage_config: Optional[OSStorageConfig] = None
    docker_run_parameters: Optional[DockerRunParameters] = None
    docker_registry_credentials: Optional[DockerRegistryCredentials] = None
    __properties = ["flavor_id", "os_storage_config", "docker_run_parameters", "docker_registry_credentials"]

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
    def from_json(cls, json_str: str) -> CreateJobRequest:
        """Create an instance of CreateJobRequest from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of os_storage_config
        if self.os_storage_config:
            _dict['os_storage_config'] = self.os_storage_config.to_dict()
        # override the default output from pydantic by calling `to_dict()` of docker_run_parameters
        if self.docker_run_parameters:
            _dict['docker_run_parameters'] = self.docker_run_parameters.to_dict()
        # override the default output from pydantic by calling `to_dict()` of docker_registry_credentials
        if self.docker_registry_credentials:
            _dict['docker_registry_credentials'] = self.docker_registry_credentials.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> CreateJobRequest:
        """Create an instance of CreateJobRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return CreateJobRequest.parse_obj(obj)

        _obj = CreateJobRequest.parse_obj({
            "flavor_id": obj.get("flavor_id"),
            "os_storage_config": OSStorageConfig.from_dict(obj.get("os_storage_config")) if obj.get("os_storage_config") is not None else None,
            "docker_run_parameters": DockerRunParameters.from_dict(obj.get("docker_run_parameters")) if obj.get("docker_run_parameters") is not None else None,
            "docker_registry_credentials": DockerRegistryCredentials.from_dict(obj.get("docker_registry_credentials")) if obj.get("docker_registry_credentials") is not None else None
        })
        return _obj


