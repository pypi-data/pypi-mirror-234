Overview
========

:mod:`pfore-cloud-utilities` is a general functionality library to ease and
abstract some of the frequently used method when developing locally
while interacting with cloud environments, this include Databricks_ and Azure_.

Most of the method requires authentication, refer to the
:doc:`authentication` section for details on how to set it up.

Assuming that you'll also want to use the package functions while running
spark code remotely on databricks, refer to the
:doc:`setting_databricks_connect` page to see how
to set up databricks-connect_ and for coding examples.

.. _Databricks: https://www.databricks.com
.. _Azure: https://azure.microsoft.com/en-us
.. _databricks-connect: https://learn.microsoft.com/en-us/azure/databricks/dev-tools/databricks-connect-legacy