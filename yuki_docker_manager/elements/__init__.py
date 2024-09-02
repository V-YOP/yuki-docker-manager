from typing import List, Type
from .BaseElement import BaseElement
from .TextElement import *
from .SpacerElement import *

def element_classes() -> List[Type[BaseElement]]:
    return BaseElement._item_classes