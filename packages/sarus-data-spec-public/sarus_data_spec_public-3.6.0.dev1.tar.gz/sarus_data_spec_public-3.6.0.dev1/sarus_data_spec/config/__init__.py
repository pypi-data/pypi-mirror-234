import os

import yaml

properties_file = os.path.join(
    os.path.dirname(__file__), "privacy_properties.yaml"
)
with open(properties_file) as f:
    privacy_properties = yaml.load(f.read(), Loader=yaml.Loader)

WHITELISTED_TRANSFORMS = privacy_properties["WHITELISTED_TRANSFORMS"]

__all__ = [
    "WHITELISTED_TRANSFORMS",
]
