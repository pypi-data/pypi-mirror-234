from .console_handler import ConsoleHandler
from .json_file_handler import JsonFileHandler


def _get_path():
    from os import getcwd
    from os.path import join

    _project_folder = getcwd()
    return join(_project_folder, "log.json")


log_file_path = _get_path()

#
# class Path:
#     __log_file_path = _get_path()
#
#     @property
#     def log_file_path(self):
#         return self.__log_file_path
#
#     @log_file_path.setter
#     def log_file_path(self, value):
#         self.__log_file_path = value
#
#
# __path = Path()
# log_file_path = __path.log_file_path


# def get_log_file_path():
#     return log_file_path
#
#
# def set_path(path: str):
#     globals()["log_file_path"] = path
#     print(log_file_path)
