import bodosdk
from bodosdk.api.auth import AuthApi
from bodosdk.api.request_wrapper import RequestWrapper


class BackendApi:
    def __init__(
        self,
        auth_api: AuthApi,
        api_url="https://api.bodo.ai/api",
        requests=RequestWrapper(),
    ):
        self._requests = requests
        self._auth_api = auth_api
        self._base_url = api_url
        self._resource_url = ""

    def get_auth_header(self):
        token = self._auth_api.auth_token
        return {
            "Authorization": f"Bearer {token}",
            "SDK-Version": bodosdk._version.get_versions().get("version"),
        }

    def get_resource_url(self, version=None):
        if not self._resource_url:
            return f"{self._base_url}/{version}" if version else self._base_url

        return (
            f"{self._base_url}/{version}/{self._resource_url}"
            if version
            else f"{self._base_url}/{self._resource_url}"
        )
