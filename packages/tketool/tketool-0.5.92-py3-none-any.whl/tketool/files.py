import os, importlib.util
import shutil
import paramiko
from paramiko import SFTPClient, SSHClient
from tketool.logs import log


def create_folder_if_not_exists(*args) -> str:
    """
    Create a folder at the specified path if it doesn't exist.

    :param args: Segments of the path, similar to os.path.join.
    :return: The constructed path.
    """
    path = os.path.join(*args)
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
    return path


def write_file_line(path: str, lines: list) -> None:
    """
    Write a list of lines to a file.

    :param path: Path to the file.
    :param lines: List of lines to write.
    """
    write_file(path, "\n".join(lines))


def read_file_lines(path: str) -> list:
    """
    Read lines from a file.

    :param path: Path to the file.
    :return: List of lines from the file.
    """
    try:
        with open(path, 'r') as ff:
            return [line.strip() for line in ff.readlines()]
    except Exception as e:
        print(f"Error reading from file {path}. Reason: {e}")
        return []


def write_file(path: str, content: str) -> None:
    """
    Write a list of lines to a file.

    :param path: Path to the file.
    :param lines: List of lines to write.
    """
    try:
        with open(path, 'w') as ff:
            ff.write(content)
    except Exception as e:
        print(f"Error writing to file {path}. Reason: {e}")


def read_file(path: str) -> str:
    """
    Read lines from a file.

    :param path: Path to the file.
    :return: List of lines from the file.
    """
    try:
        with open(path, 'r') as ff:
            return ff.read()
    except Exception as e:
        print(f"Error reading from file {path}. Reason: {e}")
        return []


def enum_directories(path, recursive=False):
    """
    遍历指定路径下的所有文件夹
    :param path: 要遍历的路径
    :param recursive: 是否递归遍历子文件夹
    :return: 返回一个元组，包含全路径和文件夹名
    """
    for root, dirs, files in os.walk(path):
        for dir_name in dirs:
            yield os.path.join(root, dir_name), dir_name

        # 如果不需要递归，则只需处理顶层目录
        if not recursive:
            break


def enum_files(path, recursive=False):
    """
    遍历指定路径下的所有文件
    :param path: 要遍历的路径
    :param recursive: 是否递归遍历子文件夹
    :return: 返回一个元组，包含全路径和文件名
    """
    for root, dirs, files in os.walk(path):
        for file_name in files:
            yield os.path.join(root, file_name), file_name

        # 如果不需要递归，则只需处理顶层目录
        if not recursive:
            break


def delete_files_in_directory(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def get_file_path_in_sftpserver(folder_path, filename, endpoint, access_user, secret_pwd, remote_folder_path, port=22):
    local_path = os.path.join(folder_path, filename)
    if os.path.exists(local_path):
        return local_path

    log(f"start download the file '{filename}'")

    _sshclient = SSHClient()
    _sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    _sshclient.connect(endpoint, port, access_user, secret_pwd)
    _sftpclient = SFTPClient.from_transport(_sshclient.get_transport())

    remote_path = f"{remote_folder_path}/{filename}"
    _sftpclient.get(remote_path, local_path)

    log(f"download the file '{filename}' completed.")

    _sshclient.close()
    return local_path
