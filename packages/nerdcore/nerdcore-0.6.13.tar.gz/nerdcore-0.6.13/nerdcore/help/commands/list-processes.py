from nerdcore.utils.nerd.theme_functions import print_t, print_table


def main():
    print_t("List Processes Help", "important")
    print_t("The `list-processes` command provides an overview of all ongoing nerd processes, their process IDs (PIDs),"
            "and commands to kill them.")

    print_t("nerd list-processes", "input")

    print_t("Usage:", "info")
    print_t("1. Execute `nerd list-processes` to display a table with detailed information", "info")
    print_t("2. Use the provided kill commands to terminate a specific nerd process if needed", "info")

    print_t("Example of a table displayed after running `nerd list-processes`:", "tip")

    USAGE_EXAMPLES_TABLE = {
        "headers": [
            "PID",
            "Command",
            "Kill Command"
        ],
        "show_headers": True,
        "rows": [
            [
                "1234",
                "nerd make deployment new-deployment",
                "kill 1234"
            ],
            [
                "4567",
                "nerd -d LeadDeployment",
                "kill 4567"
            ],
        ]
    }

    print_table(USAGE_EXAMPLES_TABLE, "Usage")

    print_t("Important: Always exercise caution when terminating processes to avoid disrupting your workspace.", "warning")
