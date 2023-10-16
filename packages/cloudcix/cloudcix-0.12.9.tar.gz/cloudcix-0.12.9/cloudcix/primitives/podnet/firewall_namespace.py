# Primitive for PodNet Firewall Namespace
# stdlib
import logging
from collections import deque
from typing import Any, Deque, Dict, List, Tuple
# lib
from netaddr import IPNetwork
# local
from cloudcix.primitives.utils import check_template_data, JINJA_ENV
from cloudcix.rcc import deploy_ssh, CouldNotConnectException

__all__ = [
    'build',
]


def build(
        firewall_rules: List[Dict[str, Any]],
        host_ip: str,
        nats: Deque[Dict[str, str]],
        namespace: str,
        public_bridge_name: str,
        debug: bool = False,
) -> Tuple[bool, str]:
    """
    This method :
        - Creates a /tmp/<namespace>.conf file with new config
        - Validates the nft file `sudo nft -c -f /tmp/<namespace>.conf`
        - If any errors then exits with errors
        - Config is applied `sudo ip netns exec <namespace>.conf nft --file /tmp/<namespace>.conf`
        - Temp file is removed from /tmp/

    firewall_rules:
        description: |
            containing firewall rules in the following format
            rule = {
                'description': '',  # string
                'interface': {'from': '', 'to': ''},  # dictionary
                'version': '6',  # string
                'source': [],  # list of strings
                'destination': [],  # list of strings
                'protocol': 'tcp',  # string
                'port': ['22'],  # list of strings
                'type': 'accept',  # string
            }
        type: array
    host_ip:
        description: Remote server ip address on which these firewall rules are applied
        type: string
    nats:
        description: List of NATs object with Private IP and its Public IP
        type: array
    namespace:
        description: Namespace's name to which the firewall rules to be applied
        type: string
    public_bridge_name:
        description: Name of the Public Bridge name to identify and use it in firewall config
        type: string
    debug:
        description: If set to True, detailed error information is shared
        type: boolean
    return:
        description: |
            A tuple with a boolean flag stating the build was successful or not and
            the output or error message.
        type: tuple
    """
    out = ''

    logger = logging.getLogger(__name__)
    logger.debug('Compiling data for firewall_namespace.build')
    template_name = 'podnet/firewall/global_namespace.j2'

    # template messages
    fail_start = f'Failed to apply Firewall config for namespace {namespace}.'
    firewall_namespace_build_messages = {
        'msg_000': f'Successfully applied Firewall config for namespace {namespace}',
        'msg_010': f'Configuration file /tmp/{namespace}.nft is valid. Applying the Firewall',
        'msg_032': f'{fail_start} Configuration file /tmp/{namespace}.nft syntax is invalid. Exiting.',
        'msg_033': f'{fail_start} Configuration file /tmp/{namespace}.nft Not found.',
    }

    # Firewall rules
    inbound_firewall_rules: Deque[Dict[str, Any]] = deque()
    outbound_firewall_rules: Deque[Dict[str, Any]] = deque()
    for rule in sorted(firewall_rules, key=lambda fw: fw['order']):
        # logging
        rule['log'] = True if rule['pci_logging'] else rule['debug_logging']
        # Determine if it is IPv4 or IPv6
        rule['address_family'] = IPNetwork(rule['destination']).version

        # Check port and protocol to allow any port for a specific protocol
        if rule['port'] is None:
            rule['port'] = '0-65535'

        if IPNetwork(rule['destination']).is_private():
            inbound_firewall_rules.append(rule)
        else:
            outbound_firewall_rules.append(rule)

    template_data = {
        'inbound_firewall_rules': inbound_firewall_rules,
        'namespace_name': namespace,
        'nats': nats,
        'outbound_firewall_rules': outbound_firewall_rules,
        'public_bridge_name': public_bridge_name,
        'messages': firewall_namespace_build_messages,
    }

    # ensure all the required keys are collected and no key has None value for template_data
    template = JINJA_ENV.get_template(template_name)
    template_verified, template_error = check_template_data(template_data, template)
    if not template_verified:
        logger.debug(f'Failed to generate PodNet Namespace Firewall build template. {template_error}')
        return False, template_error

    # Generate Firewall build config
    bash_script = template.render(**template_data)
    logger.debug(
        f'Generated Firewall build bash script for Namespace #{namespace}\n{bash_script}',
    )

    if debug:
        out += bash_script

    # Deploy the bash script to the Host
    try:
        rcc_output, rcc_error = deploy_ssh(
            host_ip=host_ip,
            payload=bash_script,
        )
    except CouldNotConnectException as e:
        return False, str(e)

    success = False

    if rcc_output:
        logger.debug(
            f'PodNet Firewall rules for Namespace #{namespace} on #{host_ip} build commands generated stdout.'
            f'\n{rcc_output}',
        )
        for message in firewall_namespace_build_messages.values():
            if message in rcc_output:
                out += message
                if message == firewall_namespace_build_messages['msg_000']:
                    success = True

    if rcc_error:
        logger.error(
            f'Firewall rules for Namespace #{namespace} on #{host_ip} build commands generated stderr.'
            f'\n{rcc_error}',
        )

    if debug:
        out += rcc_output
        out += rcc_error

    return success, out
