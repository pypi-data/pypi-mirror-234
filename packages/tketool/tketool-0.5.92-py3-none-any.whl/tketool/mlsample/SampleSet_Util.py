import time, os
from tketool.mlsample.LocalSampleSource import LocalDisk_NLSampleSource
from tketool.JConfig import get_config_instance
from tketool.mlsample.NLSampleSource import NLSampleSourceBase
from tketool.mlsample.MemorySampleSource import Memory_NLSampleSource
from tketool.mlsample.SampleSet import SampleSet
from prettytable import PrettyTable, ALL
from tketool.utils.progressbar import process_status_bar
from PyPDF2 import PdfReader
from tketool.mlsample.MinioSampleSource import MinioSampleSource
from tketool.mlsample.SSHSampleSource import SSHSampleSource
import fnmatch
from tketool.files import read_file
from tketool.logs import convert_print_color, log_color_enum


def _truncate_content(content, max_length):
    return (content[:max_length] + '..') if len(content) > max_length else content


def set_list(tsource="local", path=None, match=None):
    """
    This function generates a PrettyTable list of sets from a specified source directory.
    tsource : The target source type (local,minio,ssh), default is local
    path : The path to the source directory. If not specified, it is obtained from the config instance's 'sample_source_path'.
    match : Search filter by *
    """
    if tsource is None:
        tsource = "local"

    path = path if path else get_config_instance().get_config("sample_source_path")

    info_dict = None

    print(f"source type: {tsource}")

    if tsource == "local":
        if not os.path.exists(path):
            raise Exception(f"can not find the path : {path}")
        source = LocalDisk_NLSampleSource(path)
        info_dict = source.get_dir_list()

    if tsource == "minio":
        endpoint = get_config_instance().get_config("minio_endpoint", "")
        access_key = get_config_instance().get_config("minio_access_key", "")
        secret_key = get_config_instance().get_config("minio_secret_key", "")
        bucket_name = get_config_instance().get_config("minio_bucket_name", "")

        if endpoint == "" or access_key == "" or secret_key == "" or bucket_name == "":
            raise Exception("config is None.")

        source = MinioSampleSource(path, endpoint, access_key, secret_key, bucket_name)
        info_dict = source.get_remote_dir_list()

    if tsource == "ssh":
        # endpoint, access_user, secret_pwd, target_path, port=22
        endpoint = get_config_instance().get_config("ssh_endpoint", "")
        access_key = get_config_instance().get_config("ssh_access_user", "")
        secret_key = get_config_instance().get_config("ssh_secret_pwd", "")
        bucket_name = get_config_instance().get_config("ssh_target_path", "")
        port = get_config_instance().get_config("ssh_port", "22")

        if endpoint == "" or access_key == "" or secret_key == "" or bucket_name == "":
            raise Exception("config is None.")

        source = SSHSampleSource(path, endpoint, access_key, secret_key, bucket_name, int(port))
        info_dict = source.get_remote_dir_list()

        pass

    if info_dict is None:
        raise Exception("Source is error.")

    xtable = PrettyTable()
    # 设置表头
    xtable.field_names = ["Set name", "Count", "Columns", "description", "base_set"]

    all_keys = list(info_dict.keys())

    if match is not None:
        all_keys = [s for s in all_keys if fnmatch.fnmatchcase(s, match)]

    for k in sorted(all_keys):
        v = info_dict[k]
        xtable.add_row([k, v['count'],
                        _truncate_content(str(v['meta']['label_keys']), 30),
                        _truncate_content(v['meta']['des'], 20),
                        _truncate_content(v['meta']['base_set'], 20)
                        ])

    print(xtable)


