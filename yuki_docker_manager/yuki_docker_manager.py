from krita import *
from .helper import Toolbox, Logger, ToolEnum

logger = Logger()

class YukiDockerManager(Extension):

    def __init__(self, parent):
        # This is initialising the parent, always important when subclassing.
        super().__init__(parent)
        self.toolbox = Toolbox()

    def setup(self):
        #This runs only once when app is installed
        self.toolbox.currentToolChanged.connect(lambda x: logger.info(f"current tool changed: {x.cn_tooltip}"))
        pass

    def createActions(self, window):
        '''
        Example:
        action = window.createAction("uniqueIdOfAction", "Text shown in menu of the action", "tools/scripts")
        action.triggered.connect(self.methodToRunOnClick)
        '''
        pass

# And add the extension to Krita's list of extensions:
Krita.instance().addExtension(YukiDockerManager(Krita.instance())) 
