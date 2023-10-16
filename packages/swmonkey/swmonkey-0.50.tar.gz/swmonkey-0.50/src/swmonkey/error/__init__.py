class SystemUsageError(Exception):
    """
    When CPU, Memory or Disk usage is over 90%, raise this error
    """
    pass


class AppWindowNotFoundError(Exception):
    """
    When app window is not found, raise this error
    """
    pass
