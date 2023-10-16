# Primitive for PodNet VPN s2s
# stdlib
import logging
from collections import deque
from typing import Any, Deque, Dict, Tuple
# lib
from netaddr import IPNetwork
# local
import cloudcix.primitives.podnet.vpn_mappings as vpn_mappings
from cloudcix.primitives.utils import check_template_data, JINJA_ENV
from cloudcix.rcc import deploy_ssh, CouldNotConnectException

__all__ = [
    'build',
    'scrub',
]


def build(
        namespace_name: str,
        host_ip: str,
        vpn_ip: str,
        vpns: Deque[Dict[str, Any]],
        debug: bool = False,
) -> Tuple[bool, str]:
    """
    This method :
        - Creates a /tmp/<namespace_name>_vpns.conf file with new config and moves it to /etc/
        - Loads the vpns config

    namespace_name:
        description: Namespace's name to which the firewall rules to be applied
        type: string
    host_ip:
        description: Remote server ip address on which these firewall rules are applied
        type: string
    vpn_ip:
        description: Router side IP address that this VPN is terminating
        type: string
    vpns:
        description: vpns objects of the Project
        type: array
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
    logger.debug('Compiling data for vpns2s.build')
    template_name = 'podnet/vpns2s/build.j2'

    for vpn in vpns:
        routes: Deque[Dict[str, str]] = deque()
        local_ts = []
        remote_ts = []
        for route in vpn['routes']:
            local = IPNetwork(str(route['local_subnet']['address_range'])).cidr
            remote = IPNetwork(str(route['remote_subnet'])).cidr
            routes.append({
                'id': route['id'],
                'local': local,
                'remote': remote,
            })
            local_ts.append(str(local))
            remote_ts.append(str(remote))

        vpn['routes'] = routes

        # version conversion
        vpn['version'] = '1' if vpn['ike_version'] == 'v1-only' else '2'

        # mode
        vpn['aggressive'] = 'yes' if vpn['version'] == '1' else 'no'

        # ipsec_rekey_time = 0.9*ipsec_lifetime (Strongswan working perfectly with rekey_time instead of life_time)
        vpn['ipsec_rekey_time'] = int(0.9 * vpn['ipsec_lifetime'])

        # child SAs, one for each traffic selectors pair
        vpn['child_sas'] = []
        if vpn['traffic_selector']:
            if vpn['version'] == '2':
                local_ts_set = set(local_ts)
                remote_ts_set = set(remote_ts)
                vpn['child_sas'].append({'lts': ','.join(local_ts_set), 'rts': ','.join(remote_ts_set)})
            elif vpn['version'] == '1':
                for route in routes:
                    vpn['child_sas'].append({'lts': route['local'], 'rts': route['remote']})
        else:
            vpn['child_sas'].append({'lts': '0.0.0.0/0', 'rts': '0.0.0.0/0'})

        # tunnel action
        vpn['start_action'] = 'trap' if vpn['ipsec_establish_time'] == 'on-traffic' else 'start'

        # MAP SRX values to Strongswan values
        vpn['ike_authentication_map'] = vpn_mappings.IKE_AUTHENTICATION_MAP[vpn['ike_authentication']]
        vpn['ike_dh_groups_map'] = vpn_mappings.IKE_DH_GROUP_MAP[vpn['ike_dh_groups']]
        vpn['ike_encryption_map'] = vpn_mappings.IKE_ENCRYPTION_MAP[vpn['ike_encryption']]
        vpn['ipsec_authentication_map'] = vpn_mappings.IPSEC_AUTHENTICATION_MAP[vpn['ipsec_authentication']]
        vpn['ipsec_encryption_map'] = vpn_mappings.IPSEC_ENCRYPTION_MAP[vpn['ipsec_encryption']]
        vpn['ipsec_pfs_groups_map'] = vpn_mappings.IPSEC_PFS_GROUP_MAP[vpn['ipsec_pfs_groups']]

        vpns.append(vpn)

    template_data = {
        'vpn_ip': vpn_ip,
        'vpns': vpns,
        'namespace_name': namespace_name,
    }

    # ensure all the required keys are collected and no key has None value for template_data
    template = JINJA_ENV.get_template(template_name)
    template_verified, template_error = check_template_data(template_data, template)
    if not template_verified:
        logger.debug(
            f'Failed to generate S2S VPNs  config for Namespace #{namespace_name}.\n{template_error}',
        )
        return False, template_error

    # Generate VPN build config
    bash_script = template.render(**template_data)
    logger.debug(
        f'Generated PodNet S2S VPNs build bash script for Namespace #{namespace_name}\n{bash_script}',
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
            f'S2S VPNs for namespace #{namespace_name} on #{host_ip} build commands generated stdout.'
            f'\n{rcc_output}',
        )
        success = True
    if rcc_error:
        logger.error(
            f'S2S VPNs for namespace #{namespace_name} on #{host_ip} build commands generated stderr.'
            f'\n{rcc_error}',
        )

    if debug:
        out += rcc_output
        out += rcc_error

    return success, out


def scrub(
        namespace_name: str,
        host_ip: str,
        vpns: Deque[Dict[str, Any]],
        debug: bool = False,
) -> Tuple[bool, str]:
    """
    Removes the /etc/swanctl/conf.d/<namespace_name>_vpns.conf and unloads the Projects vpns
    Removes VPN routes from the namespace network
    Removes VPN firewall rules from namespace nftable firewall rules

    namespace_name:
        description: Namespace's name to which the firewall rules to be applied
        type: string
    host_ip:
        description: Remote server ip address on which these firewall rules are applied
        type: string
    vpns:
        description: vpns objects of the Project
        type: array
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
    logger.debug('Compiling data for vpns2s.scrub')
    template_name = 'podnet/vpns2s/scrub.j2'

    for vpn in vpns:
        routes: Deque[Dict[str, str]] = deque()
        local_ts = []
        remote_ts = []
        for route in vpn['routes']:
            local = IPNetwork(str(route['local_subnet']['address_range'])).cidr
            remote = IPNetwork(str(route['remote_subnet'])).cidr
            routes.append({
                'id': route['id'],
                'local': local,
                'remote': remote,
            })
            local_ts.append(str(local))
            remote_ts.append(str(remote))
        vpn['routes'] = routes
        vpns.append(vpn)

    template_data = {
        'vpns': vpns,
        'namespace_name': namespace_name,
    }

    # ensure all the required keys are collected and no key has None value for template_data
    template_verified, template_error = check_template_data(template_data, template_name)
    if not template_verified:
        logger.debug(
            f'Failed to generate S2S VPNs scrub config for Namespace #{namespace_name}.\n{template_error}',
        )
        return False, template_error

    # Generate VPN scrub config
    bash_script = JINJA_ENV.get_template(template_name).render(**template_data)
    logger.debug(
        f'Generated PodNet VPNS2S scrub bash script for Namespace #{namespace_name}\n{bash_script}',
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
            f'S2S VPNs for namespace #{namespace_name} on #{host_ip} scrub commands generated stdout.'
            f'\n{rcc_output}',
        )
        success = True
    if rcc_error:
        logger.error(
            f'S2S VPNs for namespace #{namespace_name} on #{host_ip} scrub commands generated stderr.'
            f'\n{rcc_error}',
        )

    if debug:
        out += rcc_output
        out += rcc_error

    return success, out
