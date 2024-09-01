from typing import Literal


CONFIG_GROUP = 'Yuki Docker Manager'
EXTENSION_PREFIX = 'yuki_docker_manager_'
ACTION_MENU_LOCATION = f'tools/{CONFIG_GROUP}'
MANAGED_DOCKER_PART_OBJECT_NAME_PREFIX = 'Yuki Managed Part '

Pos = Literal['Top'] | Literal['Bottom'] | Literal['Left'] | Literal['Right']