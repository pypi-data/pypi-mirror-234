import time

from tketool.files import *
import importlib.resources, os


def get_prompt(key: str, lang="english", return_details=False, folder=None):
    def get_file_path(lang, key):
        path = os.path.join("lmc", "prompts", "templates", lang, f"{key}.txt")
        # 非DEBUG模式，我们试图从安装的包中获取文件
        return importlib.resources.files('tketool').joinpath(path)

    if folder is None:
        path = get_file_path(lang, key)
    else:
        path = os.path.join(folder, lang, f"{key}.txt")
    doc = read_prompt_file(path)
    if return_details:
        return doc
    else:
        return doc['templatestr']


def read_prompt_file(path) -> dict:
    lines = read_file_lines(path)

    output_dict = {}
    params_dict = {}

    # 处理版本号
    version = lines[0].strip().split(' ')[1]
    output_dict['version'] = version

    # 处理介绍
    description = lines[1].strip()
    output_dict['description'] = description

    line_index = 2
    while True:
        current_line = lines[line_index].strip()

        # 当遇到固定的'start'时，停止处理参数
        if current_line.startswith("start"):
            break

        # 处理参数
        key_value = current_line.split(':')
        params_dict[key_value[0].strip()] = key_value[1].strip()

        line_index += 1

    output_dict['params'] = params_dict

    # 处理模板字符串
    template_str = '\n'.join(lines[line_index + 1:]).strip()
    output_dict['templatestr'] = template_str

    return output_dict


def write_prompt_file(path, version, des, params: {}, str_template):
    lines = []
    lines.append(f"version {version}")
    lines.append(des)
    for k, v in params.items():
        lines.append(f"{k}: {v}")
    lines.append("start:")
    lines.append(str_template)

    write_file_line(path, lines)
