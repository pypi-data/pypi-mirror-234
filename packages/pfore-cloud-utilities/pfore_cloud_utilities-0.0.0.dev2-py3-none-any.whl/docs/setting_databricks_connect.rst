Setting up databricks-connect
=============================

To run code remotely on a databricks cluster, we'll use databricks-connect_
package. Note that development on clusters of versions `13.0` is not yet
supported due to the unavailability of `Unity Catalog`_ within the schwarz
universe. This guide will cover clusters of versions `12.*`.

The first step would be to create a :file:`databricks-connect` file under your
home directory. The file will have the following structure:

.. code-block:: cfg

    {
      "host": "<link-to-databricks-workspace",
      "token": "<your-personal-access-token",
      "cluster_id": "<id-to-your-cluster>",
      "org_id": "<org-id>",
      "port": "<cluster-port, default is 15001>"
    }

Both `cluster_id` and `org_id` can be fetched from the cluster url. When you
click on a cluster from the databricks UI, the url will look like:
:file:`https://<host>/?o=637714045082932#setting/clusters/0926-150153-dz1yndfb/`
where the string after **?o=** is the **org_id** and the string
after **/clusters/** is the **cluster_id**.

Once the file is set up, you'll have to create a virtual env with a python
version that matches your cluster python version (which is **3.9.5** in the
case of `12.*` clusters) and install a `databricks-connect` package that
major's matches the cluster version so `12.*.*`.

.. code-block:: bash

    # Assuming pyenv and pyenv virtualenv is installed
    pyenv install 3.9.5
    pyenv virtualenv 3.9.5 databricks12

    # Symlink pyenv env to a desired repo for easier access
    ln -s ${HOME}/.pyenv/versions/databricks12 <path-to-your-desired-dir>

    # Activate virutal env
    source <path-to-your-desired-dir>/databricks12/bin/activate

    # Install databricks-connect
    pip install "databricks-connect>=12.0,<13.0"

    # Now install the pfore-cloud-utilities package
    pip install pfore-cloud-utilities

Once you're all set up you can start writing code from your favourite IDE and
running spark statements directly on the cluster. If the cluster specified in
the config file is down, it will first start it.

Before you run a script, make sure to add the env variable
**PYSPARK_PYTHON=python3**. This can be done in Pycharm for instance by
accessing `Run` menu in the toolbar, `Edit Configurations` and add it in
the `Environmental variables` section.

Example of executing a spark sql query, and saving results in blob storage as
parquet file is listed below.

.. code-block:: python

    from io import BytesIO

    from pyspark.sql.session import SparkSession

    from pfore_cloud_utilities import AzureBlobConnector
    from pfore_cloud_utilities import get_workspace_secret_value

    # Init contexts
    spark = SparkSession.builder.getOrCreate()

    # Init Blob Storage connection
    azure_blob_connector = AzureBlobConnector(
        spn_client_id=get_workspace_secret_value(
            secret_key='AzureProjectServicePrincipalClientId',
            workspace='dev',
        ),
        spn_client_secret=get_workspace_secret_value(
            secret_key='AzureProjectServicePrincipalSecret',
            workspace='dev',
        ),
        azure_tenant_id='<AAD-tenant-ID>', # Your organisation AAD tenant ID
        account_url='<storage_account_url>', # URL to your storage account
    )

    # Run SQL statement on cluster and save results as a pandas.DataFrame
    data = spark.sql('''
        SELECT * from my_table
    ''').toPandas()
    # Specify path in the blob storage
    path = '<path-in-the-blob-storage-container>/mydata.parquet'
    # Declare a BytesIO object acting as an intermediate to save the bytes
    # content of the parquet object
    bytes_parquet_df = BytesIO()
    data.to_parquet(bytes_parquet_df)
    # Upload the parquet object to blob storage
    azure_blob_connector.upload(
        container_name='<my-blob-container-name>',
        contents=bytes_parquet_df.getvalue(),
        path=path,
    )


It is important to know that only the spark code
is executed on the cluster, the rest is executed locally, therefore classical
notebook operations like accessing filesystem using `/dbfs`
or mounted files using `/mnt` will fail.
Use the :class:`AzureBlobConnector` class to communicate
with blob storage instead of mounts as mounts are deprecated with the birth of
`Unity Catalog`_.
Furthermore instantiate `dbutils` instance to interact with the cluster
using dbutils as you're used to do in the notebook. This can be done with
the following few lines of code:

.. code-block:: python

    from pyspark.dbutils import DBUtils
    from pyspark.sql.session import SparkSession

    spark = SparkSession.builder.getOrCreate()
    dbutils = DBUtils().get_dbutils(spark)
    # Execute dbutils method as usual with dbutils.<method>()

.. _databricks-connect: https://learn.microsoft.com/en-us/azure/databricks/dev-tools/databricks-connect-legacy
.. _Unity Catalog: https://www.databricks.com/product/unity-catalog