# These two fields will show up within `metaflow_version` task metadata.
# Setting to major version of ob-metaflow-extensions only, so we don't keep trying
# (and failing) to keep this in sync with setup.py
# E.g. "2.7.22.1+ob(v1)"
__version__ = "v1"
__mf_extensions__ = "ob"

# To support "from metaflow import get_aws_client"
from metaflow.plugins.aws.aws_client import get_aws_client
