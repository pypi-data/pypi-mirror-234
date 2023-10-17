import sys

from nerdcore.defs import import_env_class
from nerdcore.utils.nerd.theme_functions import print_t

ENV = import_env_class()
ENV = ENV.get()


def nerd_env_checks():

    version = sys.version_info[0]

    if version < 3:
        print_t("It appears you're running Python 2. Please use Python 3.", 'error')
        sys.exit(1)
