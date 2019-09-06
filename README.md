# Terraform Cloud Client

An API client for HashiCorp's Terraform Cloud

## Installation

```
$ pip install terraform-cloud-client
```

This client is only tested on python 3.7

## Usage as a library

Set up:

```python
>>> import tfc
>>> client = tfc.TerraformClient("my_api_token", "my_organization", "my_workspace")
```

Get Terraform variables:

```python
>>> variables = client.get_variables()
>>> variables
{
    'my_username': <TerraformVariable id='var-someid1', name='my_username', value='john_doe'>,
    'my_password': <TerraformVariable id='var-someid2', name='my_password', sensitive>,
}
>>> username_variable = variables['my_username']
>>> username_variable.id
'var-someid1'
>>> username_variable.name
'my_username'
>>> username_variable.value
'john_doe'
```

Change the value of a variable:

```python
>>> client.update_variable(variable_id=username_variable.id, new_value='jane_doe')
```

Trigger a run:

```python
>>> run = client.create_run('My message')
>>> run.id
'run-someid'
>>> run.url # Go here in a web browser to view the run
'https://app.terraform.io/app/my_organization/workspaces/my_workspace/runs/run-someid'
```

## Usage as a command line tool

Installing this via pip also installs a `tfc` command line tool

```
$ tfc --help
usage: tfc [-h] [--message MESSAGE]
           organization workspace [name=value [name=value ...]]

Trigger a Terraform Cloud run

positional arguments:
  organization          The name of your organization in Terraform Cloud
  workspace             The name of your workspace in Terraform Cloud
  name=value            Set terraform variable NAME to VALUE before creating
                        the run

optional arguments:
  -h, --help            show this help message and exit
  --message MESSAGE, -m MESSAGE
                        The message to be associated with this run

Put your API token in the TERRAFORM_CLOUD_TOKEN environment variable
```

So for example:

```
$ tfc my_organization my_workspace foo=baz --message="Reticulating splines"
Updated 'foo' from 'bar' to 'baz'
Created run run-g6SmSsLVKg71yeNw - check status at: https://app.terraform.io/app/my_organization/workspaces/my_workspace/runs/run-g6SmSsLVKg71yeNw
```

The message argument can contain variables which are expanded at runtime. These follow the same
formatting rules as Python's `str.format(...)`. The variables which are currently defined are:

- git_repository
- git_branch
- git_commit_subject
- git_commit_author

So for example:

```
$ tfc my_organization my_workspace foo=baz --message="{git_commit_subject} (author: {git_commit_author}, branch: {git_branch}, repo: {git_repository})"
```

might create a run with the message:

```
My commit message (author: Joe Bloggs, branch: my-branch, repo: terraform-cloud-client)
```
