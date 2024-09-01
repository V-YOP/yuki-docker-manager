

from dataclasses import dataclass, field
from typing import Any, Dict, List, Tuple

@dataclass
class YukiDockerPartSettings:
    """
    settings for one direction 
    """
    display: bool = False
    display_in_canvas_mode: bool = False

    # key is item's className, value is instance of corresponding setting class
    item_global_setting: Dict[str, Dict] = field(default_factory=list)
    item_settings: List[Tuple[str, Dict]] = field(default_factory=list)
