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

from perian.models.description_query import DescriptionQuery  # noqa: E501

class TestDescriptionQuery(unittest.TestCase):
    """DescriptionQuery unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> DescriptionQuery:
        """Test DescriptionQuery
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `DescriptionQuery`
        """
        model = DescriptionQuery()  # noqa: E501
        if include_optional:
            return DescriptionQuery(
                operator = 'EQUALS',
                description = ''
            )
        else:
            return DescriptionQuery(
        )
        """

    def testDescriptionQuery(self):
        """Test DescriptionQuery"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
