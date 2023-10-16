"""
Contains helpers for interacting with Skyramp testing scenarios.
"""

import ctypes
import json
import os
import yaml

from skyramp.utils import _library, _call_function, SKYRAMP_YAML_VERSION
from skyramp.endpoint import _Endpoint


class _Scenario:
    """
    Represents a testing scenario.
    """

    def __init__(self, name: str) -> None:
        self.name = name
        self.steps = []
        self.services = []
        self.endpoints = []
        self.requests = []

    def add_request(
        self,
        endpoint: _Endpoint,
        method_name: str,
        request_object = None,
        dynamic: bool = False,
    ) -> str:
        """
        Adds a request to this scenario.
        endpoint: The endpoint object associated with the request
        method_name: The name of the method that this request will be hitting
        request_object: Map containing request information
        dynamic: Whether or not the request_object is a dynamic script

        Returns the request name
        """
        self._build_metadata_for_endpoint(endpoint)

        for request in self.requests:
            if request["methodName"] != method_name:
                continue

            if dynamic:
                request["javascriptPath"] = request_object
                request.pop("blob", None)
            elif request_object is not None:
                request["blob"] = request_object["requestValue"]["blob"]

            self.steps += [{"requestName": request["name"]}]
            return request["name"]

    def add_request_from_file(
        self, endpoint: _Endpoint, method_name: str, request_file: str
    ) -> str:
        """
        Adds the request in the specified file to the corresponding endpoint and method.
        """
        _, file_ext = os.path.splitext(request_file)

        try:
            with open(request_file) as file:
                file_contents = file.read()
        except:
            raise Exception(f"failed to open file: {request_file}")
        # pylint: disable=duplicate-code
        dynamic = False

        if file_ext == ".json":
            data = json.loads(file_contents)
        elif file_ext in [".yaml", ".yml"]:
            data = yaml.safe_load(file_contents)
        elif file_ext == ".js":
            dynamic = True
            data = request_file
        else:
            raise Exception(
                f"unsupported file format: {file_ext}. Only JSON, YAML, and JS are supported"
            )

        return self.add_request(endpoint, method_name, data, dynamic)

    def add_assert_equal(self, value_name: str, expected_value: str):
        """
        Adds an assert equal given the value expression and expected value
        """
        assertion = f'requests.{value_name} == "{expected_value}"'
        self.steps.append({"asserts": assertion})

    def _build_metadata_for_endpoint(self, endpoint: _Endpoint):
        if endpoint.endpoint in self.endpoints:
            return

        self.services += endpoint.services

        self.endpoints.append(endpoint.endpoint)

        mock_description_yaml = yaml.dump(endpoint.mock_description)

        func = _library.buildRequestsWrapper
        argtypes = [ctypes.c_char_p]
        restype = ctypes.c_char_p

        requests = _call_function(
            func, argtypes, restype, [mock_description_yaml.encode()], return_output=True
        )

        parsed_requests = json.loads(requests)
        self.requests.append(parsed_requests[0])

    def get_test_description(self):
        """
        Helper for returning the test description for the scenario
        """
        return {
            "version": SKYRAMP_YAML_VERSION,
            "test": {
                "testPattern": [{"startAt": 1, "scenarioName": self.name}],
            },
            "services": self.services,
            "endpoints": self.endpoints,
            "scenarios": [{"name": self.name, "steps": self.steps}],
            "requests": self.requests,
        }
