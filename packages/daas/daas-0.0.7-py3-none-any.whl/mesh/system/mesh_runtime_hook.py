#
# Copyright (c) 2000, 2099, ducesoft and/or its affiliates. All rights reserved.
# DUCESOFT PROPRIETARY/CONFIDENTIAL. Use is subject to license terms.
#
#
from mesh.macro import spi
from mesh.prsim import RuntimeHook


@spi("mesh")
class MeshRuntimeHook(RuntimeHook):

    def start(self):
        """"""
        pass

    def stop(self):
        """"""
        pass

    def refresh(self):
        """"""
        pass
