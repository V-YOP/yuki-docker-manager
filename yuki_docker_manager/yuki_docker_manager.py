from dataclasses import asdict
from krita import *
from .yuki_docker_manager_settings import YukiDockerPartSettings
from .helper.util import *
from .yuki_docker_part import YukiDockerPart
from .helper import Logger, singleton
from .helper.QtAll import *
from typing import *
from .constants import *
import json

logger = Logger()

from PyQt5.QtWidgets import QVBoxLayout, QWidget

@singleton
class YukiDockerManager(Extension):
    def __init__(self, parent):
        super().__init__(parent)
        self.__docker_parts: Dict[str, List[YukiDockerPart]] = {}
    
    def get_docker_parts(self, window: Window):
        return self.__docker_parts.get(krita_window_id(window), [])
    
    def setup(self):
        pass

    def createActions(self, window):
        action = window.createAction(CONFIG_GROUP, CONFIG_GROUP, ACTION_MENU_LOCATION)
        self.menu = QMenu(CONFIG_GROUP, window.qwindow())
        action.setMenu(self.menu)

        self.create_sketch_action = window.createAction(EXTENSION_PREFIX + '_refresh_all', "Refresh All", ACTION_MENU_LOCATION)
        self.create_sketch_action.triggered.connect(lambda: self.refresh_all)

        pass

    def get_setting(self, pos: Pos):
        setting_str = Krita.instance().readSetting(CONFIG_GROUP, pos, 'NONE')
        if setting_str == 'NONE':
            res = YukiDockerPartSettings()
            Krita.instance().writeSetting(CONFIG_GROUP, pos, json.dumps(asdict(res)))
            return res
        return YukiDockerPartSettings(**json.loads(setting_str))
        

    def set_setting(self, pos: Pos, setting: YukiDockerPartSettings):
        # validate it
        self.refresh_all()

    
    def refresh_part(self, settings: YukiDockerPartSettings, docker_part: YukiDockerPart, window: Window):
        # clear widget
        if widget := docker_part.widget():
            docker_part.setWidget(None)
            
            widget.deleteLater()  # 确保控件被删除
    

        pass

    def _notify_part_mounted(self, docker_part: YukiDockerPart, window: Window):
        """ call by YukiDockerPart to notify it's mounting """
        self.__docker_parts.setdefault(krita_window_id(window), []).append(docker_part)
        self.refresh_part(self.get_setting(docker_part.pos), docker_part, window)

    def refresh_all(self):
        # fetch and update 
        for window in Krita.instance().windows():
            for docker_part in self.get_docker_parts(window):
                self.refresh_part(self.get_setting(docker_part.pos), docker_part, window)


Krita.instance().addExtension(YukiDockerManager(Krita.instance()))