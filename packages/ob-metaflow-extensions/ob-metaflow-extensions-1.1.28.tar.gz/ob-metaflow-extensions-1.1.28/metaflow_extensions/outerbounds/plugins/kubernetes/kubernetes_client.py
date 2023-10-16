import os
import sys
import time

from metaflow.exception import MetaflowException


CLIENT_REFRESH_INTERVAL_SECONDS = 300


class KubernetesClientException(MetaflowException):
    headline = "Kubernetes client error"


class KubernetesClient(object):
    def __init__(self):
        try:
            # Kubernetes is a soft dependency.
            from kubernetes import client, config
        except (NameError, ImportError):
            raise KubernetesClientException(
                "Could not import module 'kubernetes'.\n\nInstall Kubernetes "
                "Python package (https://pypi.org/project/kubernetes/) first.\n"
                "You can install the module by executing - "
                "%s -m pip install kubernetes\n"
                "or equivalent through your favorite Python package manager."
                % sys.executable
            )
        self._refresh_client()

    def _refresh_client(self):
        from metaflow_extensions.outerbounds.plugins.auth_server import get_token
        from kubernetes import client

        config = client.Configuration()
        token_info = get_token("/generate/k8s")
        config.host = token_info["endpoint"]
        config.api_key["authorization"] = "Bearer " + token_info["token"]
        config.verify_ssl = False  # TODO: FIX THIS
        client.Configuration.set_default(config)
        self._client = client
        self._client_refresh_timestamp = time.time()

    def get(self):
        if (
            time.time() - self._client_refresh_timestamp
            > CLIENT_REFRESH_INTERVAL_SECONDS
        ):
            self._refresh_client()

        return self._client

    def job(self, **kwargs):
        from metaflow.plugins.kubernetes.kubernetes_job import KubernetesJob

        return KubernetesJob(self, **kwargs)
