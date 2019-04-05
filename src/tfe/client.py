import json
import urllib.parse
import urllib.request

_TERRAFORM_API_URL = "https://app.terraform.io/api/v2/"


class TerraformError(Exception):
    pass


class TerraformVariable:
    def __init__(self, api_payload):
        self.id = api_payload["id"]
        self.name = api_payload["attributes"]["key"]
        self.value = api_payload["attributes"]["value"]
        self.sensitive = api_payload["attributes"]["sensitive"]

    def __repr__(self):
        if self.sensitive:
            return f"<TerraformVariable id={self.id!r}, name={self.name!r}, sensitive>"
        else:
            return f"<TerraformVariable id={self.id!r}, name={self.name!r}, value={self.value!r}>"


class TerraformClient:
    def __init__(self, token, organization, workspace):
        self.token = token
        self.organization = organization
        self.workspace = workspace

    def _get_headers(self):
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/vnd.api+json",
        }

    def get_variables(self):
        query_params = urllib.parse.urlencode(
            {
                "filter[organization][name]": self.organization,
                "filter[workspace][name]": self.workspace,
            }
        )

        url = f"{_TERRAFORM_API_URL}vars?{query_params}"
        request = urllib.request.Request(url, headers=self._get_headers())
        response = urllib.request.urlopen(request)
        status_code = response.getcode()
        if status_code != 200:
            raise TerraformError(f"Received status code: {status_code}")
        payload = json.load(response)
        variables = [TerraformVariable(var) for var in payload["data"]]
        return {var.name: var for var in variables}

    def update_variable(self, variable_id, new_value):
        url = f"{_TERRAFORM_API_URL}vars/{variable_id}"
        payload = {
            "data": {
                "type": "vars",
                "id": variable_id,
                "attributes": {"value": new_value},
            }
        }
        payload = json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(
            url, headers=self._get_headers(), method="PATCH", data=payload
        )
        response = urllib.request.urlopen(request)
        status_code = response.getcode()
        if status_code != 200:
            raise TerraformError(f"Received status code: {status_code}")
