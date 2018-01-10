import os


class LockFile(object):
    """
    A class helps handling a lock file.
    1 is locked, 0 is unlocked.
    """

    def __init__(self, path_to_file):
        """
        Init the variables of the class.
        :param path_to_file: The path to the lock file
        :return: None
        """
        self.path_to_file = path_to_file

    def lock(self):
        """
        Lock self
        """
        with open(self.path_to_file, "w") as f:
            f.write(str(os.getpid()))

    def is_locked(self):
        """
        :return: A bool value True is locked, False is unlocked.
        """
        if not os.path.exists(self.path_to_file):
            return False
        with open(self.path_to_file, 'r') as f:
            first_line = f.readline()
            if first_line == "":
                return False
            return check_pid(first_line)


def check_pid(pid):
    """
    Check For the existence of a unix pid.
    """
    try:
        os.kill(int(pid), 0)
    except OSError:
        return False
    else:
        return True
