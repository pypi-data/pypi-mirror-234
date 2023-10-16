#
# Copyright (c) 2000, 2099, ducesoft and/or its affiliates. All rights reserved.
# DUCESOFT PROPRIETARY/CONFIDENTIAL. Use is subject to license terms.
#
#
from abc import abstractmethod, ABC

from mesh.macro import spi


@spi("mesh")
class RuntimeHook(ABC):

    @abstractmethod
    def start(self):
        """
         Trigger when mesh runtime is start.
        :return:
        """
        pass

    @abstractmethod
    def stop(self):
        """
        Trigger when mesh runtime is stop.
        :return:
        """
        pass

    @abstractmethod
    def refresh(self):
        """
        Trigger then mesh runtime context is refresh or metadata is refresh.
        :return:
        """
        pass
