# Primitive for PodNet Network Global
# stdlib
import logging
from typing import Any, Dict, List, Tuple
# lib
# local
from cloudcix.primitives.utils import check_template_data, JINJA_ENV
from cloudcix.rcc import deploy_ssh, CouldNotConnectException

__all__ = [
    'build',
]


def build(
        domain_name_servers: List[str],
        host_ip: str,
        podnet_management_interface: Dict[str, Any],
        podnet_oob_interface: Dict[str, Any],
        podnet_private_interface: Dict[str, Any],
        podnet_public_interface: Dict[str, Any],
        debug: bool = False,
) -> Tuple[bool, str]:
    """
    This method :
        - creates /etc/netplan/00-global_network.yaml file

    domain_name_servers:
        description: List of nameservers for domain name resolution
        type: array
    host_ip:
        description: Remote server ip address on which these firewall rules are applied
        type: string
    podnet_management_interface:
        description: PodNet's Management Interface details
        type: dict object with following format:
             podnet_management_interface = {
                'name': 'eth0',                                                   #  interface name as on the PodNet
                'ips': [                                                          #  List of
                    {'network_address': '192.168.0.2', 'prefixlen': '24'},        #  ip object with network_address
                    {'network_address': '2a02:2078:9::142', 'prefixlen': '126'},  #  and prefixlen
                ],
                'routes': [
                    {'to': 'default', 'via': '192.168.0.1'},
                    {'to': '::/0', 'via': '2a02:2078::141'},
                ]
            }
    podnet_oob_interface:
        description: PodNet's OOB Interface details
        type: dict object same as podnet_management_interface
    podnet_private_interface:
        description: PodNet's Private Interface details
        type: dict object same as podnet_management_interface
    podnet_public_interface:
        description: |
            PodNet's Public Interface details
        type: dict object same as podnet_management_interface
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
    logger.debug('Compiling data for network_global.build')
    template_name = 'podnet/network/global_build.j2'

    # messages
    network_global_build_messages = {
        'msg_000': 'Successfully created 00-global_network.yaml on the host at /etc/netplan/.',
        'msg_010': 'Creating 00-global_network.yaml on the host at /etc/netplan/.',
        'msg_032': f'Failed to build Global network for PodNet {host_ip}',
    }

    template_data = {
        'domain_name_servers': domain_name_servers,
        'podnet_management_interface': podnet_management_interface,
        'podnet_oob_interface': podnet_oob_interface,
        'podnet_public_interface': podnet_public_interface,
        'podnet_private_interface': podnet_private_interface,
        'messages': network_global_build_messages,
    }

    # ensure all the required keys are collected and no key has None value for template_data
    template = JINJA_ENV.get_template(template_name)
    template_verified, template_error = check_template_data(template_data, template)
    if not template_verified:
        logger.debug(f'Failed to generate PodNet Global network build template. {template_error}')
        return False, template_error

    # Generate Netplan interface build config
    bash_script = template.render(**template_data)
    logger.debug(
        f'Generated PodNet Network Global build bash script:\n{bash_script}',
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
            f'PodNet Global Network on #{host_ip} build commands generated stdout.'
            f'\n{rcc_output}',
        )
        for message in network_global_build_messages.values():
            if message in rcc_output:
                out += message
                if message == network_global_build_messages['msg_000']:
                    success = True
    if rcc_error:
        logger.error(
            f'PodNet Global Network on #{host_ip} build commands generated stderr.'
            f'\n{rcc_error}',
        )

    if debug:
        out += rcc_output
        out += rcc_error

    return success, out
