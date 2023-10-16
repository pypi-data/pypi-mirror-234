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

from qctrlcommons.exceptions import QctrlArgumentsValueError

Credentials = Dict[str, str]


def make_credentials_for_ibmq(
    token: str,
    group: str,
    hub: str,
    project: str,
) -> Credentials:
    """
    Make a Credentials dictionary for IBM Quantum.

    Parameters
    ----------
    token : str
        The IBM Quantum account token.
    group : str
        The IBM Quantum group.
    hub : str
        The IBM Quantum hub.
    project : str
        The IBM Quantum project.

    Returns
    -------
    Credentials
        A dictionary usable for the `credentials`
        argument of any Fire Opal web API function.

    Notes
    -----
    This function performs only basic type checking of
    the credentials it receives. It does not check whether
    the credentials are valid for hardware access.
    """
    _check_all_strings(token=token, group=group, hub=hub, project=project)
    return {
        "token": token,
        "group": group,
        "hub": hub,
        "project": project,
        "provider": "ibmq",
    }


def _make_credentials_for_ibm_cloud(
    token: str,
    instance: str,
) -> None:
    """
    Placeholder for a `Credentials` builder for IBM cloud.

    Parameters
    ----------
    token : str
        The IBM Quantum account token.
    instance : str,
        The IBM cloud instance.

    Raises
    ------
    NotImplementedError
        To indicate IBM cloud support is not in place yet.
    """
    _check_all_strings(token=token, instance=instance)
    raise NotImplementedError("Support for IBM cloud is coming soon!")


def make_credentials_for_braket(arn: str) -> Credentials:
    """
    Make a Credentials dictionary for Braket.

    Parameters
    ----------
    arn : str
        The Amazon resource number for an IAM role
        that has Braket permissions and trusts Q-CTRL's
        AWS account.

    Returns
    -------
    Credentials
        A dictionary usable for the `credentials`
        argument of any Fire Opal web API function.

    Notes
    -----
    This function performs only basic type checking of
    the credentials it receives. It does not check whether
    the credentials are valid for hardware access.
    """
    _check_all_strings(arn=arn)
    return {
        "arn": arn,
        "provider": "braket",
    }


def _check_all_strings(**kwargs: str) -> None:
    """
    Check whether all arguments are strings.

    Raises
    ------
    QctrlArgumentsValueError
        If there are non-string arguments.
    """
    if not all((isinstance(arg, str) for arg in kwargs.values())):
        raise QctrlArgumentsValueError(
            description="All arguments should be strings.",
            arguments={f"{key} type": type(value) for key, value in kwargs.items()},
        )
