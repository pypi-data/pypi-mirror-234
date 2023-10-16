# stdlib
from typing import Any, Dict, Tuple
# libs
from jinja2 import Environment, meta, PackageLoader, Template


__all__ = [
    'check_template_data',
    'JINJA_ENV',
]

JINJA_ENV = Environment(
    loader=PackageLoader('cloudcix.primitives'),
    trim_blocks=True,
)


def check_template_data(template_data: Dict[str, Any], template: Template) -> Tuple[bool, str]:
    """
    Verifies for any key in template_data is missing.
    :param template_data: dictionary object that must have all the template_keys.
    :param template: The template to be verified
    :return: tuple of boolean flag, success and the error string if any
    """
    with open(template.filename, 'r') as fp:
        template_source = fp.read()

    parsed = JINJA_ENV.parse(source=template_source)
    required_keys = meta.find_undeclared_variables(parsed)
    err = ''
    for k in required_keys:
        if k not in template_data:
            err += f'Key `{k}` not found in template data.\n'

    success = '' == err
    return success, err
