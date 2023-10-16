import os

from setuptools import setup

# If build workflow is triggered from ADO or it's a pre-release,
# ARTIFACT_LABEL exists
try:
    setup(
        version=os.environ['ARTIFACT_LABEL']
    )
# If build is triggered for gitHub and it's not a pre-release,
# use setuptools_scm to fetch tag as version
except KeyError:
    setup(
        use_scm_version=True
    )
