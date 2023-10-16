import io
import paramiko
from paramiko import SFTPClient, SSHClient
from tketool.mlsample.LocalSampleSource import LocalDisk_NLSampleSource
from tketool.JConfig import get_config_instance
from tketool.files import create_folder_if_not_exists
from tketool.utils.progressbar import process_status_bar
import os


class SSHSampleSource(LocalDisk_NLSampleSource):

    @staticmethod
    def instance_default():
        folder_path = get_config_instance().get_config("ssh_samplesource_folderpath")
        endpoint = get_config_instance().get_config("ssh_samplesource_endpoint")
        access_user = get_config_instance().get_config("ssh_samplesource_user")
        access_pwd = get_config_instance().get_config("ssh_samplesource_pwd")
        access_target_path = get_config_instance().get_config("ssh_samplesource_target_apth")

        return SSHSampleSource(folder_path, endpoint, access_user, access_pwd, access_target_path)

    def __init__(self, folder_path, endpoint, access_user, secret_pwd, target_path, port=22):
        super().__init__(folder_path)
        self._folder_path = folder_path
        self._endpoint = endpoint
        self._access_key = access_user
        self._secret_key = secret_pwd
        self._target_path = target_path
        self._porter = port

        self._sshclient = SSHClient()
        self._sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        self._sshclient.connect(self._endpoint, self._porter, self._access_key, self._secret_key)
        self._sftpclient = SFTPClient.from_transport(self._sshclient.get_transport())

    def _download_if_not_exsited(self, name: str):
        if super().has_set(name):
            return
        all_sets = self._sftpclient.listdir(self._target_path)
        if name in all_sets:
            create_folder_if_not_exists(os.path.join(self.base_folder, name))

            all_set_files = self._sftpclient.listdir(os.path.join(self._target_path, name))

            bar = process_status_bar()
            for remote_f in bar.iter_bar(all_set_files, key="download", max=len(all_set_files)):
                bar.process_print(f"Download the set {name} ...")

                remote_path = os.path.join(self._target_path, name, remote_f)
                local_path = os.path.join(self.base_folder, name, remote_f)
                self._sftpclient.get(remote_path, local_path)
        else:
            raise Exception("没有此set")

    def _object_exsited(self, name_or_path):
        try:
            info = self._sftpclient.stat(name_or_path)
            return True, info.st_size
        except BaseException:
            return False, -1

    def update(self, set_name=None):

        super().flush()
        if set_name is not None:
            local_sets = [set_name]
        else:
            local_sets = super().get_dir_list()

        all_remote_list = self._sftpclient.listdir(self._target_path)

        # comput count
        totle_count = 0
        for set in local_sets:
            for file in [f for f in os.listdir(os.path.join(self._folder_path, set)) if not f.startswith('.')]:
                totle_count += 1

        pb = process_status_bar()
        for set in pb.iter_bar(local_sets, key="set", max=len(local_sets)):
            pb.process_print(f"Upload set '{set}'")

            set_dir = self._target_path + "/" + set

            if set not in all_remote_list:
                self._sftpclient.mkdir(set_dir)

            file_list = [f for f in os.listdir(os.path.join(self._folder_path, set)) if not f.startswith('.')]
            for file in pb.iter_bar(file_list, key="file", max=len(file_list)):
                f_l_path = os.path.join(self._folder_path, set, file)
                o_path = os.path.join(set_dir, file)

                exsited_state, remote_size = self._object_exsited(o_path)

                if not exsited_state:
                    self._sftpclient.put(f_l_path, o_path)
                    # client.fput_object(self._bucket_name, o_path, f_l_path)
                else:
                    with self._sftpclient.open(o_path, 'rb') as f_obj:
                        remote_data = f_obj.read(160)

                    with open(f_l_path, 'rb') as f_obj:
                        fobj_data = f_obj.read(160)
                    local_size = os.path.getsize(f_l_path)
                    if (remote_data != fobj_data) or (remote_size != local_size):
                        self._sftpclient.put(f_l_path, o_path)

    def create_new_set(self, name: str, description: str, tags: [str], keys: [str], base_set="",
                       base_set_process="") -> bool:
        if self.has_set(name):
            raise Exception("已存在同名的set")
        return super().create_new_set(name, description, tags, keys, base_set=base_set,
                                      base_set_process=base_set_process)

    def has_set(self, name: str) -> bool:
        if super().has_set(name):
            return True
        all_sets = self._sftpclient.listdir(self._target_path)
        if name in all_sets:
            return True
        return False

    def add_row(self, name: str, data) -> bool:
        self._download_if_not_exsited(name)
        return super().add_row(name, data)

    def get_metadata_keys(self, name: str) -> {}:
        self._download_if_not_exsited(name)
        return super().get_metadata_keys(name)

    def iter_data(self, name: str):
        self._download_if_not_exsited(name)
        return super().iter_data(name)

    def get_remote_dir_list(self) -> {}:
        """
        获得远程所有set的列表信息
        :return: 远程所有set信息的列表
        """
        sets = self._sftpclient.listdir(self._target_path)
        sets_infos = {}
        start_seek = self.int_size * 5 + self.pointer_size + self.header_node_size
        for p_set in sets:
            with io.BytesIO() as ib:
                o_path = f"{p_set}/{p_set}.dlib"
                with self._sftpclient.open(o_path, 'rb') as f_obj:
                    remote_data = f_obj.read(start_seek)
                # remote_data = client.get_object(self._bucket_name, o_path, 0, start_seek).data
                ib.write(remote_data)
                ib.seek(0)
                file_index, append_seek, data_start_seek, count, filecount, current_count = self._read_base_header(
                    ib)
                node = self._read_node(ib)
                sets_infos[p_set] = {
                    'meta': node,
                    'count': count,
                    'filecount': filecount
                }
        return sets_infos

    def download(self, name):
        """
        下载特定的set到本地
        :param name: 需要下载的set名称
        :return: 无返回
        """
        self._download_if_not_exsited(name)