def download(tsource, set_name, path=None):
    """
    This function download a set in remote to local.
    tsource : The target source type (minio,ssh)
    set_name : The target set name.
    path : The path to the source directory. If not specified, it is obtained from the config instance's 'sample_source_path'.
    """
    path = path if path else get_config_instance().get_config("sample_source_path")

    source = None

    if tsource == "minio":
        endpoint = get_config_instance().get_config("minio_endpoint", "")
        access_key = get_config_instance().get_config("minio_access_key", "")
        secret_key = get_config_instance().get_config("minio_secret_key", "")
        bucket_name = get_config_instance().get_config("minio_bucket_name", "")

        if endpoint == "" or access_key == "" or secret_key == "" or bucket_name == "":
            raise Exception("config is None.")

        source = MinioSampleSource(path, endpoint, access_key, secret_key, bucket_name)

    if tsource == "ssh":
        # endpoint, access_user, secret_pwd, target_path, port=22
        endpoint = get_config_instance().get_config("ssh_endpoint", "")
        access_key = get_config_instance().get_config("ssh_access_user", "")
        secret_key = get_config_instance().get_config("ssh_secret_pwd", "")
        bucket_name = get_config_instance().get_config("ssh_target_path", "")
        port = get_config_instance().get_config("ssh_port", "22")

        if endpoint == "" or access_key == "" or secret_key == "" or bucket_name == "":
            raise Exception("config is None.")

        source = SSHSampleSource(path, endpoint, access_key, secret_key, bucket_name, int(port))

        pass

    if source is None:
        raise Exception("Source Error.")

    source.download(set_name)


def upload(tsource, set_name, path=None):
    """
    This function upload a set to remote .
    tsource : The target source type (minio,ssh)
    set_name : The target set name.
    path : The path to the source directory. If not specified, it is obtained from the config instance's 'sample_source_path'.
    """
    path = path if path else get_config_instance().get_config("sample_source_path")

    source = None

    if tsource == "minio":
        endpoint = get_config_instance().get_config("minio_endpoint", "")
        access_key = get_config_instance().get_config("minio_access_key", "")
        secret_key = get_config_instance().get_config("minio_secret_key", "")
        bucket_name = get_config_instance().get_config("minio_bucket_name", "")

        if endpoint == "" or access_key == "" or secret_key == "" or bucket_name == "":
            raise Exception("config is None.")

        source = MinioSampleSource(path, endpoint, access_key, secret_key, bucket_name)

    if tsource == "ssh":
        # endpoint, access_user, secret_pwd, target_path, port=22
        endpoint = get_config_instance().get_config("ssh_endpoint", "")
        access_key = get_config_instance().get_config("ssh_access_user", "")
        secret_key = get_config_instance().get_config("ssh_secret_pwd", "")
        bucket_name = get_config_instance().get_config("ssh_target_path", "")
        port = get_config_instance().get_config("ssh_port", "22")

        if endpoint == "" or access_key == "" or secret_key == "" or bucket_name == "":
            raise Exception("config is None.")

        source = SSHSampleSource(path, endpoint, access_key, secret_key, bucket_name, int(port))

        pass

    if source is None:
        raise Exception("Source Error.")

    source.update(set_name)


def set_info(setname, count=5, max_len=100, path=None):
    """
    This function prints out detailed information about a specific set.
    setname : The name of the specific set.
    count : count of print sample . default is 5
    max_len : max len of data will print. default is 100
    path : The path to the source directory. If not specified, it is obtained from the config instance's 'sample_source_path'.
    """
    path = path if path else get_config_instance().get_config("sample_source_path")
    if not os.path.exists(path):
        raise Exception(f"can not find the path : {path}")
    source = LocalDisk_NLSampleSource(path)

    meta_data = source.get_metadata_keys(setname)

    print("basic info: \n")
    table = PrettyTable(header=False)
    table.hrules = ALL
    # 定义表格的列名
    table.field_names = ["Attribute", "Value"]
    # 添加数据
    table.add_row(["Name", setname])
    table.add_row(["Count", source.get_set_count(setname)])
    table.add_row(["base set", meta_data['base_set']])
    table.add_row(["keys", meta_data['label_keys']])
    table.add_row(["tags", meta_data['tags']])
    table.add_row(["des", meta_data['des']])
    print(table)
    print("Set file info:")
    source.print_set_info(setname)
    print(f"Set Data (first {str(count)} row):")
    for item in SampleSet(source, setname).take(count):
        print("---" * 3)
        for k, v in item.items():
            vv=str(v)
            v_data = f" {vv[:max_len]}"
            if len(vv) > max_len:
                print(convert_print_color((k + "\t:", log_color_enum.GREEN), v_data, ("...", log_color_enum.YELLOW)))
            else:
                print(convert_print_color((k + "\t:", log_color_enum.GREEN), v_data))


