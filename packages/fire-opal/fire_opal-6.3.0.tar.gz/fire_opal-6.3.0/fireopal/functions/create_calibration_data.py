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

from .base import fire_opal_workflow


@fire_opal_workflow("calibration_workflow")
def create_calibration_data(
    ibm_device_name: str,
    gate_type: str,
    echo: bool,
    ibmq_token: str,
    hub: str,
    group: str,
    project: str,
    gates_to_calibrate: List[str],
    optimizer_iterations: int = 10,
    candidate_count: int = 4,
    cost_temperature: float = 0.5,
    temperature_scaling: float = 0.5,
    use_latest_gates: bool = False,
) -> Dict:
    """
    Creates calibration data for Fire Opal.

    Parameters
    ----------
    ibm_device_name : str
        Description
    gate_type : str
        Description
    echo : bool
        Description
    ibmq_token : str
        Description
    hub : str
        Description
    group : str
        Description
    project : str
        Description
    gates_to_calibrate : List[str]
        Description
    optimizer_iterations : int, optional
        Defaults to 10.
    candidate_count : int, optional
        Defaults to 4.
    cost_temperature : float, optional
        Defaults to 0.5.
    temperature_scaling : float, optional
        Defaults to 0.5.
    use_latest_gates : bool, optional
        Defaults to False.

    Returns
    -------
    Dict
        The output of the calibration workflow.
    """

    return {
        "ibm_device_name": ibm_device_name,
        "gate_type": gate_type,
        "echo": echo,
        "ibmq_token": ibmq_token,
        "hub": hub,
        "group": group,
        "project": project,
        "gates_to_calibrate": gates_to_calibrate,
        "optimizer_iterations": optimizer_iterations,
        "candidate_count": candidate_count,
        "cost_temperature": cost_temperature,
        "temperature_scaling": temperature_scaling,
        "use_latest_gates": use_latest_gates,
    }
