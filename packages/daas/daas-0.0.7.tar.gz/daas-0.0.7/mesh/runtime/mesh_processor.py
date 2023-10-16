#
# Copyright (c) 2000, 2099, ducesoft and/or its affiliates. All rights reserved.
# DUCESOFT PROPRIETARY/CONFIDENTIAL. Use is subject to license terms.
#
#
from typing import Any

from mesh.ioc.paas_processor import PaaSProcessor


class MeshPostProcessor(PaaSProcessor):

    def before_initialization(self, cls: type, name: str) -> Any:
        pass

    def after_initialization(self, instance, name: str) -> Any:
        pass

    def before_instantiation(self, instance, name: str) -> Any:
        pass

    def after_instantiation(self, instance, name: str) -> Any:
        pass