# stdlib
import hashlib
import logging
from typing import Tuple
# local
from cloudcix.primitives.utils import check_template_data, JINJA_ENV
from cloudcix.rcc import deploy_ssh, CouldNotConnectException


def update(host_ip: str, device_size: int, device_name: str, pool_name: str) -> Tuple[int, str]:
    logger = logging.getLogger(__name__)
    logger.debug('Compiling data for ceph.update')

    success_id = hashlib.sha256(
        (str(device_size) + device_name + pool_name).encode(),
    ).hexdigest()[:10]
    template_data = {
        'device_size': device_size,
        'device_name': device_name,
        'pool_name': pool_name,
        'success_id': success_id,
    }

    template = JINJA_ENV.get_template('kvm/ceph/update.sh.j2')
    valid, error = check_template_data(template_data, template)
    if not valid:
        return valid, error
    bash_script = template.render(template_data)

    # Deploy the command to the hosts
    try:
        stdout, stderr = deploy_ssh(host_ip, payload=bash_script)
    except CouldNotConnectException as e:
        return False, str(e)

    # Check if we reached a desired end-state
    last_newline = stdout.rfind('\n')
    last_line = stdout[last_newline + 1:]
    success = last_line == success_id
    output = ''
    if success:
        output = stdout[:last_newline].strip()
    if stderr:
        output += f'\nstderr: {stderr.strip()}'

    return success, output
