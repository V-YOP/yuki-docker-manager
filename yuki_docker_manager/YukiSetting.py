

import copy
from dataclasses import dataclass, field, asdict
import json
import sys
from textwrap import dedent
from typing import Any, Dict, List, Optional, Tuple, Type

from .elements import BaseElement

from .helper import singleton
from .helper.QtAll import *
from .helper.util import *
from krita import *
from .constants import *
from .elements import element_classes


@dataclass
class YukiPartSettingDto:
    """
    settings for one direction 
    """
    display: bool = False
    display_in_canvas_mode: bool = False

    # key is item's className, value is instance of corresponding setting class
    element_local_settings: List[Tuple[str, Dict]] = field(default_factory=list)

@singleton
class YukiSetting:
    @staticmethod
    def __read_setting_dto(pos: Pos, mock: Optional[YukiPartSettingDto] = None) -> Optional[YukiPartSettingDto]:
        if mock:
            return mock
        """notify users if there's a fatal"""
        setting_str = Krita.instance().readSetting(CONFIG_GROUP, pos, '{}')
        try:
            return YukiPartSettingDto(**json.loads(setting_str))
        except RuntimeError as e:
            # json deserialize failed, it's fatal and cannot be fixed, we must restore to default and notify users 

            display_msg_box(dedent(f"""\
                Yuki Dokker Manager settings {pos} parse failed, restore to default settings.
                callback: {sys.exc_info()}
                {e}
            """.rstrip()), QMessageBox.Critical)

            Krita.instance().writeSetting(CONFIG_GROUP, pos, '{}')
            return YukiPartSettingDto()
        
    @staticmethod
    def __validate_item_settings(setting_class: Any, setting_instance: dict):

        pass

    def refresh(self, mock: Optional[YukiPartSettingDto] = None):
        element_class_to_setting_class = {i: i.my_config_dataclass for i in element_classes()}
        element_str_to_class = {i.__name__: i for i in element_class_to_setting_class.keys()}

        for pos in ('Top', 'Bottom', 'Left', 'Right'):
            self.__dto_cache[pos] = YukiSetting.__read_setting_dto(pos, mock)
            self.__items[pos] = []

            # validate global settings
            for element_class_str, global_settings_dict in self.__dto_cache[pos].element_local_settings:
                if (element_class := element_str_to_class.get(element_class_str)) is None:
                    display_msg_box(dedent(f"""\
                        Element class ''
                    """.rstrip()), QMessageBox.Critical)
                pass
            
            

    """
    A reactive wrapper for settings
    """
    def __init__(self) -> None:
        # load from krita settings, use a single 
        # self.setting_dto = copy.deepcopy(dto)
        self.__dto_cache: Dict[Pos, YukiPartSettingDto] = {}
        self.__items: Dict[Pos, List[Tuple[Type[BaseElement], Any]]] = {}

        self.refresh()



    # class YukiPartSetting: