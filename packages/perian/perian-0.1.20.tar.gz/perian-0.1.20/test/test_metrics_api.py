# coding: utf-8

"""
    FastAPI

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)

    The version of the OpenAPI document: 0.1.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from perian.api.metrics_api import MetricsApi  # noqa: E501


class TestMetricsApi(unittest.TestCase):
    """MetricsApi unit test stubs"""

    def setUp(self) -> None:
        self.api = MetricsApi()  # noqa: E501

    def tearDown(self) -> None:
        pass

    def test_get_liveness_metrics_liveness_get(self) -> None:
        """Test case for get_liveness_metrics_liveness_get

        Get Liveness  # noqa: E501
        """
        pass

    def test_get_readiness_metrics_readiness_get(self) -> None:
        """Test case for get_readiness_metrics_readiness_get

        Get Readiness  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
