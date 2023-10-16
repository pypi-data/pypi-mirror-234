import psutil
from swmonkey.log.log import logger

INTERVAL = 2


class SystemMonitor:
    def __init__(self) -> None:
        self.whitelist = ['swmonkey_runner', 'swmonkey', 'sshd', 'init',
                          'Xorg', 'systemd', 'dbus-daemon']

    def should_release_resource(self, threshold=90) -> bool:
        '''
        监控monkey test执行过程中的系统资源变化,输出到日志
        '''
        cpu_usage = psutil.cpu_percent(interval=1)
        mem_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage('/').percent
        net_info = psutil.net_io_counters()
        logger.info(
            f'CPU:  {cpu_usage}%; Memory: {mem_usage}%; Disk: {disk_usage}%; Net: {net_info.bytes_sent} bytes sent, {net_info.bytes_recv} bytes received')

        # 阈值告警
        if cpu_usage > threshold:
            logger.warning(f'CPU usage is over 90%')
        if mem_usage > threshold:
            logger.warning(f'Memory usage is over 90%')
        if disk_usage > threshold:
            logger.warning(f'Disk usage is over 90%')
        return cpu_usage > threshold or mem_usage > threshold

    def free_resources(self, whitelist=None):
        '''
        释放资源
        '''
        self._kill_high_memory_processes(whitelist)
        self._kill_high_cpu_processes(whitelist)

    def _kill_high_memory_processes(self, whitelist=None, limit=3):
        # Get all running processes
        if whitelist is None:
            whitelist = []
        whitelist.extend(self.whitelist if whitelist is None else [])
        processes = [proc for proc in psutil.process_iter(
            ['pid', 'name', 'memory_percent', 'cpu_percent']) if proc.info['name'] not in whitelist]
        processes.sort(key=lambda x: x.info['memory_percent'], reverse=True)
        killed = 0
        for proc in processes:
            if killed > limit:
                break
            pid = proc.info['pid']
            name = proc.info['name']
            logger.info(
                f'Process {pid} {name} memory usage: {proc.info["memory_percent"]}%')
            # print(f'Process {pid} {name} memory usage: {proc.info["memory_percent"]}%')
            try:
                p = psutil.Process(pid)
                # print process information
                print('pid: %s, name: %s, memory_percent: %s%%, cpu_percent: %s%%' %
                      (pid, name, p.memory_percent(), p.cpu_percent()))
                p.terminate()
                killed += 1
                logger.info(
                    f'进程内存资源释放. Killed process {pid} {name} {p.memory_percent()}%')
            except psutil.ZombieProcess:
                logger.warning(
                    f'Failed to kill process {pid} {name}: Zombie process')
            except psutil.NoSuchProcess:
                logger.warning(
                    f'Failed to kill process {pid} {name}: No such process')
            except psutil.AccessDenied:
                logger.warning(
                    f'Failed to kill process {pid} {name}: Access denied')
            except psutil.TimeoutExpired:
                logger.warning(
                    f'Failed to kill process {pid} {name}: Timeout expired')
            except Exception as e:
                logger.warning(
                    f'An unexpected error occurred when killing process {pid} {name}: {e}')

    def _kill_high_cpu_processes(self, whitelist, limit=3):
        if whitelist is None:
            whitelist = []
        processes = [proc for proc in psutil.process_iter(
            ['pid', 'name', 'cpu_percent']) if proc.info['name'] not in whitelist]
        processes.sort(key=lambda x: x.info['cpu_percent'], reverse=True)
        killed = 0
        for proc in processes:
            if killed > limit:
                break
            pid = proc.info['pid']
            name = proc.info['name']
            logger.info(
                f'进程CPU资源释放. Process {pid} {name} cpu usage: {proc.info["cpu_percent"]}%')
            try:
                p = psutil.Process(pid)
                p.terminate()
                killed += 1
                logger.info(f'Killed process {pid} {name}')
            except psutil.ZombieProcess:
                logger.warning(
                    f'Failed to kill process {pid} {name}: Zombie process')
            except psutil.NoSuchProcess:
                logger.warning(
                    f'Failed to kill process {pid} {name}: No such process')
            except psutil.AccessDenied:
                logger.warning(
                    f'Failed to kill process {pid} {name}: Access denied')
            except psutil.TimeoutExpired:
                logger.warning(
                    f'Failed to kill process {pid} {name}: Timeout expired')
            except Exception as e:
                logger.warning(
                    f'An unexpected error occurred when killing process {pid} {name}: {e}')


if __name__ == '__main__':
    swmonitor = SystemMonitor()
    swmonitor.free_resources()
