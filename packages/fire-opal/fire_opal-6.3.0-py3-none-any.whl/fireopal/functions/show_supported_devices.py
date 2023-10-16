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

from qctrlworkflowclient import print_warnings

from fireopal.credentials import Credentials

from .base import fire_opal_workflow


@fire_opal_workflow("show_supported_devices_workflow", formatter=print_warnings)
def show_supported_devices(credentials: Credentials) -> Dict:
    """
    Shows the current supported devices for Fire Opal.

    Parameters
    ----------
    credentials : Credentials
        The hardware provider credentials. See the `credentials` module
        for functions to generate credentials for your desired provider.

    Returns
    -------
    Dict
        The output of the show supported devices workflow.
    """

    return {
        "credentials": credentials,
    }
