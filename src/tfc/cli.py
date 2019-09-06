import argparse
import os
import sys

from . import client

DEFAULT_RUN_MESSAGE = "Run triggered by `tfc` command line tool"


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
    parser.add_argument(
        "organization", help="The name of your organization in Terraform Cloud"
    )
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
    trigger_run_with_variables(args.organization, args.workspace, args.message, args.variables)
    return 0
