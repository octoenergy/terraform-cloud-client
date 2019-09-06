from unittest import mock

import pytest

import tfc

# In the actually API response the "relationships" dictionary is populated. Leaving it unpopulated
# here because we don't use it and it's quite large.
api_response_to_create_run = """
{
    "data": {
        "id": "run-somerunid",
        "type": "runs",
        "attributes": {
            "actions": {
                "is-cancelable": true,
                "is-confirmable": false,
                "is-discardable": false,
                "is-force-cancelable": false
            },
            "canceled-at": null,
            "created-at": "2019-01-02T03:04:05.006Z",
            "has-changes": false,
            "is-destroy": false,
            "message": "Some message",
            "plan-only": false,
            "source": "tfc-api",
            "status-timestamps": {},
            "status": "pending",
            "trigger-reason": "manual",
            "permissions": {
                "can-apply": true,
                "can-cancel": true,
                "can-discard": true,
                "can-force-execute": true,
                "can-force-cancel": true
            }
        },
        "relationships": {},
        "links": {
            "self": "/api/v2/runs/run-somerunid"
        }
    }
}
"""


@mock.patch("urllib.request")
def test_create_run_happy_path(mock_request):
    request_constructor = mock.Mock()
    mock_request.Request = request_constructor
    response = mock.Mock()
    response.getcode.return_value = 201
    response.read.return_value = api_response_to_create_run
    mock_request.urlopen.return_value = response

    client = tfc.TerraformClient("my_token", "my_org", "my_workspace")
    client._workspace_id = "workspaceid"

    run = client.create_run("my_message")

    request_constructor.assert_called_once_with(
        "https://app.terraform.io/api/v2/runs",
        data=b'{"data": {"attributes": {"is-destroy": false, "message": "my_message"}, "type": "runs", "relationships": {"workspace": {"data": {"type": "workspaces", "id": "workspaceid"}}}}}',
        headers={"Authorization": "Bearer my_token", "Content-Type": "application/vnd.api+json"},
        method="POST",
    )
    assert run.id == "run-somerunid"


@mock.patch("urllib.request")
def test_create_run_invalid_key_raise_terraform_error(mock_request):
    response = mock.Mock()
    response.getcode.return_value = 401
    mock_request.urlopen.return_value = response

    client = tfc.TerraformClient("my_token", "my_org", "my_workspace")
    with pytest.raises(tfc.TerraformError, match="Received status code 401. Expected 200"):
        client.create_run("my_message")


@mock.patch("urllib.request")
def test_create_run_invalid_org_or_workspace_raise_terraform_error(mock_request):
    response = mock.Mock()
    response.getcode.return_value = 404
    mock_request.urlopen.return_value = response

    client = tfc.TerraformClient("my_token", "my_org", "my_workspace")
    with pytest.raises(tfc.TerraformError, match="Received status code 404. Expected 200"):
        client.create_run("my_message")
