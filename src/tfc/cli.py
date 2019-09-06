import argparse
import os
import sys

from . import client, message_variables

DEFAULT_RUN_MESSAGE = "Run triggered by `tfc` command line tool"


class MessageVariableMapping:
    """
    Wrapper for the tfc.message_variables module

    Wraps the tfc.message_variables module in a mapping (dictionary like) interface. The name of
    each function in tfc.message_variables becomes a key in the mapping and the value is the result
    of running that function with no arguments.

    This wrapper effectively allows us to lazily pass all of the results from the functions in
    tfc.message_variables into str.format() (i.e. without running functions which are not used by
    the format string)
    """

    def __getitem__(self, key):
        func = getattr(message_variables, key)
        if getattr(func, "is_message_variable", False):
            return func()
        else:
            raise KeyError(key)


def trigger_run_with_variables(organization, workspace, message, assignments):
    token = os.environ["TERRAFORM_CLOUD_TOKEN"]
    terraform = client.TerraformClient(token, organization, workspace)
    vars = terraform.get_variables()

    for (variable_name, new_value) in assignments.items():
        variable = vars[variable_name]
        terraform.update_variable(variable.id, new_value)
        old_value = variable.value
        print(f"Updated {variable_name!r} from {old_value!r} to {new_value!r}")

    run = terraform.create_run(message)
    print(f"Created run {run.id} - check status at: {run.url}")


def variable_assignment(value):
    if "=" not in value:
        raise argparse.ArgumentTypeError(
            f"Expected an assignment with an equals sign, got {value!r}"
        )
    return value


def get_command_line_arguments(argv):
    parser = argparse.ArgumentParser(
        description="Trigger a Terraform Cloud run",
        epilog="Put your API token in the TERRAFORM_CLOUD_TOKEN environment variable",
    )
    parser.add_argument("organization", help="The name of your organization in Terraform Cloud")
    parser.add_argument("workspace", help="The name of your workspace in Terraform Cloud")
    parser.add_argument(
        "variables",
        metavar="name=value",
        type=variable_assignment,
        nargs="*",
        help="Set terraform variable NAME to VALUE before creating the run",
    )
    parser.add_argument(
        "--message",
        "-m",
        help="The message to be associated with this run",
        default=DEFAULT_RUN_MESSAGE,
    )

    args = parser.parse_args(argv[1:])
    args.variables = dict([v.split("=", 1) for v in args.variables])
    return args


def main(argv=sys.argv):
    """The entry point when running `tfc` as a script"""
    args = get_command_line_arguments(argv)
    message = args.message.format_map(MessageVariableMapping())
    trigger_run_with_variables(args.organization, args.workspace, message, args.variables)
    return 0
