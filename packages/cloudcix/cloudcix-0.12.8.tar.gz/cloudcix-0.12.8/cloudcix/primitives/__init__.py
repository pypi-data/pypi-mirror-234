"""
Wrapper around the python requests module for ease of interaction with all CloudCIX services

Basic usage: ``cloudcix.primitives.<hardware>.[_hardware].<method>``

More detailed usage information will be available under each of the above terms

To see even more details about the API you can visit our `HTTP API Reference <https://docs.community.cloudcix.com/>`_
"""
from .podnet import (
    firewall_global,
    firewall_namespace,
    network_global,
    network_namespace,
    subnet_bridge,
    vpns2s,
)

__all__ = [
    'firewall_global',
    'firewall_namespace',
    'network_global',
    'network_namespace',
    'subnet_bridge',
    'vpns2s',
]
