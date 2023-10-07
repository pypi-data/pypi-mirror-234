# coding: utf-8

"""
    FastAPI

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)

    The version of the OpenAPI document: 0.1.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest
import datetime

from perian.models.memory import Memory  # noqa: E501

class TestMemory(unittest.TestCase):
    """Memory unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> Memory:
        """Test Memory
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `Memory`
        """
        model = Memory()  # noqa: E501
        if include_optional:
            return Memory(
                size = 1.337,
                unit = 'Gb',
                bandwidth = perian.models.bandwidth.Bandwidth(
                    speed = 1.337, 
                    maximum = 1.337, 
                    minimum = 1.337, 
                    unit = null, 
                    sla = null, 
                    limit = null, ),
                interface = 'Hbm2'
            )
        else:
            return Memory(
        )
        """

    def testMemory(self):
        """Test Memory"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
