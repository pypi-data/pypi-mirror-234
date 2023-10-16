#
# Copyright (c) 2000, 2099, ducesoft and/or its affiliates. All rights reserved.
# DUCESOFT PROPRIETARY/CONFIDENTIAL. Use is subject to license terms.
#
#
from mesh.macro import mps
from mesh.prsim import Endpoint, EndpointSticker


@mps
class MeshEndpoint(Endpoint, EndpointSticker[bytes, bytes]):

    def fuzzy(self, buff: bytes) -> bytes:
        pass

    def stick(self, varg: bytes) -> bytes:
        pass
