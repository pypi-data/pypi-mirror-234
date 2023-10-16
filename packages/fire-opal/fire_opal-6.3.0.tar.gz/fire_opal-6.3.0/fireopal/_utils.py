# Copyright 2023 Q-CTRL. All rights reserved.
#
# Licensed under the Q-CTRL Terms of service (the "License"). Unauthorized
# copying or use of this file, via any medium, is strictly prohibited.
# Proprietary and confidential. You may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
#    https://q-ctrl.com/terms
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS. See the
# License for the specific language.

"""
Module to host some utility functions, which are exposed at the top-level.
"""
from qctrlworkflowclient.utils import package_versions_table

__all__ = ["print_package_versions"]


def print_package_versions() -> None:
    """
    Print a Markdown-formatted table showing the Python version being used,
    as well as the versions of some loaded packages that are relevant to Fire Opal.
    """

    package_names = [
        # External packages.
        "matplotlib",
        "networkx",
        "numpy",
        "qiskit",
        "qiskit-ibm-provider",
        "sympy",
        # Q-CTRL packages.
        "fireopal",
        "qctrlvisualizer",
        "qctrlworkflowclient",
    ]

    print(package_versions_table(package_names))
