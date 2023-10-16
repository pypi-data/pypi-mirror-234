__version__ = '0.50'

from threading import Thread
import argparse
from swmonkey.heartbeat import send_heartbeat, finish_heartbeat
import os
from swmonkey.log.log import logger
import signal

DURATION = 10  # Duration in seconds
TIME_DIFF_SCALE = 0.1


def get_signal_name(sig_number):
    signal_number_to_name = {getattr(signal, n): n for n in dir(
        signal) if n.startswith('SIG') and '_' not in n}
    return signal_number_to_name.get(sig_number, 'UNKNOWN')


def signal_handler_to_exit(signum, frame):
    sig_name = get_signal_name(signum)
    logger.info(f'收到信号: {sig_name}({signum}), 退出程序')
    os._exit(1)


def register_signal():
    '''
    注册信号处理函数
    '''
    signal.signal(signal.SIGINT, signal_handler_to_exit)
    signal.signal(signal.SIGTERM, signal_handler_to_exit)
    signal.signal(signal.SIGHUP, signal_handler_to_exit)
    signal.signal(signal.SIGQUIT, signal_handler_to_exit)


def run_monkey(duration):
    assert duration > 0
    register_signal()
    # set environment variable DISPLAY
    os.environ['DISPLAY'] = ':0'
    from swmonkey.monkey_test.monkey_test import MonkeyTest
    monkey_test = MonkeyTest(duration=duration)
    monkey_test.run()


def run_replay(actions_path):
    assert actions_path is not None
    # set environment variable DISPLAY
    os.environ['DISPLAY'] = ':0'
    from swmonkey.controller.replay import ReplayController
    replay_controller = ReplayController()
    replay_controller.run(actions_json_file_path=actions_path)


def swmonkey():
    '''
    执行monkey测试
    '''
    register_signal()
    parser = argparse.ArgumentParser(
        description='A tool for monkey test on Linux GUI')
    parser.add_argument('-d', '--duration', type=int,
                        default=DURATION, help='Duration in seconds')

    parser.add_argument('-r', '--replay', dest='replay', action='store_true',
                        default=None, help='Replay a previous monkey test')

    parser.add_argument('-p', '--path', type=str,
                        default=None, help='Path to the monkey test')

    parser.add_argument('--heartbeat', dest='heartbeat',
                        type=str, default=None, help='Heartbeat server address')

    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s ' + __version__)

    parser.add_argument('--start-time', dest='start_time', type=float,
                        default=None, help="Start time of the monkey test")

    parser.add_argument('--keep-alive', dest='keep_alive', action='store_true',
                        default=None, help="自动清理系统资源以保证monkey测试")

    parser.add_argument('--interval', dest='interval', type=float,
                        default=0.5, help="GUI操作的间隔时间")

    parser.add_argument('--app-path', dest='app_path', type=str,
                        default=None, help="Monkey测试限定的应用程序路径")

    args = parser.parse_args()
    logger.info(f"Arguments:{args}")
    logger.info(f"OS Environment:{os.environ}")

    app_path = args.app_path
    if app_path is not None:
        os.environ['APP_PATH'] = app_path

    interval = args.interval
    if interval is not None:
        os.environ['INTERVAL'] = str(interval)

    keep_alive = args.keep_alive
    if keep_alive is not None:
        os.environ['KEEP_ALIVE'] = str(keep_alive)

    duration = args.duration
    if duration is not None:
        os.environ['DURATION'] = str(duration)
    heartbeat = args.heartbeat
    if heartbeat is not None:
        os.environ['HEARTBEAT_URL'] = heartbeat
    replay = args.replay
    if replay is not None:
        os.environ['REPLAY'] = str(replay)

    path = args.path
    if path is not None:
        os.environ['LOG_PATH'] = path

    starttime = args.start_time
    if starttime is not None:
        os.environ['START_TIME'] = str(starttime)
    else:
        import time
        os.environ['START_TIME'] = str(time.time())
    if os.getenv('HEARTBEAT_URL') is not None:
        logger.info("HEARTBEAT_URL: ", os.getenv('HEARTBEAT_URL'))
        heartbeat_thread = Thread(target=send_heartbeat, daemon=True)
        heartbeat_thread.start()
    if os.getenv('REPLAY') is not None:
        run_replay(actions_path=os.getenv('LOG_PATH'))
    else:
        duration = int(os.getenv('DURATION'))
        run_monkey(duration=duration)
    if os.getenv('HEARTBEAT_URL') is not None:
        finish_heartbeat()


def version():
    return __version__


if __name__ == '__main__':
    # swmonkey()
    v =version()
    print(f"version {v}")
