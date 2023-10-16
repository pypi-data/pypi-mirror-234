#
# Copyright (c) 2000, 2099, ducesoft and/or its affiliates. All rights reserved.
# DUCESOFT PROPRIETARY/CONFIDENTIAL. Use is subject to license terms.
#
#
from mesh.macro import index, serializable


@serializable
class Institution:

    @index(0)
    def node_id(self) -> str:
        return ''

    @index(5)
    def inst_id(self) -> str:
        return ''

    @index(10)
    def inst_name(self) -> str:
        return ''
