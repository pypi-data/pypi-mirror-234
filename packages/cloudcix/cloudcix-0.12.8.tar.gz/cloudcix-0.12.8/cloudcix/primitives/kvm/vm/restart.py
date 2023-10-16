# stdlib
import hashlib
import logging
from typing import Tuple
# libs
from jinja2 import meta
# local
from cloudcix.primitives.utils import JINJA_ENV
from cloudcix.rcc import deploy_ssh, CouldNotConnectException


def restart(host_ip: str, vm_name: str) -> Tuple[int, str]:
    logger = logging.getLogger(__name__)
    logger.debug('Compiling data for vm.restart')

    success_id = hashlib.sha256(vm_name.encode()).hexdigest()[:10]
    template_data = {
        'vm_name': vm_name,
        'success_id': success_id,
    }

    bash_script = JINJA_ENV.get_template(
        'kvm/vm/restart.sh.j2',
    ).render(template_data)
    # Check if there are any values that are still undefined
    parsed = JINJA_ENV.parse(bash_script)
    undefined_vars = meta.find_undeclared_variables(parsed)
    if undefined_vars:
        return False, f'The following variables were not passed to the kvm.vm.restart template : {undefined_vars}'

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
