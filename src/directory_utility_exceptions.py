class PlatformError(Exception):

    '''
    The exceptions is invoked when the user platform is not supported.
    '''
    pass


class ConfigError(Exception):

    '''
    The exception is invoked if the config file is either missing or corrupt
    or the parameter being queried does not exist.
    '''
    pass


class ExtensionError(Exception):

    '''
    The exception is invoked if the extension file is either missing or corrupt
    or the parameter being queried does not exist.
    '''
    pass
