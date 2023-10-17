from nerdcore.base_entities.deployment_class import Deployment
from nerdcore.utils.nerd.theme_functions import print_t


class ExampleDeployment(Deployment):

    # Note: It is important to review the base class constructor / general behavior.
    #       It is also important to be aware of the capabilities of the CliRunnable class.

    required_config_keys = []
    allowed_dirs = []

    def run(self):
        print_t(self.nerd_config, 'info')
        print_t(self.config_name, 'info')
        print_t('Example run run() method called. You need to implement it.', 'super_important')


"""
The following may also be overridden from Deployment class.

 - load_config() for custom config loading logic.
 - validate_config() for custom NerdConfig validation logic.
 - __init__() for custom initialization logic.
"""
