# Primitive for PodNet Subnet Bridge
# stdlib
import logging
from typing import Any, Dict, Tuple
# local
from cloudcix.primitives.utils import check_template_data, JINJA_ENV
from cloudcix.rcc import deploy_ssh, CouldNotConnectException

__all__ = [
    'build',
]


def build(
        host_ip: str,
        subnet_bridge_address_range: str,
        subnet_bridge_interface: Dict[str, Any],
        subnet_bridge_name: str,
        debug: bool = False,
) -> Tuple[bool, str]:
    """
    Checks if the /etc/netplan/B<subnet_id>.yaml file exists.
    Creates /etc/netplan/B<subnet_id>.yaml file if not exists.
    Apply's the netplan changes

    host_ip:
        description: Remote server ip address on which these firewall rules are applied
        type: string
    subnet_bridge_address_range:
        description: Subnet Bridge's address range.
        type: str, eg '91.103.0.1/24'
    subnet_bridge_interface:
        description: Subnet Bridge Interface name that this bridge is connected to. Usually PodNet's Public interface
        type: string, eg 'eth0'
    subnet_bridge_name:
        description: Name of the Subnet Bridge to identify and used across Namespaces
        type: string, eg 'B123'
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
    logger.debug('Compiling data for subnet_bridge.build')
    template_name = 'podnet/subnet_bridge/build.j2'

    # messages
    subnet_bridge_build_messages = {
        'msg_000': f'Successfully created /etc/netplan/{subnet_bridge_name}.yaml on the host at /etc/netplan/.',
        'msg_001': f'Public Bridge config file /etc/netplan/{subnet_bridge_name}.yaml already built, so exiting.',
        'msg_010': f'Public Bridge config file /etc/netplan/{subnet_bridge_name}.yaml created.',
        'msg_032': f'Failed to build Subnet Bridge #{subnet_bridge_name} for PodNet {host_ip}',
    }

    template_data = {
        'subnet_bridge_address_range': subnet_bridge_address_range,
        'subnet_bridge_interface': subnet_bridge_interface,
        'subnet_bridge_name': subnet_bridge_name,
        'messages': subnet_bridge_build_messages,
    }

    # ensure all the required keys are collected and no key has None value for template_data
    template = JINJA_ENV.get_template(template_name)
    template_verified, template_error = check_template_data(template_data, template)
    if not template_verified:
        logger.debug(
            f'Failed to generate PodNet Subnet bridge config for bridge #{subnet_bridge_name}.\n{template_error}',
        )
        return False, template_error

    # Prepare subnet bridge build config
    bash_script = template.render(**template_data)
    logger.debug(
        f'Generated build bash script for Public Bridge #{subnet_bridge_name}\n{bash_script}',
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
            f'PodNet Subnet Bridge #{subnet_bridge_name} on #{host_ip} build commands generated stdout.'
            f'\n{rcc_output}',
        )
        for message in subnet_bridge_build_messages.values():
            if message in rcc_output:
                out += message
                if message == subnet_bridge_build_messages['msg_000'] or \
                        message == subnet_bridge_build_messages['msg_001']:
                    success = True
    if rcc_error:
        logger.error(
            f'PodNet Subnet Bridge #{subnet_bridge_name} on #{host_ip} build commands generated stderr.'
            f'\n{rcc_error}',
        )

    if debug:
        out += rcc_output
        out += rcc_error

    return success, out
