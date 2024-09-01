from typing import Literal
import uuid
from krita import *
from .helper import Toolbox, Logger, ToolEnum, ViewManager
from .helper.QtAll import *
from .constants import *

logger = Logger()
class YukiDockerPart(DockWidget):
    """
    Managed docker part, one per direction, fully controlled by extension YukiDockerManager, only contains minimal logics for initialation and notification
    """
    def __my_parent_window(self):
        for window in Krita.instance().windows():
            for docker in window.dockers():
                if docker is self:
                    return window
        return None # when docker is newly created
    
    def __check_me_mounted(self):
        from .yuki_docker_manager import YukiDockerManager
        if window := self.__my_parent_window():
            YukiDockerManager(None)._notify_part_mounted(self, window)
            return
        QTimer.singleShot(100, self.__check_me_mounted)

    
    def __real_init_me_and_notify(self, caller, new_object_name: str):
        self.objectNameChanged.disconnect(caller)
        self.setWindowTitle(new_object_name)
        self.__pos = new_object_name.removeprefix(MANAGED_DOCKER_PART_OBJECT_NAME_PREFIX)
        # restrict my position
        match self.__pos:
            case 'Top':
                self.setAllowedAreas(Qt.DockWidgetArea.TopDockWidgetArea)
            case 'Bottom':
                self.setAllowedAreas(Qt.DockWidgetArea.BottomDockWidgetArea)
            case 'Left':
                self.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea)
            case 'Right':
                self.setAllowedAreas(Qt.DockWidgetArea.RightDockWidgetArea)
            case _:
                raise NotImplementedError('Impossible')
            
        # disallow floating
        self.setFeatures(self.features() & ~DockWidget.DockWidgetFloatable)
        
        # loop until me mounted to a window
        self.__check_me_mounted()
        
    def __init__(self):
        # This is initialising the parent, always important when subclassing.
        super().__init__()
        self.__pos: str = None

        # setup window title and read position from objectName
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint, True)
        self.setWindowTitle(str(uuid.uuid4()))

        def on_object_name_changed(new_object_name: str):
            self.__real_init_me_and_notify(on_object_name_changed, new_object_name)
        self.objectNameChanged.connect(on_object_name_changed)

        # a placeholder
        label = QLabel("replace me!", self)
        self.setWidget(label)
        self.label = label
        
    def canvasChanged(self, canvas: Canvas):
        print('canvas changed')
        pass
    
    @property
    def pos(self) -> Pos:
        return self.__pos
    
    @property
    def is_vertical(self):
        return self.pos in ('Left', 'Right')

Krita.instance().addDockWidgetFactory(DockWidgetFactory(f"{MANAGED_DOCKER_PART_OBJECT_NAME_PREFIX}Top", DockWidgetFactoryBase.DockTop, YukiDockerPart)) # type: ignore
Krita.instance().addDockWidgetFactory(DockWidgetFactory(f"{MANAGED_DOCKER_PART_OBJECT_NAME_PREFIX}Bottom", DockWidgetFactoryBase.DockBottom, YukiDockerPart)) # type: ignore
Krita.instance().addDockWidgetFactory(DockWidgetFactory(f"{MANAGED_DOCKER_PART_OBJECT_NAME_PREFIX}Left", DockWidgetFactoryBase.DockLeft, YukiDockerPart)) # type: ignore
Krita.instance().addDockWidgetFactory(DockWidgetFactory(f"{MANAGED_DOCKER_PART_OBJECT_NAME_PREFIX}Right", DockWidgetFactoryBase.DockRight, YukiDockerPart)) # type: ignore