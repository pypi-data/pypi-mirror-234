"""
Defines a Skyramp client, which can be used to interact with a cluster.
"""

import ctypes
import yaml

from skyramp.utils import _library, _call_function
from skyramp.scenario import _Scenario


class _Client:
    """
    Skyramp client object which can be used to interact with a cluster.
    """

    def __init__(
        self,
        kubeconfig_path: str = "",
        cluster_name: str = "",
        context: str = "",
    ) -> None:
        """
        Initializes a Skyramp Client.

        kubeconfig_path: The filesystem path of a kubeconfig
        cluster_name: The name of the cluster.
        context: The Kubernetes context within a kubeconfig
        """
        self.kubeconfig_path = kubeconfig_path
        self.cluster_name = cluster_name
        self.context = context

        self._namespace_set = set()

    def apply_local(self) -> None:
        """
        Creates a local cluster.
        """
        apply_local_function = _library.applyLocalWrapper
        argtypes = []
        restype = ctypes.c_char_p

        _call_function(apply_local_function, argtypes, restype, [])

        self.kubeconfig_path = self._get_kubeconfig_path()
        if not self.kubeconfig_path:
            raise Exception("no kubeconfig found")

    def remove_local(self) -> None:
        """
        Removes a local cluster.
        """
        func = _library.removeLocalWrapper
        argtypes = []
        restype = ctypes.c_char_p

        _call_function(func, argtypes, restype, [])

    def add_kubeconfig(
        self,
        context: str,
        cluster_name: str,
        kubeconfig_path: str,
    ) -> None:
        """
        Adds a preexisting Kubeconfig file to Skyramp.

        context: The kubeconfig context to use
        cluster_name: Name of the cluster
        kubeconfig_path: filepath of the kubeconfig
        """
        func = _library.addKubeconfigWrapper
        argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
        restype = ctypes.c_char_p

        _call_function(
            func,
            argtypes,
            restype,
            [
                context.encode(),
                cluster_name.encode(),
                kubeconfig_path.encode(),
            ],
        )

        self.kubeconfig_path = kubeconfig_path

    def remove_cluster(self, cluster_name: str) -> None:
        """
        Removes a cluster, corresponding to the name, from Skyramp
        """
        func = _library.removeClusterFromConfigWrapper
        argtypes = [ctypes.c_char_p]
        restype = ctypes.c_char_p

        _call_function(func, argtypes, restype, [cluster_name.encode()])

    def deploy_skyramp_worker(
        self, namespace: str, worker_image: str, local_image: bool
    ) -> None:
        """
        Installs a Skyramp worker onto a cluster if one is registered with Skyramp
        """
        if not self.kubeconfig_path:
            raise Exception("no cluster to deploy worker to")

        func = _library.deploySkyrampWorkerWrapper
        argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_bool]
        restype = ctypes.c_char_p

        _call_function(
            func,
            argtypes,
            restype,
            [namespace.encode(), worker_image.encode(), local_image],
        )

        self._namespace_set.add(namespace)

    def delete_skyramp_worker(self, namespace: str) -> None:
        """
        Removes the Skyramp worker, if a Skyramp worker is installed on a registered Skyramp cluster
        """
        if not self.kubeconfig_path:
            raise Exception("no cluster to delete worker from")

        if namespace not in self._namespace_set:
            raise Exception(f"no worker to delete from {namespace} namespace")

        func = _library.deleteSkyrampWorkerWrapper
        argtypes = [ctypes.c_char_p]
        restype = ctypes.c_char_p

        _call_function(func, argtypes, restype, [namespace.encode()])

        self._namespace_set.remove(namespace)

    def mocker_apply(self, namespace: str, address: str, endpoint) -> None:
        """
        Applies a configuration to mocker.
        namespace: The namespace where Mocker resides
        address: The address of Mocker
        endpoint: The Skyramp enpdoint object
        """
        yaml_string = yaml.dump(endpoint.mock_description)

        func = _library.applyMockDescriptionWrapper
        argtypes = [
            ctypes.c_char_p,
            ctypes.c_char_p,
            ctypes.c_char_p,
        ]
        restype = ctypes.c_char_p  # pylint: disable=duplicate-code

        _call_function(
            func,
            argtypes,
            restype,
            [
                namespace.encode(),
                address.encode(),
                yaml_string.encode(),
            ],
        )

    def tester_start(self, namespace: str, address: str, scenario: _Scenario) -> str:
        """
        Runs testers. If namespace is provided, connects with the worker instance running
        on the specified namespace in the registered Kubernetes cluster. If address is provided,
        connects to the worker directly using the network address.
        namespace: The namespace where mocker resides
        address: The address to reach mocker
        scenario: Scenario object for the test to run
        """
        test_description = scenario.get_test_description()
        test_yaml = yaml.dump(test_description)

        func = _library.runTesterStartWrapper
        argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_bool]
        restype = ctypes.c_char_p

        _call_function(
            func,
            argtypes,
            restype,
            [
                namespace.encode(),
                address.encode(),
                test_yaml.encode(),
                True,
            ],
        )

    def _get_kubeconfig_path(self) -> str:
        func = _library.getKubeConfigPath
        argtypes = []
        restype = ctypes.c_char_p

        return _call_function(func, argtypes, restype, [], True)
