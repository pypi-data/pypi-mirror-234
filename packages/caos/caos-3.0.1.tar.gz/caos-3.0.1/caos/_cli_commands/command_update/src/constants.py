NAME: str = "update"
DESCRIPTION: str = """\
            Downloads the missing dependencies of the project
            and upgrades the ones with newer minor or patch versions,
            according to the defined configuration.
            
            It requires an existing 'caos.yml' file and a virtual
            environment in the current directory.\
"""
CLI_USAGE_EXAMPLE: str = """\
            caos update
"""
