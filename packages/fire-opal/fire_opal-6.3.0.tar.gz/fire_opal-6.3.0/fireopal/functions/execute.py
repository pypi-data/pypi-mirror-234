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

from __future__ import annotations

from qctrlcommons.preconditions import check_argument
from qctrlworkflowclient import print_warnings

from fireopal.config import get_config
from fireopal.credentials import Credentials

from .base import fire_opal_workflow


@fire_opal_workflow("compile_and_run_workflow", formatter=print_warnings)
def execute(
    circuits: str | list[str],
    shot_count: int,
    credentials: Credentials,
    backend_name: str,
) -> dict:
    """
    Execute a batch of `circuits` where `shot_count` measurements are taken per circuit.

    Parameters
    ----------
    circuits : str or list[str]
        Quantum circuit(s) in the form of a QASM strings. You may use Qiskit to
        generate these strings.
    shot_count : int
        Number of bitstrings that are sampled from the final quantum state.
    credentials : Credentials
        The credentials for running circuits. See the `credentials` module for functions
        to generate credentials for your desired provider.
    backend_name : str
        The backend device name that should be used to run circuits.

    Returns
    -------
    dict
        A dictionary containing probability mass functions and warnings.
    """
    _check_execute_types(
        circuits=circuits,
        shot_count=shot_count,
        credentials=credentials,
        backend_name=backend_name,
    )
    circuits = _handle_single_circuit(circuits)

    settings = get_config()
    credentials_with_org = credentials.copy()
    credentials_with_org.update({"organization": settings.organization})
    return {
        "circuits": circuits,
        "shot_count": shot_count,
        "credentials": credentials_with_org,
        "backend_name": backend_name,
    }


def _handle_single_circuit(strings: str | list[str]) -> list[str]:
    """
    Convert a single string to a list holding containing it, if applicable.

    Parameters
    ----------
    strings : str or list[str]
        One or more strings.

    Returns
    -------
    list[str]
        The input if originally provided as a list. Otherwise, the input string in
        a list.
    """
    if isinstance(strings, str):
        return [strings]
    return strings


def _check_execute_types(
    circuits: str | list[str],
    shot_count: int,
    credentials: Credentials,
    backend_name: str,
) -> None:
    """
    Check if the types are correct for execute function.

    Parameters
    ----------
    circuits : str or list[str]
        Quantum circuit(s) in the form of a QASM strings. You may use Qiskit to
        generate these strings.
    shot_count : int
        Number of bitstrings that are sampled from the final quantum state.
    credentials : Credentials
        The credentials for running circuits. See the `credentials` module for functions
        to generate credentials for your desired provider.
    backend_name : str
        The backend device name that should be used to run circuits.
    """

    if isinstance(circuits, list):
        check_argument(
            all(isinstance(circuit, str) for circuit in circuits),
            "Invalid type received for circuits input. All circuits must be strings.",
            {"circuits": circuits},
        )
    else:
        check_argument(
            isinstance(circuits, str),
            "Invalid type received for circuits input. The circuit must be a string.",
            {"circuits": circuits},
        )
    check_argument(
        isinstance(shot_count, int),
        "Invalid type received for shot_count input. The shot_count must be an integer.",
        {"shot_count": shot_count},
    )
    check_argument(
        isinstance(credentials, dict),
        "Invalid type received for credentials input. The credentials must be a dictionary.",
        {
            "credentials": credentials,
            "credentials type": type(credentials),
        },
    )
    check_argument(
        isinstance(backend_name, str),
        "Invalid type received for backend_name input. The backend_name must be a string.",
        {"backend_name": backend_name},
    )
