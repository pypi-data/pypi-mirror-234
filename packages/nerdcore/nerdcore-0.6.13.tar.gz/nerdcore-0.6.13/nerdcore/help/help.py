import argparse

from nerdcore.defs import nl2, nl
from nerdcore.utils.nerd.theme_functions import print_banner, print_table, print_t, apply_t


def run_default_help(nerd_args: argparse.Namespace = None):

    # Nerd CLI Banner
    print_banner()

    # Overview
    print_t("Welcome to Nerd CLI, a Fivable-specific utility for console commands and deployments.", 'white')

    # Recursive Name-Matching Logic
    print_t("`nerd` employs recursive name-matching logic to locate nerdcore/usr entities. This requires unique "
            "filenames within each entity directory. While this is limiting, it also keeps things simple, "
            f"customizable, and powerful.{nl}", 'important')

    # Handling of Deployments and Modules
    print_t("Entity Type flags allow you to target deployments (-d).", 'info')

    # Action Flags
    print_t(f"Action flags allow you to perform a variety of operations on any targetable entity.{nl2}", 'info')

    min_col_widths = [23, 25, 13]

    nerd_general_json = {
      "headers": [
        "Command",
        "Description",
        "Note"
      ],
      "show_headers": False,
      "rows": [
        [
          "nerd help",
          "Run this help script",
          ""
        ],
        [
          "nerd list",
          "List existing entities",
          "-b/a/m, --all"
        ],
        [
          "nerd -v",
          "Print version",
          "--version"
        ],
        [
          "nerd <command>",
          "Run a command",
          "default action/entity"
        ]
      ]
    }
    print_table(nerd_general_json, apply_t("Nerd CLI", 'special'), min_col_width=min_col_widths)

    nerd_types = {
      "headers": [
        "Command",
        "Description",
        "Note"
      ],
      "show_headers": False,
      "rows": [
        [
          "nerd -d <deployment>",
          "Run an deployment",
          "--deployment"
        ],
      ]
    }
    print_table(nerd_types, apply_t("Entity Types", 'special'), min_col_width=min_col_widths)

    nerd_actions = {
      "headers": [
        "Command",
        "Description",
        "Note"
      ],
      "show_headers": False,
      "rows": [
        [
          "nerd -r <entity>",
          "Run an entity",
          "--run"
        ],
        [
          "nerd -e <entity>",
          "Open in vim",
          "--edit"
        ],
        [
          "nerd -p <entity>",
          "Print file contents",
          "--print"
        ],
        [
          "nerd -cp <entity>",
          "Copy file abspath",
          "--copy-path"
        ],
        [
          "nerd -cc <entity>",
          "Copy file contents",
          "--copy-contents"
        ],
        [
          "nerd -h <entity>",
          "Help for an entity",
          "--help"
        ]
      ]
    }
    print_table(nerd_actions, apply_t("Actions", 'special'), min_col_width=min_col_widths)

    # Wrap up
    print_t("That's it! For more info, run `nerd -h <entity>` or view the docs.", 'done')
    exit(0)
