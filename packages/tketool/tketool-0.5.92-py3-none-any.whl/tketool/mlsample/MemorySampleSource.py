from tketool.mlsample.NLSampleSource import NLSampleSourceBase


class Memory_NLSampleSource(NLSampleSourceBase):
    """
    构建一个基于内存的SampleSource
    """

    def __init__(self):
        self.datas = {}

    def create_new_set(self, name: str, description: str, tags: [str], keys: [str], base_set="",
                       base_set_process="") -> bool:
        if name in self.datas:
            raise Exception("已存在相同的set")

        self.datas[name] = {
            'name': name,
            'des': description,
            'tags': tags,
            'label_keys': keys,
            'base_set': base_set,
            'base_set_process': base_set_process,
            'data': [],
        }

        return True

    def has_set(self, name: str) -> bool:
        return name in self.datas

    def add_row(self, name: str, data: []) -> bool:
        self.datas[name]['data'].append(data)
        return True

    def get_metadata_keys(self, name: str) -> {}:
        return {
            'des': self.datas[name]['des'],
            'tags': self.datas[name]['tags'],
            'label_keys': self.datas[name]['label_keys'],
            'base_set': self.datas[name]['base_set'],
            'base_set_process': self.datas[name]['base_set_process'],
        }

    def get_dir_list(self) -> {}:
        # 'meta': node,
        # 'count': count,
        # 'filecount': filecount
        return {x_key: {
            'meta': self.get_metadata_keys(x_key),
            'count': self.get_set_count(x_key),
        }
            for x_key in self.datas.keys()}

    def iter_data(self, name: str):
        for item in self.datas[name]['data']:
            yield item

    def iter_pointer(self, name: str):
        for idx in range(len(self.datas[name]['data'])):
            yield idx

    def delete_set(self, name: str):
        del self.datas[name]

    def load_pointer_data(self, name: str, pointer):
        return self.datas[name]['data'][pointer]

    def get_set_count(self, name: str):
        return len(self.datas[name]['data'])

    def add_attachment(self, set_name: str, key, data):
        raise Exception("not support")

    def read_attachment(self, set_name: str):
        raise Exception("not support")

    def read_one_row(self, set_name: str):
        return self.datas[set_name]['data'][0]
