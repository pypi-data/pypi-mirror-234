from swmonkey.util.util import get_out_dir
import os
import time
from swmonkey.data_structure.gui_action import GUIAction
import json
from swmonkey.log.log import logger


class ReplayController:
    def __init__(self):
        pass
        # self.acions = []

    def run(self, actions_json_file_path):
        try:
            # check path
            if not os.path.exists(actions_json_file_path):
                raise Exception("File not found: {}".format(
                    actions_json_file_path))
            # get lines count
            with open(actions_json_file_path, 'r') as f:
                linecount = 0
                for line in f:
                    if line.strip():
                        linecount += 1
            with open(actions_json_file_path, 'r') as f:
                cur_line = 0
                for line in f:
                    if line.strip():
                        action_dict = json.loads(line.strip())
                        self.replay(action_dict)
                        cur_line += 1
                        print("Replay progress: {}/{}".format(cur_line, linecount))
        except Exception as e:
            print("Replay failed with error: {}".format(e))
            logger.error("Replay failed with error: {}".format(e))

    def replay(self, action_dict):
        action = GUIAction(**action_dict)
        action.execute()


if __name__ == '__main__':
    replay_controller = ReplayController()
    replay_controller.run(actions_json_file_path=os.path.join(
        get_out_dir(), 'actions.json'))
