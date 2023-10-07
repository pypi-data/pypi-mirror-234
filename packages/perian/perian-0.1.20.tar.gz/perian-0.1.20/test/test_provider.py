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

from perian.models.provider import Provider  # noqa: E501

class TestProvider(unittest.TestCase):
    """Provider unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> Provider:
        """Test Provider
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `Provider`
        """
        model = Provider()  # noqa: E501
        if include_optional:
            return Provider(
                name = 'Open Telekom Cloud',
                name_short = '',
                regions = [
                    perian.models.region.Region(
                        name = '', 
                        city = '', 
                        location = null, 
                        sustainable = True, 
                        status = null, 
                        zones = [
                            perian.models.zone.Zone(
                                name = '', 
                                status = null, )
                            ], )
                    ],
                location = 'de',
                status = 'Active',
                capabilities = [
                    'PricingAPI'
                    ]
            )
        else:
            return Provider(
        )
        """

    def testProvider(self):
        """Test Provider"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
