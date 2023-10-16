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

from typing import (
    Dict,
    Optional,
)

import networkx as nx
from qctrlworkflowclient import print_warnings
from sympy import Expr

from fireopal.credentials import Credentials

from .base import fire_opal_workflow


@fire_opal_workflow("solve_qaoa_workflow", formatter=print_warnings)
def solve_qaoa(
    problem: Expr | nx.Graph,
    problem_type: str,
    credentials: Credentials,
    backend_name: Optional[str] = None,
) -> Dict:
    """
    Solve a QAOA problem.

    Parameters
    ----------
    problem : Expr or nx.Graph
        The QAOA problem definition, represented as either an
        `nx.Graph` or `sympy.Expr`.
    problem_type : str
        The class of QAOA problem to solve.
    credentials : Credentials
        The credentials for running circuits on an IBM backend.
        Use the `make_credentials_for_ibmq` function from the `credentials` module
        to generate properly formatted credentials.
    backend_name : str, optional
        The backend device that should be used to run circuits. Defaults to None.

    Returns
    -------
    Dict
        The output of the solve qaoa workflow.
    """
    print(
        "This function performs multiple circuit executions. "
        "The total execution time is expected to take a few minutes but will take "
        "much longer if waiting in the public queue. It is highly recommended to visit "
        "https://quantum-computing.ibm.com/reservations and make a dedicated reservation.\n"
    )
    print("Visit https://quantum-computing.ibm.com/jobs to check your queue position.")
    return {
        "problem": problem,
        "problem_type": problem_type,
        "credentials": credentials,
        "backend_name": backend_name,
    }
