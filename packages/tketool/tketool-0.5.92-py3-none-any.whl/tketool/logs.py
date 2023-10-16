from enum import Enum
from datetime import datetime
import os
from tketool.utils.progressbar import get_process_bar_current


def _handle_console(str):
    bar = get_process_bar_current()
    if bar is None:
        print(str + "\n")
    else:
        bar.print_log(str)


_file_instance = None


def print_dash_line():
    try:
        # 获取控制台的宽度
        console_width = os.get_terminal_size().columns
        # 打印指定长度的'-'
        log('-' * console_width, no_header=True)
    except Exception as ex:
        log('-' * 20, no_header=True)


def _handle_file(str):
    global _file_instance
    if _file_instance is None:
        _file_instance = open("log.txt", "a")

    _file_instance.read(str + "\n")
    _file_instance.flush()


handle_type_enum_dict = {
    "console": _handle_console,
    "file": _handle_file
}


class log_color_enum(Enum):
    DEFAULT = ""
    RED = "\033[91m"
    YELLOW = "\033[93m"
    GREEN = "\033[92m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"


def convert_print_color(*args):
    """
    函数返回带有指定颜色的字符串。

    :param args: 可变数量的参数，每个参数可以是字符串或一个包含字符串和log_color_enum的元组。
    :return: 拼接好的带有颜色代码的字符串
    """
    result = []

    for arg in args:
        if isinstance(arg, tuple) and len(arg) == 2 and isinstance(arg[1], log_color_enum):
            # 元组包含字符串和颜色枚举
            result.append(f"{arg[1].value}{arg[0]}\033[0m")
        else:
            # 只有字符串
            result.append(arg)

    return ''.join(result)


log_handles = {
    "console": _handle_console,
}


def add_log_handle(key: str, func=None):
    if key in handle_type_enum_dict:
        log_handles[key] = handle_type_enum_dict[key]
    else:
        log_handles[key] = func


def remove_log_handle(key: str):
    if key in log_handles:
        del log_handles[key]


def get_log_handle():
    return list(log_handles.keys())


def log(str, no_header=False):
    if not no_header:
        current_date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        str = f'[{current_date_time}] {str}'

    for k, v in log_handles.items():
        v(str)
    # print(f"{str}\n")  # Using \033[0m to reset the color after printing


def log_debug(str, no_header=False):
    log(str, no_header)


def log_state(str):
    bar = get_process_bar_current()
    if bar is None:
        log(str)
    else:
        bar.process_print(str)
