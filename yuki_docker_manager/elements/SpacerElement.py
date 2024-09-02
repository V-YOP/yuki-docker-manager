from dataclasses import dataclass
from typing import Optional
from .BaseElement import BaseElement
from ..helper.QtAll import *

@dataclass
class MySpacerSetting:
    size: Optional[int]
    pass

class SpacerElement(BaseElement[MySpacerSetting]):
    my_config_dataclass = MySpacerSetting

    @classmethod
    def create_me(cls, is_vertical: bool, my_setting: MySpacerSetting) -> QWidget | QLayoutItem:
        size = my_setting.size if my_setting.size is not None else 0
        policy = QSizePolicy.Fixed if my_setting.size is not None else QSizePolicy.Expanding

        if is_vertical:
            return QSpacerItem(0, size, QSizePolicy.Minimum, policy)
        return QSpacerItem(size, 0, policy, QSizePolicy.Minimum)
    
    