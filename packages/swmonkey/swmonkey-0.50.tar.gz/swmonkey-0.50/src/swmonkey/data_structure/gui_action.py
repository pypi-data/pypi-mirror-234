import json
import pyautogui
from .gui_action_type import GUIActionType


class GUIAction:
    '''
    A class that represents a GUI action
    '''

    def __init__(self, action_type, timestamp, x=0, y=0, key='', button='', text='') -> None:
        # Type of action e.g., 'click', 'key_press', 'write', etc.
        self.action_type = action_type
        # Timestamp of when the action was performed
        self.timestamp = timestamp

        # Mouse coordinates
        self.x = x
        self.y = y
        # Key/button pressed (if applicable)
        self.key = key
        self.button = button
        # Text written (if applicable)
        self.text = text

    @staticmethod
    def to_json(gui_action):
        '''
        Serialize the action to JSON format
        '''
        serialized_actions = [gui_action.__dict__]
        return json.dumps(serialized_actions)

    @staticmethod
    def from_json(json_data):
        '''
        Deserialize the action from JSON format
        '''
        deserialized_actions = json.loads(json_data)
        return GUIAction(**deserialized_actions[0])

    def execute(self):
        '''
        Execute the action
        '''
        if self.action_type == 'click':
            pyautogui.moveTo(self.x, self.y, duration=0.1)
            pyautogui.click(self.x, self.y, button=self.button)
        elif self.action_type == 'double_click':
            pyautogui.moveTo(self.x, self.y, duration=0.1)
            pyautogui.doubleClick(self.x, self.y, button=self.button)
        elif self.action_type == 'key_press':
            pyautogui.press(self.key)
        elif self.action_type == 'write':
            pyautogui.write(self.text)
        else:
            raise ValueError('Invalid action type')


if __name__ == '__main__':
    action = GUIAction('click', 123456, 10, 20, 'a', 'left')
    print(GUIAction.to_json(action))
    print(GUIAction.from_json(GUIAction.to_json(action)).__dict__)
