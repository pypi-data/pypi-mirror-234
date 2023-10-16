# Primitive for PodNet Firewall Global
# stdlib
import logging
from typing import Any, Dict, List, Tuple
# libs
# local
from cloudcix.primitives.utils import check_template_data, JINJA_ENV
from cloudcix.rcc import deploy_ssh, CouldNotConnectException

__all__ = [
    'build',
]


def build(
        firewall_rules: List[Dict[str, Any]],
        global_services: List[str],
        host_ip: str,
        podnet_management_interface: str,
        podnet_public_interface: str,
        debug: bool = False,
) -> Tuple[bool, str]:
    """
    This method :
        - Creates a new /tmp/nftables.conf file with new config
        - Validates the nft file `sudo nft -c -f /tmp/nftables.conf`
        - If any errors then exits with errors Otherwise conf file is moved to /etc/nftables.conf
        - Config is applied at last `sudo nft -f /etc/nftables.conf`

    firewall_rules:
        description: All the Firewall rules for the PodNet. List of dict objects, each dict is of the following format
            rule = {
                'action': 'accept',           # string
                'description': '',            # string
                'destination': [],            # list of strings
                'interface': {                # dictionary
                    'from': 'public',         # string
                    'to': 'management',       # string
                },
                'order': 1                    # integer
                'port': ['22'],               # list of strings
                'protocol': 'tcp',            # string
                'source': [],                 # list of strings
                'version': 6,                 # integer
            }
        type: array

    global_services:
        description: List of global services(strings) applied on Firewall config, eg robosoc
        type: array
    host_ip:
        description: Remote server ip address on which these firewall rules are applied
        type: string
    podnet_management_interface:
        description: Interface name for Podnet Management network
        type: string
    podnet_public_interface:
        description: Interface name for Podnet Public network
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
    logger.debug('Compiling data for firewall_gobal.build')
    template_name = 'podnet/firewall/global_build.j2'

    # template messages
    fail_start = f'Failed to apply Global Firewall config for PodNet {host_ip}.'
    firewall_global_build_messages = {
        'msg_000': 'Successfully applied Firewall config /etc/nftables.conf',
        'msg_010': 'Configuration file /tmp/nftables.conf is valid. Applying the Firewall',
        'msg_032': f'{fail_start} Configuration file /tmp/nftables.conf syntax is invalid. Exiting.',
        'msg_033': f'{fail_start} Configuration file /tmp/nftables.conf Not found.',
    }

    template_data = {
        'firewall_rules': firewall_rules,
        'global_services': global_services,
        'podnet_management_interface': podnet_management_interface,
        'podnet_public_interface': podnet_public_interface,
        'messages': firewall_global_build_messages,
    }

    # ensure all the required keys are collected and no key has None value for template_data
    template = JINJA_ENV.get_template(template_name)
    template_verified, template_error = check_template_data(template_data, template)
    if not template_verified:
        logger.debug(f'Failed to generate PodNet Firewall Global build template. {template_error}')
        return False, template_error

    # Generate Firewall build config
    bash_script = template.render(**template_data)
    logger.debug(
        f'Generated PodNet Firewall Global build bash script:\n{bash_script}',
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
            f'PodNet Firewall Global build commands for #{host_ip} generated stdout.\n{rcc_output}',
        )
        for message in firewall_global_build_messages.values():
            if message in rcc_output:
                out += message
                if message == firewall_global_build_messages['msg_000']:
                    success = True
    if rcc_error:
        logger.error(
            f'PodNet Firewall Global build commands for #{host_ip} generated stderr.\n{rcc_error}',
        )

    if debug:
        out += rcc_output
        out += rcc_error

    return success, out
