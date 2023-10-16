Contributing
============

Everyone is invited to contribute to this project.
Feel free to create a `pull request`_ ,
if you find errors,
omissions,
inconsistencies,
or other things
that need improvement.

.. _pull request: https://github.com/Bahaabrougui/pfore-cloud-utilities/pulls


Development Installation
------------------------

Instead of pip-installing the latest release from PyPI_,
you should get the newest development version from GitHub_::

   git clone https://github.com/Bahaabrougui/pfore-cloud-utilities
   cd pfore-cloud-utilities
   # Create virtual environment for this project
   # e.g.
   # pyenv virtualenv 3.<x>.<x>  $HOME/.envs/pfore-cloud-utilities
   # source $HOME/.envs/pfore-cloud-utilities/bin/activate
   pip install -r requirements.txt


This way,
your installation always stays up-to-date,
even if you pull new changes from the Github repository.

.. _PyPI: https://pypi.org/project/pfore-cloud-utilities
.. _GitHub: https://github.com/Bahaabrougui/pfore-cloud-utilities


Coding Convention
-----------------

We follow the PEP8_ convention for Python code
and check for correct syntax with ruff_.
In addition,
we check for common spelling errors with codespell_.
Both tools and possible exceptions
are defined in :file:`pyproject.toml`.

The checks are executed in the CI using `pre-commit`_.
You can enable those checks locally by executing::

    pip install pre-commit  # consider system wide installation
    pre-commit install
    pre-commit run --all-files

Afterwards ruff_ and codespell_ are executed
every time you create a commit.

You can also install ruff_ and codespell_
and call it directly::

    pip install ruff codespell  # consider system wide installation
    ruff check .
    codespell

It can be restricted to specific folders::

    ruff check some_folder/ tests/
    codespell some_folder/ tests/


.. _codespell: https://github.com/codespell-project/codespell/
.. _PEP8: https://peps.python.org/pep-0008/
.. _pre-commit: https://pre-commit.com
.. _ruff: https://docs.astral.sh/ruff/


Building the Documentation
--------------------------

If you make changes to the documentation,
you can re-create the HTML pages using Sphinx_.
You can install it and a few other necessary packages with::

   pip install -r docs/requirements.txt

To create the HTML pages, use::

   python -m sphinx docs/ build/sphinx/html -b html

The generated files will be available
in the directory :file:`build/sphinx/html/`.

It is also possible to automatically check if all links are still valid::

   python -m sphinx docs/ build/sphinx/html -b linkcheck

.. _Sphinx: https://www.sphinx-doc.org/en/master/


Running the Tests
-----------------

You'll need pytest_ for that.
It can be installed with::

   pip install -r tests/requirements.txt

To execute the tests, simply run::

   python -m pytest

.. _pytest: https://docs.pytest.org/en/7.4.x/


Creating a New Stable Release
-----------------------------

New releases are made using the following steps:

#. Update ``CHANGELOG.rst``
#. Commit those changes as "Release X.Y.Z"
#. Create an (annotated) tag with ``git tag -a X.Y.Z``
#. Push the commit and the tag to GitHub
