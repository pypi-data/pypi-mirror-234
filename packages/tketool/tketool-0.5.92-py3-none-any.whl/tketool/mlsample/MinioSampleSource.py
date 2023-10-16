import io
from tketool.utils.progressbar import process_status_bar
from tketool.mlsample.LocalSampleSource import LocalDisk_NLSampleSource
import os
from minio import Minio


class MinioSampleSource(LocalDisk_NLSampleSource):
    """
    Minio远程数据源，同步LocalDisk数据源，继承自LocalDisk
    """

    def __init__(self, folder_path, endpoint, access_key, secret_key, bucket_name):
        """
        初始化方法
        :param folder_path: 本地缓存目录
        :param endpoint: minio的地址
        :param access_key: minio的access key
        :param secret_key: minio的secret key
        :param bucket_name: bucket名称
        """
        super().__init__(folder_path)
        self._folder_path = folder_path
        self._endpoint = endpoint
        self._access_key = access_key
        self._secret_key = secret_key
        self._bucket_name = bucket_name
        self._minio_client = None

    def _join(self, *args):
        args_list = [item for item in args]
        return "/".join(args_list)

    def _get_minio_client(self):
        if self._minio_client is None:
            self._minio_client = Minio(self._endpoint, self._access_key, self._secret_key, secure=False)
            if not self._minio_client.bucket_exists(self._bucket_name):
                raise Exception("此bucket不存在")
        return self._minio_client

    def _download_if_not_exsited(self, name: str):
        if super().has_set(name):
            return
        client = self._get_minio_client()
        all_sets = {obj.object_name.strip('/') for obj in client.list_objects(self._bucket_name)}
        if name in all_sets:
            os.mkdir(os.path.join(self.base_folder, name))
            all_set_files = list(client.list_objects(self._bucket_name, prefix=f"{name}/"))

            bar = process_status_bar()
            for remote_f in bar.iter_bar(all_set_files, key="download", max=len(all_set_files)):
                bar.process_print(f"Download the set {name} ...")
                file_name = os.path.split(remote_f.object_name)[-1]
                client.fget_object(self._bucket_name, remote_f.object_name,
                                   os.path.join(self.base_folder, name, file_name))
        else:
            raise ("没有此set")

    def _object_exsited(self, name):
        try:
            client = self._get_minio_client()
            client.stat_object(self._bucket_name, name)
            return True
        except:
            return False

    def update(self, set_name=None):
        """
        提交本地更改到服务器
        :param set_name: 提交的set名称，默认为所有更改
        :return:
        """
        super().flush()
        client = self._get_minio_client()
        if set_name is not None:
            local_sets = [set_name]
        else:
            local_sets = super().get_dir_list()

        # comput count
        totle_count = 0
        for set in local_sets:
            for file in [f for f in os.listdir(os.path.join(self._folder_path, set)) if not f.startswith('.')]:
                totle_count += 1

        pb = process_status_bar()
        for set in pb.iter_bar(local_sets, key="set", max=len(local_sets)):
            pb.process_print(f"Upload set '{set}'")
            file_list = [f for f in os.listdir(os.path.join(self._folder_path, set)) if not f.startswith('.')]
            for file in pb.iter_bar(file_list, key="file", max=len(file_list)):
                f_l_path = os.path.join(self._folder_path, set, file)
                o_path = self._join(set, file)
                if not self._object_exsited(o_path):
                    client.fput_object(self._bucket_name, o_path, f_l_path)
                else:
                    remote_data = client.get_object(self._bucket_name, o_path, 0, 160).data
                    remote_info = client.stat_object(self._bucket_name, o_path)
                    with open(f_l_path, 'rb') as f_obj:
                        fobj_data = f_obj.read(160)
                    local_size = os.path.getsize(f_l_path)
                    if (remote_data != fobj_data) and (remote_info.size == local_size):
                        client.fput_object(self._bucket_name, o_path, f_l_path)

    def create_new_set(self, name: str, description: str, tags: [str], keys: [str], base_set="",
                       base_set_process="") -> bool:
        if self.has_set(name):
            raise Exception("已存在同名的set")
        return super().create_new_set(name, description, tags, keys, base_set=base_set,
                                      base_set_process=base_set_process)

    def has_set(self, name: str) -> bool:
        if super().has_set(name):
            return True
        client = self._get_minio_client()
        all_sets = {obj.object_name: obj.is_dir for obj in client.list_objects(self._bucket_name)}
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
        client = self._get_minio_client()
        sets = [obj.object_name.strip('/') for obj in client.list_objects(self._bucket_name)]
        sets_infos = {}
        start_seek = self.int_size * 5 + self.pointer_size + self.header_node_size
        for p_set in sets:
            with io.BytesIO() as ib:
                o_path = f"{p_set}/{p_set}.dlib"
                remote_data = client.get_object(self._bucket_name, o_path, 0, start_seek).data
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

    def read_one_row(self, name: str):
        client = self._get_minio_client()

        start_seek = self.int_size * 5 + self.pointer_size + self.header_node_size

        with io.BytesIO() as ib:
            o_path = f"{name}/{name}.dlib"
            remote_data = client.get_object(self._bucket_name, o_path, 0, start_seek + self.int_size * 2).data
            ib.write(remote_data)
            ib.seek(0)
            file_index, append_seek, data_start_seek, count, filecount, current_count = self._read_base_header(
                ib)
            node = self._read_node(ib)
            ib.seek(data_start_seek)
            f_len = self._read_int(ib)
            act_len = self._read_int(ib)

            ib.seek(0)
            remote_data = client.get_object(self._bucket_name, o_path, data_start_seek,
                                            act_len + self.int_size * 2).data
            ib.write(remote_data)
            ib.seek(0)

            node = self._read_node(ib)

            return node
