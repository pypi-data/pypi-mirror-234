#
# Copyright (c) 2000, 2099, ducesoft and/or its affiliates. All rights reserved.
# DUCESOFT PROPRIETARY/CONFIDENTIAL. Use is subject to license terms.
#
#
from typing import Type

from mesh.codec import Codec
from mesh.macro import T, spi

Xml = "xml"


@spi(Xml)
class XmlCodec(Codec):

    def encode(self, value: T) -> bytes:
        pass

    def decode(self, value: bytes, kind: Type[T]) -> T:
        pass
