# encoding: utf-8
"""
@project: Animated-All-Star->observer
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 监听者模式抽象类继承
@created_time: 2022/11/15 8:20
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List


class Observer(ABC):
    @abstractmethod
    def update(self, subject: Subject) -> None:
        pass


class Subject(ABC):
    _observers: List[Observer] = []

    @abstractmethod
    def attach(self, observer: Observer) -> None:
        pass

    @abstractmethod
    def detach(self, observer: Observer) -> None:
        pass

    @abstractmethod
    def notify(self, subject=None) -> None:
        pass
