from unittest import mock

import pytest

import tfc

api_response_to_vars_query = """
{
    "data": [
        {
            "id": "var-someid1",
            "type": "vars",
            "attributes": {
                "key": "variable_1",
                "value": "value_1",
                "sensitive": false,
                "category": "terraform",
                "hcl": false,
                "created-at": "2019-01-02T03:04:05.006Z"
            },
            "relationships": {
                "configurable": {
                    "data": {
                        "id": "ws-workspaceid",
                        "type": "workspaces"
                    },
                    "links": {
                        "related": "/api/v2/organizations/my_org/workspaces/my_workspace"
                    }
                }
            },
            "links": {
                "self": "/api/v2/vars/var-someid1"
            }
        },
        {
            "id": "var-someid2",
            "type": "vars",
            "attributes": {
                "key": "variable_2",
                "value": "value_2",
                "sensitive": true,
                "category": "terraform",
                "hcl": false,
                "created-at": "2019-01-02T03:04:05.006Z"
            },
            "relationships": {
                "configurable": {
                    "data": {
                        "id": "ws-workspaceid",
                        "type": "workspaces"
                    },
                    "links": {
                        "related": "/api/v2/organizations/my_org/workspaces/my_workspace"
                    }
                }
            },
            "links": {
                "self": "/api/v2/vars/var-someid2"
            }
        }
    ]
}
"""


@mock.patch("urllib.request")
def test_get_variables_happy_path(mock_request):
    request_constructor = mock.Mock()
    mock_request.Request = request_constructor
    response = mock.Mock()
    response.getcode.return_value = 200
    response.read.return_value = api_response_to_vars_query
    mock_request.urlopen.return_value = response

    client = tfc.TerraformClient("my_token", "my_org", "my_workspace")
    variables = client.get_variables()

    request_constructor.assert_called_once_with(
        "https://app.terraform.io/api/v2/vars?filter%5Borganization%5D%5Bname%5D=my_org&filter%5Bworkspace%5D%5Bname%5D=my_workspace",
        headers={"Authorization": "Bearer my_token", "Content-Type": "application/vnd.api+json"},
    )
    assert all(isinstance(v, tfc.TerraformVariable) for v in variables.values())
    assert {k: v.__dict__ for (k, v) in variables.items()} == {
        "variable_1": {
            "id": "var-someid1",
            "name": "variable_1",
            "sensitive": False,
            "value": "value_1",
        },
        "variable_2": {
            "id": "var-someid2",
            "name": "variable_2",
            "sensitive": True,
            "value": "value_2",
        },
    }


@mock.patch("urllib.request")
def test_get_variables_invalid_key_raise_terraform_error(mock_request):
    response = mock.Mock()
    response.getcode.return_value = 401
    mock_request.urlopen.return_value = response

    client = tfc.TerraformClient("my_token", "my_org", "my_workspace")
    with pytest.raises(tfc.TerraformError, match="Received status code 401. Expected 200"):
        client.get_variables()


@mock.patch("urllib.request")
def test_get_variables_invalid_org_or_workspace_raise_terraform_error(mock_request):
    response = mock.Mock()
    response.getcode.return_value = 404
    mock_request.urlopen.return_value = response

    client = tfc.TerraformClient("my_token", "my_org", "my_workspace")
    with pytest.raises(tfc.TerraformError, match="Received status code 404. Expected 200"):
        client.get_variables()
