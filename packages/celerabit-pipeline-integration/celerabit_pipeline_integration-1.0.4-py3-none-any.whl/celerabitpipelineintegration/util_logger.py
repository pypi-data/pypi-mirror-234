
from celerabitpipelineintegration.util_configuration import Configuration


DEBUG_TYPE:str = 'debug'
INFO_TYPE:str = 'info'
WARN_TYPE:str = 'warn'
ERROR_TYPE:str = 'error'

def __print_message__(type:str, *args):
    message:str = type.upper() + ' :: ' + ('\n' if type.strip().lower() == ERROR_TYPE else '')
    for arg in args:
        if isinstance(arg, list):
            message += '['
            for item in arg:
                message += str(item) + ', '
            message = message[0, len(message) - 2]
            message += ']'
        else:
            message += (str(arg) + '\t')

    print(' *-*-*-* {message}'.format(message = message))

def print_debug(*args):
    if  not Configuration.instance().get_config_value('LOGGER', 'quiet') and \
        Configuration.instance().get_config_value('LOGGER', 'level') == 'DEBUG':
        __print_message__(DEBUG_TYPE, args)

def print_info(*args):
    if  not Configuration.instance().get_config_value('LOGGER', 'quiet'):
        __print_message__(INFO_TYPE, args)

def print_warn(*args):
    if  not Configuration.instance().get_config_value('LOGGER', 'quiet'):
        __print_message__(WARN_TYPE, args)

def print_error(*args):
    __print_message__(ERROR_TYPE, args)
