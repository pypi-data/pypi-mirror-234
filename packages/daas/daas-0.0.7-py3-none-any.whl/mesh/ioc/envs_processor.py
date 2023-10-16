#
# Copyright (c) 2000, 2099, ducesoft and/or its affiliates. All rights reserved.
# DUCESOFT PROPRIETARY/CONFIDENTIAL. Use is subject to license terms.
#
#
from abc import abstractmethod
from typing import Any

from mesh.ioc import Context


class EnvsProcessor:

    @abstractmethod
    def post_properties(self, context: Context) -> Any:
        pass
