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

from typing import (
    Dict,
    List,
)

from qctrlworkflowclient import print_warnings

from fireopal.credentials import Credentials

from .base import fire_opal_workflow


@fire_opal_workflow("validate_input_circuits_workflow", formatter=print_warnings)
def validate(
    circuits: List[str],
    credentials: Credentials,
    backend_name: str,
) -> Dict:
    """
    Validate the compatibility of a batch of circuits for Fire Opal.

    Parameters
    ----------
    circuits : List[str]
        A list of quantum circuit in the form QASM string. You can use Qiskit to
        generate these strings.
    credentials : Credentials
        The credentials for running circuits on an IBM backend.
        Use the `make_credentials_for_ibmq` function from the `credentials` module
        to generate properly formatted credentials.
    backend_name : str
        The backend device name that will be used to run circuits after validation.

    Returns
    -------
    Dict
        The output of the validate workflow.
    """
    return {
        "circuits": circuits,
        "credentials": credentials,
        "backend_name": backend_name,
    }
