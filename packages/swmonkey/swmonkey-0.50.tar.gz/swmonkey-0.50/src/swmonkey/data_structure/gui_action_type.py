from enum import Enum

class GUIActionType(Enum):
    CLICK = 'click'
    DOUBLE_CLICK='double_click'
    KEY_PRESS='key_press'
    WRITE='write'