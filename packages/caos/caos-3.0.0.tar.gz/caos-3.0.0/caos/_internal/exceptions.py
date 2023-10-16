class UnsupportedOS(Exception):
    pass


class OpenCaosFileException(Exception):
    pass


class InvalidCaosFileFormat(Exception):
    pass


class MissingKeyInYamlFile(Exception):
    pass


class WrongKeyTypeInYamlFile(Exception):
    pass


class InvalidVirtualEnvironmentFormat(Exception):
    pass


class InvalidDependencyVersionFormat(Exception):
    pass


class MissingBinaryException(Exception):
    pass


class MissingVirtualEnvironmentException(Exception):
    pass


class MissingYamlException(Exception):
    pass


class UnexpectedError(Exception):
    pass