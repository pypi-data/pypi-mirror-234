from swmonkey.data_structure.gui_action import GUIAction

actions = []
filename = 'actions.json'


def record(gui_action):
    actions.append(gui_action)

def replay(actions):
    for action in actions:
        action.execute()


def save_actions(actions, filename=filename):
    serialized_actions = []
