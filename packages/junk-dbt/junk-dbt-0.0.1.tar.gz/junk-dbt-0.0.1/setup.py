#!/usr/bin/env python
import sys

from setuptools import find_namespace_packages, setup

package_name = "junk-dbt"
package_version = "0.0.1"
description = "test-dbt"

requires = ["requests"]

extras = {
    "v14": [
        "dbt-core>=0.14,<0.15",
        ],
    "v15": [
        "dbt-core>=1.5,<1.6",
    ],
    "v16": [
        "dbt-core>=1.6,<1.7",
    ],
}

setup(
    name=package_name,
    version=package_version,
    install_requires=requires,
    extras_require=extras,
)
