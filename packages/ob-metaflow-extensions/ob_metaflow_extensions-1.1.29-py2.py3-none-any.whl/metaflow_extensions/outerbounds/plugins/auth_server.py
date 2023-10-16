import os
import json
import requests
from urllib.parse import urlparse


def read_mf_config():
    # Read configuration from $METAFLOW_HOME/config_<profile>.json.
    home = os.environ.get("METAFLOW_HOME", "~/.metaflowconfig")
    profile = os.environ.get("METAFLOW_PROFILE")
    path_to_config = os.path.join(home, "config.json")
    if profile:
        path_to_config = os.path.join(home, "config_%s.json" % profile)
    path_to_config = os.path.expanduser(path_to_config)
    config = {}
    if os.path.exists(path_to_config):
        with open(path_to_config, encoding="utf-8") as f:
            return json.load(f)
    elif profile:
        from metaflow.exception import MetaflowException

        raise MetaflowException(
            "Unable to locate METAFLOW_PROFILE '%s' in '%s')" % (profile, home)
        )
    return config


def get_token(url_path):
    from metaflow.metaflow_config import (
        SERVICE_HEADERS,
        from_conf,
        SERVICE_URL,
    )
    from metaflow.exception import MetaflowException

    # Infer auth host from metadata service URL, unless it has been
    # specified explicitly. Take the MDS host and replace first part of
    # the domain name with `auth.`. All our deployments follow this scheme
    # anyways.
    #
    auth_host = "auth." + urlparse(SERVICE_URL).hostname.split(".", 1)[1]

    authServer = read_mf_config().get("OBP_AUTH_SERVER", auth_host)
    assert url_path.startswith("/")
    url = "https://" + authServer + url_path
    headers = SERVICE_HEADERS
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        token_info = r.json()
        return token_info

    except requests.exceptions.HTTPError as e:
        raise MetaflowException(repr(e))
