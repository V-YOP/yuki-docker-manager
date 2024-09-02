from dataclasses import dataclass
import sys
from typing import Dict
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget

from yuki_docker_manager.helper import Dict
from yuki_docker_manager.helper.QtAll import QLayoutItem
from ..helper import *
from ..helper.QtAll import *
from typing import *
from abc import ABC, abstractmethod

MySettingType = TypeVar('T')

OurSettingType = TypeVar('R')

class BaseElement(ABC, Generic[ MySettingType]):
    _item_classes = []
    def __init_subclass__(cls, **kwargs):
        BaseElement._item_classes.append(cls)

    my_config_dataclass: Optional[MySettingType] = None

    @classmethod
    @abstractmethod
    def create_me(cls, is_vertical: bool, my_setting: MySettingType) -> QWidget | QLayoutItem:
        ...
