import argparse
from typing import Dict, Any, List

from nerdcore.base_entities.utils.cli_runnable_class import CliRunnable
from nerdcore.defs import import_nerd_config_class
from nerdcore.utils.nerd.theme_functions import print_t
from nerdcore.utils.nerd_config.load_nerd_config import load_nerd_config

NerdConfig = import_nerd_config_class()


class Deployment(CliRunnable):
    named_arg_keys = ['config']
    config: str = None

    # Override this in subclasses to define required nerd config keys.
    required_config_keys = []

    def __init__(self, nerd_args: argparse.Namespace, named_args: Dict[str, Any], unnamed_args: List[str]):

        super().__init__(nerd_args, named_args, unnamed_args)

        _nerd_config, _config_name = self.load_config()
        self.nerd_config: NerdConfig = _nerd_config
        self.config_name: str = _config_name

        self.validate_config()
        _class_name = self.__class__.__name__

        print_t(f"{_class_name} deployment initialized with config: {_config_name}.", "start")

    """
    Override this method to define custom nerd config loading logic.
    Default is to load from --config=config-name or use loaded config / selection logic.
    Must return a Tuple of (NerdConfig, config_name string), which is the return of load_nerd_config().
    """
    def load_config(self) -> (NerdConfig, str):
        return load_nerd_config(self.config)

    """
    Override this method to define custom config validation logic (or just set required_config_keys).
    """
    def validate_config(self):
        missing_keys = [key for key in self.required_config_keys if key not in vars(self.nerd_config)]
        if missing_keys:
            raise ValueError(f"Missing required config keys: {', '.join(missing_keys)}")

    def run(self):
        raise NotImplementedError("The main() method must be implemented in a subclass of Deployment.")
