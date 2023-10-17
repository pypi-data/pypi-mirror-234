from nerdcore.base_entities.command_class import Command
from nerdcore.ncdefs import VERSION
from nerdcore.utils.nerd.theme_functions import print_t


class Version(Command):

    def run(self):
        print_t(f"Nerd CLI v{VERSION}", 'nerd')
