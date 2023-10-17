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

from abc import (
    ABC,
    abstractmethod,
)
from typing import (
    Any,
    Dict,
    Optional,
)


class BaseRouter(ABC):
    """
    Route a request to execute a workflow.
    """

    @abstractmethod
    def __call__(self, workflow: str, data: Optional[Dict[str, Any]] = None) -> Any:
        """
        Given a workflow name and the corresponding data (if any),
        execute the workflow and returns the raw result.

        Parameters
        ----------
        workflow : str
            Name of the workflow to be executed.
        data : Dict[str, Any], optional
            Any data required by the workflow for execution.
        """
