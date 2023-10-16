import re


class NoPackageNameException(Exception):
    def __init__(self):
        super().__init__('No package name provided')


class EmptyPackageNameException(Exception):
    def __init__(self):
        super().__init__('Package name is empty')


class InvalidPackageNameException(Exception):
    def __init__(self, package_name: str, hint: str):
        message = f'Package name {package_name} is not a valid name'

        if hint:
            message = f'{message}. HINT: {hint}'
        super().__init__(message)


def evaluate_package(package_regex: str, hint: str, **props):
    ATTRITBUTE_PACKAGE = 'package'

    if ATTRITBUTE_PACKAGE not in props:
        raise NoPackageNameException()
    else:
        package = props[ATTRITBUTE_PACKAGE]
    
    if not package:
        raise EmptyPackageNameException()
    elif not re.match(package_regex, package):
        raise InvalidPackageNameException(package, hint)
    return package
