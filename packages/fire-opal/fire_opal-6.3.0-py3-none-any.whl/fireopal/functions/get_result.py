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

from typing import Any

from qctrlcommons.preconditions import check_argument
from qctrlworkflowclient import print_warnings
from qctrlworkflowclient.router.api import (
    Action,
    ApiRouter,
)

from fireopal.config import get_config


def get_result(action_id: int | str) -> dict[str, Any]:
    """
    Retrieve the result of a previously submitted action, blocking
    for completion if the action is still in progress.

    Parameters
    ----------
    action_id : int or str
        The unique identifier associated with the action.
        You can retrieve this value from the activity monitor.

    Returns
    -------
    dict[str, Any]
        The action result. The shape of this dictionary
        will be the same as that of the result returned
        from the function that was previously called
        to create this action.
    """
    check_argument(
        str(action_id).isnumeric(),
        "The action ID must be an integer.",
        {"action_id": action_id},
    )
    router: ApiRouter = get_config().get_router()

    action = Action(action_id=str(action_id))
    result = router.get_result(action)
    result = print_warnings(result)
    return result
