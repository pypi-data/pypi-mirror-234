# Copyright CNRS/Inria/UCA
# Contributor(s): Eric Debreuve (since 2023)
#
# eric.debreuve@cnrs.fr
#
# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

import re as rgex
from pathlib import Path as path_t
from typing import Dict

from setuptools import setup


HERE = path_t(__file__).parent.resolve()
DOCUMENTATION_HOME = HERE / "documentation" / "wiki" / "description.asciidoc"


def DescriptionFromDocumentation(documentation: path_t, /) -> Dict[str, str]:
    """"""
    output = {}

    pattern = rgex.compile(r":([A-Z_]+): +(.+)\n?", flags=rgex.ASCII)

    with open(documentation) as accessor:
        for line in accessor.readlines():
            if (match := pattern.fullmatch(line)) is not None:
                name = match.group(1)
                value = match.group(2)
                output[name] = value

    return output


DESCRIPTION = DescriptionFromDocumentation(DOCUMENTATION_HOME)


LICENSE_SHORT = "CeCILL-2.1"
LICENCE_LONG = "CEA CNRS Inria Logiciel Libre License, version 2.1"
PY_VERSION = "3.11"

DOCUMENTATION_SITE = "-/wikis/home"

PYPI_NAME = "str-to-obj"
PYPI_TOPIC = "Software Development"        # https://pypi.org/classifiers/    Topic::*  # /!\ REMOVE THE Topic:: PREFIX
PYPI_AUDIENCE = "Developers"  # https://pypi.org/classifiers/    Intended Audience::*  # /!\ REMOVE THE PREFIX
PYPI_STATUS = "4 - Beta"      # https://pypi.org/classifiers/    Development Status::*  # /!\ REMOVE THE PREFIX

IMPORT_NAME = "str_to_obj"
PACKAGES = [
    IMPORT_NAME,
    f"{IMPORT_NAME}.interface",
    f"{IMPORT_NAME}.task",
    f"{IMPORT_NAME}.type",
]
EXCLUDED_FOLDERS = (
    f"{IMPORT_NAME}.documentation",
)
ENTRY_POINTS = {}


long_description = (HERE / "README.rst").read_text(encoding="utf-8")
repository_url = (
    f"https://"
    f"{DESCRIPTION['REPOSITORY_SITE']}/"
    f"{DESCRIPTION['REPOSITORY_USER']}/"
    f"{DESCRIPTION['REPOSITORY_NAME']}/"
)
documentation_url = f"{repository_url}/{DOCUMENTATION_SITE}"


def CheckCoherenceBetweenDeclarationAndReality() -> None:
    """"""
    folders = [IMPORT_NAME]
    for node in (HERE / IMPORT_NAME).rglob("*"):
        if node.is_dir() and not str(node).startswith("."):
            node = node.relative_to(HERE)
            node = ".".join(node.parts)
            if not (
                (node in EXCLUDED_FOLDERS)
                or any(node.startswith(_fld + ".") for _fld in EXCLUDED_FOLDERS)
            ):
                folders.append(node)
    folders = sorted(folders)

    packages = sorted(PACKAGES)
    if packages != folders:
        raise ValueError(
            f"Mismatch between declared and found packages:\n"
            f"    - Declared=\n      {packages}\n"
            f"    - Found=\n      {folders}\n"
            f"    - Undeclared=\n      {set(folders).difference(packages)}\n"
            f"    - Nonexistent=\n      {set(packages).difference(folders)}"
        )


def Version():
    """"""
    contents = {}
    with open(HERE / IMPORT_NAME / "version.py") as accessor:
        exec(accessor.read(), contents)

    output = contents["__version__"]
    if isinstance(output, str) and rgex.fullmatch(r"20[0-9]{2}\.[1-9][0-9]*", output):
        return output

    raise ValueError(f"{output}: Invalid version")


if __name__ == "__main__":
    #
    CheckCoherenceBetweenDeclarationAndReality()
    # fmt: off
    setup(
        author=DESCRIPTION["AUTHOR"],
        author_email=DESCRIPTION["EMAIL"],
        #
        name=PYPI_NAME,
        description=DESCRIPTION["SHORT_DESCRIPTION"],
        long_description=long_description,
        long_description_content_type="text/x-rst",
        license=LICENSE_SHORT,
        version=Version(),
        #
        classifiers=[
            f"Topic :: {PYPI_TOPIC}",
            f"Intended Audience :: {PYPI_AUDIENCE}",
            f"License :: OSI Approved :: {LICENCE_LONG} ({LICENSE_SHORT})",
            f"Programming Language :: Python :: {PY_VERSION}",
            f"Development Status :: {PYPI_STATUS}",
        ],
        keywords=DESCRIPTION["KEYWORDS"],
        #
        url=repository_url,
        project_urls={
            "Documentation": documentation_url,
            "Source": repository_url,
        },
        #
        packages=PACKAGES,
        entry_points=ENTRY_POINTS,
        python_requires=f">={PY_VERSION}",
        install_requires=[
            "rich",
        ],
    )
