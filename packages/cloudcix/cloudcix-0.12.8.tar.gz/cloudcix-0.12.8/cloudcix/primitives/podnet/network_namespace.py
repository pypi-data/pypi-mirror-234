# network namespace primitive
# stdlib
import logging
from typing import Any, Dict, Tuple
# lib
from cloudcix.primitives.utils import check_template_data, JINJA_ENV
from cloudcix.rcc import deploy_ssh, CouldNotConnectException

__all__ = [
    'build',
    'scrub',
]


def build(
        host_ip: str,
        namespace: Dict[str, Any],
        podnet_private_interface: Dict[str, Any],
        public_subnet_bridge: Dict[str, str],
        debug: bool = False,
) -> Tuple[bool, str]:
    """
    Building namespace for the given data.
    host_ip:
        description: Remote server ip address on which these firewall rules are applied
        type: string
    namespace:
        description: Namespace details of the Project
        type: dict,  with following format and fields
            namespace = {
                'name': 'P123',                           #  :type str, name of the Namespace
                'networks': [{                            #  :type list, List of all the Namespace networks
                     'name': 'prj1001'                   #  :type str, name of the private bridge for this network
                     'vlan': '1001',                      #  :type str, vlan number of the network in string
                     'address_range': '192.168.0.1/24',   #  :type str, subnet_ip/subnet_mask
                 },
                 ],
            }
    podnet_private_interface:
        description: PodNet's Private Interface name
        type: str, eg 'eth1'
    public_subnet_bridge:
        description: The Floating subnet bridge details that this Namespace is connected to
        type: dict, of the format:
            public_subnet = {
                'name': 'B123',                           #  :type str, Namespace's Floating subnet bridge name
                'address_range': '185.49.65.127/24',      #  :type str, network_ip/mask
                'gateway': '185.49.65.1',                 #  :type str, gateway of Floating subnet
            }
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
    logger.debug('Compiling data for network_namespace.build')
    template_name = 'podnet/network/namespace_build.j2'
    name = namespace['name']

    template_data = {
        'namespace_name': name,  # Namespace name
        'namespace_networks': namespace['networks'],  # Namespace networks (RFC1918 and IPv6 /64s)
        'podnet_private_interface': podnet_private_interface,  # The private interface of the firewall
        'public_bridge_name': public_subnet_bridge['name'],  # Public bridge that the namespace is connected to
        'public_bridge_gateway': public_subnet_bridge['gateway'],  # Public bridge gateway
        'public_bridge_mask': public_subnet_bridge['address_range'].split('/')[1],  # Public bridge mask(prefixlen)
        'public_bridge_network': public_subnet_bridge['address_range'].split('/')[0],  # Public bridge network IP
    }

    # ensure all the required keys are collected and no key has None value for template_data
    template = JINJA_ENV.get_template(template_name)
    template_verified, template_error = check_template_data(template_data, template)
    if not template_verified:
        logger.debug(
            f'Failed to generate PodNet Namespace network build template for namespace#{name}.\n{template_error}',
        )
        return False, template_error

    # Prepare namespace build config
    bash_script = template.render(**template_data)
    logger.debug(
        f'Generated build bash script for Namespace #{name}\n{bash_script}',
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
            f'Namespace Network for namespace #{name} on #{host_ip} build commands generated stdout.'
            f'\n{rcc_output}',
        )
        success = True
    if rcc_error:
        logger.error(
            f'Namespace Network for namespace #{name} on #{host_ip} build commands generated stderr.'
            f'\n{rcc_error}',
        )

    if debug:
        out += rcc_output
        out += rcc_error

    return success, out


def scrub(
        host_ip: str,
        namespace: Dict[str, Any],
        podnet_private_interface: Dict[str, Any],
        debug: bool = False,
) -> Tuple[bool, str]:
    """
    Deleting namespace for the given data.

    host_ip:
        description: Remote server ip address on which these firewall rules are applied
        type: string
    namespace:
        description: Namespace details of the Project
        type: dict,  with following format and fields
            namespace = {
                'name': 'P123',                           #  :type str, name of the Namespace
                'networks': [{                            #  :type list, List of all the Namespace networks
                     'name': 'prj1001'                   #  :type str, name of the private bridge for this network
                     'vlan': '1001',                      #  :type str, vlan number of the network in string
                     'address_range': '192.168.0.1/24',   #  :type str, subnet_ip/subnet_mask
                 },
                 ],
            }
    podnet_private_interface:
        description: PodNet's Private Interface name
        type: str, eg 'eth1'
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
    logger.debug('Compiling data for network_namespace.scrub')
    template_name = 'podnet/network/namespace_scrub.j2'
    name = namespace['name']

    template_data = {
        'namespace_name': name,
        'namespace_networks': namespace['networks'],
        'podnet_private_interface': podnet_private_interface,
    }

    # ensure all the required keys are collected and no key has None value for template_data
    template_verified, template_error = check_template_data(template_data, template_name)
    if not template_verified:
        logger.debug(
            f'Failed to generate PodNet Namespace network Scrub template for namespace#{name}.\n{template_error}',
        )
        return False, template_error

    # Prepare namespace delete config
    bash_script = JINJA_ENV.get_template(template_name).render(**template_data)
    logger.debug(
        f'Generated scrub bash script for Namespace #{name}\n{bash_script}',
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
            f'Namespace Network for namespace #{name} on #{host_ip} scrub commands generated stdout.'
            f'\n{rcc_output}',
        )
        success = True
    if rcc_error:
        logger.error(
            f'Namespace Network for namespace #{name} on #{host_ip} scrub commands generated stderr.'
            f'\n{rcc_error}',
        )

    if debug:
        out += rcc_output
        out += rcc_error

    return success, out
