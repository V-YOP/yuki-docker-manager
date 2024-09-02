from dataclasses import dataclass
from typing import Optional
from .BaseElement import BaseElement
from ..helper.QtAll import *

@dataclass
class MyTextSetting:
    text: str
    pass

class TextElement(BaseElement[MyTextSetting]):
    my_config_dataclass = MyTextSetting

    @classmethod
    def create_me(cls, is_vertical: bool, my_setting: MyTextSetting) -> QWidget | QLayoutItem:
        return QLabel(my_setting.text)
    

