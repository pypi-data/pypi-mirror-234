import os
import base64
import configparser

from databricks.sdk import WorkspaceClient

from .singleton import Singleton


class DatabricksWorkspace(metaclass=Singleton):
    """Helper class to interact with a Databricks workspace.
    
    The class requires that at least a databricks configuration profile is set
    which is assumed to be located under `~/.databrickscfg`.
    
    This class can be extended to use `DBFS`,
    `secrets`, `jobs` and `libraries` APIs.

    Raises:
        FileNotFoundError: If `~/.databrickscfg` config file is not found

    """

    def __init__(self):
        databricks_config_file = f'{os.path.expanduser("~")}/.databrickscfg'
        if not os.path.exists(databricks_config_file):
            raise FileNotFoundError(
                'Please set up a databricks configuration profile first.'
            )
        # Read configuration file to dynamically fetch profiles
        config = configparser.ConfigParser()
        config.read(databricks_config_file)
        self.workspacesClients = {
            workspace: WorkspaceClient(profile=workspace)
            for workspace in config.sections()
        }


def get_workspace_secret_value(
    secret_key: str,
    workspace: str,
    scope: str,
) -> str:
    """Returns a value of a Databricks workspace secret which scope
    mirrors an Azure KV.
    
    Note that `get_secret()` returns the bytes representation of the secret,
    which has to be decoded using `base64` package.
    
    The method uses :class:`DatabricksWorkspace` which requires
    the `.databrickscfg` file to exist under your home directory.
    
    Args:
        secret_key: Secret's key
        workspace: Workspace name, matches config file profile name
        scope: Name of Databricks secret scope

    Returns:
        Secret value, based64 decoded

    Raises:
        FileNotFoundError: If `~/.databrickscfg` config file is not found
    
    """

    return base64.b64decode(
        DatabricksWorkspace().workspacesClients[workspace].secrets.get_secret(
            key=secret_key, scope=scope
        ).value
    ).decode()
