Fetching Key Vault secrets
==========================

To abstract secrets fetching from keyvault,
:class:`pfore-cloud-utilities.DatabricksWorkspace` was implemented,
you can directly use :func:`get_workspace_secret_value`
to securely retrieve secrets.

This requires having a Databricks Secret Scope mirroring an Azure Keyvault
Scope, which is implemented by default for UAPC projects, so you'll only
have to specify the scope's name when retrieving the secret. To list the
existing scopes within a workspace,
use `databricks secrets list-scopes`, output will look like

.. code-block:: bash

    databricks secrets list-scopes --profile=<profile>

        Scope                     Backend         KeyVault URL
    ------------------------  --------------  --------------------------------------------
    uapc-prj-kv-secret-scope  AZURE_KEYVAULT  https://uapc-e-prj-pfore-kv.vault.azure.net/

This also requires setting up a connection to a Databricks workspace, this
can be done by simply creating :file:`.databrickscfg` file under your home
directory, which contains information on your workspace.
Example of how the file is structured for three workspaces, dev, qas and prod
is shown below.

.. code-block:: cfg

    [dev]
    host = <databricks-host-url, starts with https://>
    token = <your databricks personal access token>

    [qas]
    host = <databricks-host-url, starts with https://>
    token = <your databricks personal access token>

    [prod]
    host = <databricks-host-url, starts with https://>
    token = <your databricks personal access token>

Once the configuration file is set up, you can call the helper class method
to fetch the secrets present in your keyvault. Example is shown in the
code below.

.. code-block:: python

    from pfore_cloud_utilities import get_workspace_secret_value

    azure_spn_client_id = get_workspace_secret_value(
            secret_key='AzureProjectServicePrincipalClientId',
            workspace='dev',
            scope='uapc-prj-kv-secret-scope',
        )
