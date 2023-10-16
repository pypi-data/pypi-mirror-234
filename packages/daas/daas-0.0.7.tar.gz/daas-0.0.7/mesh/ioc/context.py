#
# Copyright (c) 2000, 2099, ducesoft and/or its affiliates. All rights reserved.
# DUCESOFT PROPRIETARY/CONFIDENTIAL. Use is subject to license terms.
#
#
from abc import abstractmethod
from typing import Any


class Context:

    @abstractmethod
    def inject_properties(self, properties: bytes):
        pass

    @abstractmethod
    def register_processor(self, processor: Any):
        pass
