Installation
============

To install :mod:`pfore-cloud-utilities` run:

.. code-block:: bash

    $ # Create and activate Python virtual environment, e.g.
    $ # Assuming you have pyenv and pyenv virtualenv installed
    $ # pyenv virtualenv 3.<minor>.<patch> ${HOME}/.envs/pfore-cloud-utilities
    $ # source ${HOME}/.envs/pfore-cloud-utilities/bin/activate
    $ pip install pfore-cloud-utilities

Please note that if you're working behind a firewall or a VPN, you need to
configure pip to mirror the public PyPI_ repository so that public packages
are discoverable. To do so, edit or create if not yet created
pip configuration file under :file:`${HOME}/.pip/pip.conf`. The structure of
the configuration file is following:

.. code-block:: cfg

    [global]
    timeout = 60
    index-url = https://<username>:<api-key>@<domain>/<tool>/api/pypi/<private-repository-name>/simple
    extra-index-url = https://<username>:<api-key><domain>/<tool>/api/pypi/pypi/simple

For Artifactory users, `<tool>` will be `artifactory` and `<username>` is your
artifactory username, `<api-key>` is your artifactory API key and `<domain>`
is your organisation domain name on Artifactory.

Note that the repository that mirrors public PyPI_ needs to be first
configured on Artifactory. Your organisation should have already this set up
and you'd only need to configure `pip` locally.


.. _PyPI: https://pypi.org/project/pfore-cloud-utilities
