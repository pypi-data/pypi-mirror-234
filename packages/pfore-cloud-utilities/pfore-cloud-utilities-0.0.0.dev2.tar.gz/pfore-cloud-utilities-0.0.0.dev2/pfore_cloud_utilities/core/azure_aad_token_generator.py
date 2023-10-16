import datetime

from azure.identity import DefaultAzureCredential, ClientSecretCredential

from .define import AAD_RESOURCE_NAME_TO_ID
from .singleton import Singleton


class AADTokenGenerator(metaclass=Singleton):
    """Singleton class to handle AAD token generation of AAD resources.

    Connection is created using either a managed identity or an SPN.

    If spn_client_id or spn_client_secret are set to None, the client
    will assume Managed Identity as an authentication method.

    Args:
        azure_tenant_id: Azure tenant ID, required
        spn_client_id: Service Principal client ID
        spn_client_secret: Service Principal client secret

    """

    def __init__(
            self,
            azure_tenant_id: str,
            spn_client_id: str = None,
            spn_client_secret: str = None,
            ) -> None:

        if spn_client_id is None or spn_client_secret is None:
            self._credentials = DefaultAzureCredential()
        else:
            self._credentials = ClientSecretCredential(
                tenant_id=azure_tenant_id,
                client_id=spn_client_id,
                client_secret=spn_client_secret,
            )
        self._token = dict()

    def get_token(self, aad_resource_name: str) -> str:
        """Helper method that uses `_credentials` variables
        to make calls to the AAD API to generate token
        using Managed Identities or SPNs based connection.

        Args:
            aad_resource_name: AAD resource name

        Returns:
            AAD token, valid for 60 minutes.

        Raises:
            NotImplementedError: If the specified `aad_resource_name`
            does not exist in `AAD_RESOURCE_NAME_TO_ID`, defined in `define.py`

        """
        if aad_resource_name not in AAD_RESOURCE_NAME_TO_ID.keys():
            raise NotImplementedError(
                'Please specify a valid AAD resource name.'
            )

        # AAD token is only valid for 1 hour
        if not (aad_resource_name in self._token.keys()) or (
            (datetime.datetime.now() -
             self._token[aad_resource_name]['date']).seconds // 60 >= 58
        ):
            self._token[aad_resource_name] = dict()
            self._token[aad_resource_name]['date'] = datetime.datetime.now()
            self._token[aad_resource_name][
                'token'
            ] = self._credentials.get_token(
                f"{AAD_RESOURCE_NAME_TO_ID[aad_resource_name]}/.default"
            ).token

        return self._token[aad_resource_name]['token']
