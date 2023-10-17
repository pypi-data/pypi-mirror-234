#!/usr/bin/env python
from typing import List, Tuple, Dict
from abc import ABC, abstractmethod

from codefast import logger as cf
from codefast.exception import get_exception_str


class BeeMaxin(ABC):
    """ Base class for pipeline
    """

    def __init__(self) -> None:
        super().__init__()
        self.print_log = False
        self.use_previous=False # user previous output as arg or not

    @abstractmethod
    def process(self, *args, **kwargs):
        pass

    def exec(self, *args, **kwargs):
        class_name = self.__class__.__name__
        file_name = self.__class__.__module__.split('.')[-1]
        if self.print_log:
            cf.info({
                'step': 'pipeline starts exec',
                'class': file_name + "." + class_name,
            })
        if self.use_previous:
            honey = self.process(*args, **kwargs)
        else:
            honey = self.process()
        if self.print_log:
            cf.info({
                'step': 'pipeline finish exec',
                'class': file_name + "." + class_name,
            })
        return honey


class Pipeline(object):
    def __init__(self, bee_swarm: List[Tuple[str, BeeMaxin]] = None):
        self.bee_swarm = bee_swarm if bee_swarm else []
        self.source_input = None

    def add(self, bee: Tuple[str, BeeMaxin]):
        self.bee_swarm.append(bee)
        return self

    def set_source_input(self, source_input):
        self.source_input = source_input
        return self

    def gather(self, args=None, forever=False):
        while True:
            honey = self.source_input or args
            try:
                for _, c in self.bee_swarm:
                    if honey is not None:
                        honey = c.exec(honey)
                    else:
                        honey = c.exec()
            except Exception as e:
                cf.error(get_exception_str(e))
            if not forever:
                return honey

    def process(self, args=None):
        return self.gather(args)