def set_data_info(setname, label_key, path=None):
    """
    This function prints the count of  per label key.
    setname : The name of the specific set.
    label_key : Statistics the result will use the key
    path : The path to the source directory. If not specified, it is obtained from the config instance's 'sample_source_path'.
    """
    path = path if path else get_config_instance().get_config("sample_source_path")
    if not os.path.exists(path):
        raise Exception(f"can not find the path : {path}")
    source = LocalDisk_NLSampleSource(path)

    content_key = {}
    for item in SampleSet(source, setname):
        label_value = item[label_key]
        if label_value not in content_key:
            content_key[label_value] = 0
        content_key[label_value] += 1

    print("Data info (count of per label key): \n")
    table = PrettyTable(header=False)
    table.hrules = ALL
    # 定义表格的列名
    table.field_names = ["Attribute", "Value"]

    for k, v in content_key.items():
        table.add_row([k, v])

    print(table)


def delete_set(setname, path=None):
    """
    This function deletes a specific set from a specified source directory.
    setname : The name of the specific set to be deleted.
    path : The path to the source directory.
    """
    path = path if path else get_config_instance().get_config("sample_source_path")
    if not os.path.exists(path):
        raise Exception(f"can not find the path : {path}")
    source = LocalDisk_NLSampleSource(path)
    source.delete_set(setname)
    print(f"{setname} deleted.")


def capture_str(setname, folderpath, path=None):
    """
    This function captures all the files in a given folder path into a set.
    setname: The name of the specific set to be deleted.
    folderpath: The path to the folder containing the files.
    path: The path to the source directory.
    """
    path = path if path else get_config_instance().get_config("sample_source_path")
    if not os.path.exists(path):
        raise Exception(f"can not find the path : {path}")

    source = LocalDisk_NLSampleSource(path)
    # source = Memory_NLSampleSource()
    source.create_new_set(setname, "capture from folder", ['capture'], ['filename', 'text'])

    pb = process_status_bar()
    allfiles = os.listdir(folderpath)

    for filename in pb.iter_bar(allfiles):
        try:
            name, ext = os.path.splitext(filename)
            if ext == ".txt":
                content = read_file(os.path.join(folderpath, filename))
                source.add_row(setname, [filename, content])
                continue

            if ext == '.pdf':
                pdf_file_obj = open(os.path.join(folderpath, filename), 'rb')
                pdf_reader = PdfReader(pdf_file_obj)

                text = ''
                for page in pdf_reader.pages:
                    # page_obj = pdf_reader.pages[page_num]  # getPage(page_num)
                    text += page.extract_text()
                pdf_file_obj.close()
                source.add_row(setname, [filename, text])
                continue

            raise Exception(f"Can't capture the file {filename}")


        except Exception as ex:
            pb.print_log(f"file {filename} error. {ex}")

    source.flush()


# def Info_of_set(sample_set: SampleSet, key_func):
#     key_dict = {}
#     for item in sample_set:
#         lable = key_func(item)
#         if lable not in key_dict:
#             key_dict[lable] = 0
#         key_dict[lable] += 1
#
#     # PRINT
#     print("\n 统计结果:")
#     for k, v in key_dict.items():
#         print(f"{k} : {v} \n")


def SplitSet(samplesource: NLSampleSourceBase, ori_set_name: str, key_func,
             name_to_key_dict: dict, need_shuffle=True):
    meta_data = samplesource.get_metadata_keys(ori_set_name)
    new_set_name_gen_list = []

    # Create new sample sets based on the provided name-to-key dictionary
    for n_setname in name_to_key_dict.keys():
        n_name = f"{ori_set_name}_{n_setname}"
        samplesource.create_new_set(n_name, f"split from {ori_set_name}", ["split"],
                                    meta_data['label_keys'], ori_set_name)
        new_set_name_gen_list.append(n_name)

    sample_set = SampleSet(samplesource, ori_set_name)
    if need_shuffle:
        sample_set = sample_set.shuffle()

    # Initialize a list of counters, each element is a dictionary to track the label count for a subset
    count_list = [{} for _ in name_to_key_dict.values()]

    for item in sample_set:
        cur_label = key_func(item)
        list_formattor = [item[key] for key in meta_data['label_keys']]
        # Find the appropriate subset
        for idx, subset_name in enumerate(name_to_key_dict.keys()):
            subset_dict = name_to_key_dict[subset_name]
            if cur_label in subset_dict and subset_dict[cur_label] > count_list[idx].get(cur_label, 0):
                samplesource.add_row(new_set_name_gen_list[idx], list_formattor)
                count_list[idx][cur_label] = count_list[idx].get(cur_label, 0) + 1
                break

    samplesource.flush()
