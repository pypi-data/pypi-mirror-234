#!/usr/bin/env python
import sys

from setuptools import find_namespace_packages, setup

package_name = "junk-dbt"
package_version = "3.0.5"
description = "test-dbt"

requires = ["requests"]

extras = {
    "15": [
        "dbt-core>=1.5,<1.6",
    ],

}

setup(
    name=package_name,
    version=package_version,
    install_requires=requires,
    extras_require=extras,
)
