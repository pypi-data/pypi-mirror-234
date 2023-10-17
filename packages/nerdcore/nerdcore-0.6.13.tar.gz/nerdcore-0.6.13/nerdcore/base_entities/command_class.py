from nerdcore.base_entities.utils.cli_runnable_class import CliRunnable


class Command(CliRunnable):
    """
    Command is a base class for framework and user-created Commands for the `nerd` CLI.
    It processes named and unnamed arguments and provides a `main` method to be implemented.
    Run `nerd make <name>` to create a new command.
    """

    def run(self):
        raise NotImplementedError("The main() method must be implemented in a subclass of Command.")
