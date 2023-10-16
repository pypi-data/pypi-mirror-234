import subprocess
import os
import argparse
import time
from .main import run_monkey
import multiprocessing
from swmonkey.log.log import logger
import psutil


def count_process_instances(process_name):
    count = 0
    try:
        for process in psutil.process_iter():
            if process.name() == process_name:
                count += 1
        return count
    except Exception as e:
        logger.error(e)
        return False


def run_command(sudo=False, cmd=None, passwd=None):
    if sudo:
        if passwd is None:
            raise Exception('passwd is None')
        cmd = f'sudo -S {cmd}'
    subprocess.run(f'echo {passwd} | {cmd}', shell=True)


def run_monkey_test():
    duration = int(os.getenv('DURATION'))
    starttime = float(os.environ.get('START_TIME'))
    while time.time() - starttime < duration:
        logger.info(f'[Main process] start swmonkey {starttime}')
        # 检查当前是否已经有swmonkey_runner进程在运行
        if count_process_instances('swmonkey_runner') > 1:
            exit(0)
        # 使用multiprocessing的原因：
        #  1. subprocess.open在一些情况下会找不到swmonkey command/file，原因未知
        #  2. multiprocess.Process 子进程会继承父进程的环境变量，不需要再传入
        p = multiprocessing.Process(
            target=run_monkey, args=(duration,), daemon=True)
        p.start()
        p.join()
        if p.exitcode == 0:
            # 正常退出
            logger.info("[Main process]Child process exited normally")
            break
        else:
            # 异常退出
            logger.info(
                f"[Main process]Child process exited abnormally, exitcode: {p.exitcode}")
        # 设定的时间没有执行完
        # Note:
        # 在openlylin压测过程中发现桌面环境会崩溃重置，这时如果配置了autostart smwonkey,
        # 相当于重新执行了一遍swmonkey, start_time将重置，~/.swmonkey会新建日志文件夹
        if time.time() - starttime < duration:
            logger.info(
                "[Main process]Monkey test stopped unexpectedly, restarting...")
        time.sleep(5)

        restart_x11 = os.environ.get('RESTART_X11')
        password = os.environ.get('PASSWORD')
        if restart_x11 is not None and password is not None:
            logger.info("[Main process]Restarting x11...")
            # WARNING
            # 执行这个命令会导致桌面环境重启，所有的应用都会关闭,包括swmonkey_runner
            run_command(sudo=True, cmd='systemctl restart lightdm',
                        passwd=password)
    logger.info("[Main process]Monkey test finished!")


def main():
    parser = argparse.ArgumentParser(
        description='A tool for monkey test on Linux GUI')

    parser.add_argument('-d', '--duration', type=int,
                        default=0, help='Duration in seconds')

    parser.add_argument('--restart-x11', dest='restartx11', action='store_true',
                        default=None, help='开启这个参数，会在 swmonkey 挂掉的时候，自动重启 X11 服务, 前提是终端需要配置了自动运行monkey, 如何配置参见:https://kb.cvte.com/pages/viewpage.action?pageId=377734914')

    parser.add_argument('--password', dest='password', type=str,
                        default=None, help='指定sudo密码, 用于 swmonkey 进程挂掉的时候，自动重启 X11 服务,重启X11服务需要sudo权限')

    parser.add_argument('--keep-alive', dest='keep_alive', action='store_true',
                        default=None, help="自动清理系统资源以保证monkey测试")

    parser.add_argument('--interval', dest='interval', type=float,
                        default=0.5, help="GUI操作的间隔时间")

    parser.add_argument('--app-path', dest='app_path', type=str,
                        default=None, help="Monkey测试限定的应用程序路径")

    args = parser.parse_args()
    logger.info(f"Arguments: {args}")
    logger.info(f"OS Environment: {os.environ}")

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
    assert duration > 0, 'Duration must be greater than 0'
    if duration is not None:
        os.environ['DURATION'] = str(duration)

    restartx11 = args.restartx11
    if restartx11 is not None:
        os.environ['RESTART_X11'] = str(restartx11)

    password = args.password
    if password is not None:
        os.environ['PASSWORD'] = password

    # 控制进程不需要传入starttime，默认为当前时间
    starttime = time.time()
    os.environ['START_TIME'] = str(starttime)

    run_monkey_test()


if __name__ == '__main__':
    main()
