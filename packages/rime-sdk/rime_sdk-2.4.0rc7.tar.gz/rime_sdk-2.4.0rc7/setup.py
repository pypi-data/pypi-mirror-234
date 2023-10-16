"""Setup file for package."""
import re
from pathlib import Path
from subprocess import CalledProcessError, run

from setuptools import find_packages, setup

CUR_DIR = Path(__file__).parent

# We want the semantic version to come in the form
# of `git describe`.  In edge cases we might run this command in
# a git repo with a shallow history which will cause an error.
# In that situation we fall back to the string in the fw_version.txt
# file which is updated every time we cut a release.
#
# Our naming scheme is at odds with PEP 440, so we have to
# make it conforming but using "+" to join the public
# identify (fw_version.txt) with our local identifier, which
# is the string that git describe appends.
with open("../../version.txt", encoding="utf-8") as f:
    version_txt = f.read().strip()
try:
    rawver = run(
        ["git", "describe", "HEAD", "--match", "[0-9]*.[0-9]*.[0-9]*"],
        check=True,
        encoding="utf-8",
        capture_output=True,
    ).stdout.strip()
    localver = re.split(version_txt, rawver)[-1]
    # locaver is not empty and starts with "-" on devlopment releases
    if localver:
        localver = "+" + localver[1:]
    semver = version_txt + localver
except (CalledProcessError, AttributeError):
    semver = version_txt

with open(CUR_DIR / "README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="rime_sdk",
    version=semver,
    packages=find_packages(include=["rime_sdk*"]),
    description="Package to programmatically access a RIME deployment",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # TODO(VAL-2432): upgrade to semver 3 when it is released.
    setuptools_git_versioning={"enabled": True},
    setup_requires=["setuptools-git-versioning==1.7.4"],
    install_requires=[
        # Note: click is a dependency of `requests` but has to be pinned here
        # due to https://github.com/psf/black/issues/2964 .
        "click>=8.0.1,<8.1.4",
        "deprecated>=1.0.0,<2.0.0",
        "semver>=2.10.0,<3.0.0",
        "simplejson",
        "pandas>=1.1.0,<1.5.0",
        "requests>=2.0.0",
        "tqdm",
        "importlib_metadata",
        "protobuf",
        # below reqs are for data_format_check
        "schema",
        "numpy",
    ],
    python_requires=">=3.6",
    license="OSI Approved :: Apache Software License",
    entry_points={
        "console_scripts": [
            "rime-data-format-check=rime_sdk.data_format_check.cli:main",
        ]
    },
)
