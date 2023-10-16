from caos._internal.constants import ValidDependencyVersionRegex
from caos._internal.exceptions import InvalidDependencyVersionFormat, UnexpectedError
from typing import NewType

PipReadyDependency = NewType(name="PipReadyDependency", tp=str)


def _is_dependency_name_in_wheel(dependency_name: str, wheel: str, version: str) -> bool:
    wheel = wheel[:-1*len("-{}".format(version))]\
            .replace("_", "-")\
            .lower()
    return wheel.endswith(dependency_name.replace("_", "-").lower())


def _get_dependency_version_format(dependency_name: str, version: str) -> ValidDependencyVersionRegex:
    """
    Raises:
        InvalidDependencyVersionFormat
    """
    if ValidDependencyVersionRegex.MAJOR_MINOR_PATCH.value.match(version):
        return ValidDependencyVersionRegex.MAJOR_MINOR_PATCH

    if ValidDependencyVersionRegex.MAJOR_MINOR.value.match(version):
        return ValidDependencyVersionRegex.MAJOR_MINOR

    if ValidDependencyVersionRegex.MAJOR.value.match(version):
        return ValidDependencyVersionRegex.MAJOR

    if ValidDependencyVersionRegex.LATEST.value.match(version):
        return ValidDependencyVersionRegex.LATEST

    wheel_info = ValidDependencyVersionRegex.WHEEL.value.match(version)
    if wheel_info:
        wheel = wheel_info.group("wheel")
        wheel_version = wheel_info.group("version")
        if not _is_dependency_name_in_wheel(dependency_name=dependency_name, wheel=wheel, version=wheel_version):
            raise InvalidDependencyVersionFormat(
                "The dependency '{dep}' is not present in the wheel filename '{wheel}'"
                .format(dep=dependency_name, wheel=version)
            )

        if not ValidDependencyVersionRegex.MAJOR_MINOR_PATCH.value.match(wheel_version) and \
           not ValidDependencyVersionRegex.MAJOR_MINOR.value.match(wheel_version) and \
           not ValidDependencyVersionRegex.MAJOR.value.match(wheel_version):

            raise InvalidDependencyVersionFormat(
                "\nThe version format for the wheel dependency '{dep}' is invalid. Use a 'Final release' format "
                "(see https://www.python.org/dev/peps/pep-0440/#final-releases)"
                .format(dep=dependency_name)
            )

        return ValidDependencyVersionRegex.WHEEL

    if ValidDependencyVersionRegex.TARGZ.value.match(version):
        return ValidDependencyVersionRegex.TARGZ

    raise InvalidDependencyVersionFormat(
        "\nInvalid version format for the dependency '{dep}'. Only the following formats are allowed:"
        "\n  - 'latest' or 'LATEST'"
        "\n  - Final release format (see https://www.python.org/dev/peps/pep-0440/#final-releases)"
        "\n  - Wheel Binary Packages (see https://www.python.org/dev/peps/pep-0491/#file-format)"
        "\n  - .tar.gz Packages"
        .format(dep=dependency_name)
    )


def generate_pip_ready_dependency(dependency_name: str, version: str) -> PipReadyDependency:
    """
    Raises:
        InvalidDependencyVersionFormat
        UnexpectedError
    """
    dependency_regex: ValidDependencyVersionRegex = _get_dependency_version_format(
        dependency_name=dependency_name,
        version=version
    )

    if dependency_regex == ValidDependencyVersionRegex.MAJOR_MINOR_PATCH:  # (^|~) X.X.X
        if version.startswith("~"):  # Allow patch updates
            return version.replace("~", "~=")  # ~=X.X.X

        elif version.startswith("^"):  # Allow minor updates
            version = version.replace("^", "")
            major, minor, patch = version.split(".")
            return "~={}.{}".format(major, minor)  # ~=X.X

        else:  # Allow exact version
            return "=={}".format(version)  # ==X.X.X

    elif dependency_regex == ValidDependencyVersionRegex.MAJOR_MINOR:
        if version.startswith("~"):  # Allow patch updates
            version = version.replace("~", "")
            major, minor = version.split(".")
            return "~={}.{}.0".format(major, minor)  # ~=X.X.0

        elif version.startswith("^"):  # Allow minor updates
            version = version.replace("^", "~=")
            return version  # ~=X.X

        else:  # Allow exact version
            return "=={}".format(version)  # ==X.X

    elif dependency_regex == ValidDependencyVersionRegex.MAJOR:
        if version.startswith("~"):  # Allow patch updates
            version = version.replace("~", "")
            return "~={}.0.0".format(version)  # ~=X.0.0

        elif version.startswith("^"):  # Allow minor updates
            version = version.replace("^", "")
            return "~={}.0".format(version)  # ~=X.0

        else:  # Allow exact version
            return "=={}".format(version)  # ==X

    elif dependency_regex == ValidDependencyVersionRegex.LATEST:
        return dependency_name.lower()

    elif dependency_regex == ValidDependencyVersionRegex.WHEEL:
        return version

    elif dependency_regex == ValidDependencyVersionRegex.TARGZ:
        return version

    raise UnexpectedError("The dependency given should have thrown 'InvalidDependencyVersionFormat' but it did not")
