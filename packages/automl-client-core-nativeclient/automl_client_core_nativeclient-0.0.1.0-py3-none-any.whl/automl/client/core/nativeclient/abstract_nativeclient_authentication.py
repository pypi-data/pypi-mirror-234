# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from typing import Dict
from abc import ABC, abstractmethod


class AbstractNativeClientAuthentication(ABC):

    @abstractmethod
    def get_authentication_header(self) -> Dict[str, str]:
        raise NotImplementedError
