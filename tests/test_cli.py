from unittest import mock

import pytest

import tfc.cli


@mock.patch.object(tfc.cli, "client")
def test_cli_run_wth_no_variables_or_message(mock_client_module, monkeypatch):
    monkeypatch.setenv("TERRAFORM_CLOUD_TOKEN", "my_token")
    client = mock_client_module.TerraformClient.return_value

    tfc.cli.main(argv=["tfc", "my_org", "my_workspace"])

    mock_client_module.TerraformClient.assert_called_once_with(
        "my_token", "my_org", "my_workspace"
    )
    client.update_variable.assert_not_called()
    client.create_run.assert_called_once_with(tfc.cli.DEFAULT_RUN_MESSAGE)


@mock.patch.object(tfc.cli, "client")
def test_cli_run_with_message(mock_client_module, monkeypatch):
    monkeypatch.setenv("TERRAFORM_CLOUD_TOKEN", "my_token")
    client = mock_client_module.TerraformClient.return_value

    tfc.cli.main(argv=["tfc", "my_org", "my_workspace", "--message=my_message"])

    mock_client_module.TerraformClient.assert_called_once_with(
        "my_token", "my_org", "my_workspace"
    )
    client.update_variable.assert_not_called()
    client.create_run.assert_called_once_with("my_message")


@mock.patch.object(tfc.cli, "client")
def test_cli_run_with_variable_being_set(mock_client_module, monkeypatch):
    monkeypatch.setenv("TERRAFORM_CLOUD_TOKEN", "my_token")
    client = mock_client_module.TerraformClient.return_value
    client.get_variables.return_value = {"foo": mock.Mock(name="foo", id="foo_id")}

    tfc.cli.main(argv=["tfc", "my_org", "my_workspace", "foo=bar"])

    mock_client_module.TerraformClient.assert_called_once_with(
        "my_token", "my_org", "my_workspace"
    )
    client.get_variables.assert_called_once_with()
    client.update_variable.assert_called_once_with("foo_id", "bar")
    client.create_run.assert_called_once()
