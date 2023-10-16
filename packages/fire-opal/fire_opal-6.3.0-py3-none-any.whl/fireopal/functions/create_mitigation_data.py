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

from typing import Dict

from .base import fire_opal_workflow


@fire_opal_workflow("ibm_mitigation_workflow")
def create_mitigation_data(
    ibm_device_name: str,
    ibmq_token: str,
    hub: str,
    group: str,
    project: str,
) -> Dict:
    """
    Creates mitigation data for Fire Opal.

    Parameters
    ----------
    ibm_device_name : str
        The device to run mitigation on.
    ibmq_token : str
        The IBM token for authentication.
    hub : str
        The IBM hub for authentication.
    group : str
        The IBM group for authentication.
    project : str
        The IBM project for authentication.

    Returns
    -------
    Dict
        Dictionary with workflow output.
    """

    return {
        "ibm_device_name": ibm_device_name,
        "ibmq_token": ibmq_token,
        "hub": hub,
        "group": group,
        "project": project,
    }
