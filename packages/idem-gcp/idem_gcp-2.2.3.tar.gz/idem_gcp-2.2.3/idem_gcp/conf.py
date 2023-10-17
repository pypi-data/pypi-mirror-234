# https://pop.readthedocs.io/en/latest/tutorial/quickstart.html#adding-configuration-data
# In this dictionary goes all the immutable values you want to show up under hub.OPT.idem_gcp
CONFIG = {
    "config": {
        "default": None,
        "help": "Load extra options from a configuration file onto hub.OPT.idem_gcp",
    },
    # pop-create options
    "services": {
        "default": [],
        "nargs": "*",
        "help": "The cloud services to target, defaults to all",
        "dyne": "pop_create",
    },
}

# The selected subcommand for your cli tool will show up under hub.SUBPARSER
# The value for a subcommand is a dictionary that will be passed as kwargs to argparse.ArgumentParser.add_subparsers
SUBCOMMANDS = {
    # "my_sub_command": {}
    "gcp": {
        "help": "Create idem_gcp state modules by parsing Google Cloud Client libraries",
        "dyne": "pop_create",
    },
}

# Include keys from the CONFIG dictionary that you want to expose on the cli
# The values for these keys are a dictionaries that will be passed as kwargs to argparse.ArgumentParser.add_option
CLI_CONFIG = {
    "config": {"options": ["-c"]},
    # "my_option1": {"subcommands": ["A list of subcommands that exclusively extend this option"]},
    # This option will be available under all subcommands and the root command
    # "my_option2": {"subcommands": ["_global_"]},
    "services": {
        "subcommands": ["gcp"],
        "dyne": "pop_create",
    },
}

# These are the namespaces that your project extends
# The hub will extend these keys with the modules listed in the values
DYNE = {
    "states": ["states"],
    "exec": ["exec"],
    "tool": ["tool"],
    "acct": ["acct"],
    "metadata": ["metadata"],
    "autogen": ["autogen"],
}
