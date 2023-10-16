import os, pickle, io
import time


class chunk_file():
    def __init__(self, file_path):
        self.key_file_path = file_path + ".key"
        self.value_file_path = file_path + ".value"

        self.index_dict = {}
        self.write_next_loc = 0

        if os.path.exists(self.key_file_path):
            with open(self.key_file_path, "rb") as ff:
                self.index_dict = pickle.load(ff)

        open(self.value_file_path, "ab").close()
        self.file_obj = open(self.value_file_path, "rb+")

    def __contains__(self, item):
        return item in self.index_dict

    def __iter__(self):
        for item_key in self.index_dict.keys():
            yield item_key, self.get(item_key)

    def __getitem__(self, key):
        return self.get(key)

    def verify_data(self):
        for item, val in self:
            pass
        return True

    def add(self, key, value):
        with io.BytesIO() as temf:
            pickle.dump(value, temf)
            act_len = temf.tell()
            temf.seek(0)
            self.file_obj.seek(self.write_next_loc)
            self.file_obj.write(temf.read(act_len))
            self.index_dict[key] = (self.write_next_loc, act_len)
            self.write_next_loc = self.file_obj.tell()

        return act_len

    def get(self, key):
        if key not in self.index_dict:
            return None
        loc, len = self.index_dict[key]
        with io.BytesIO() as bf:
            self.file_obj.seek(loc)
            bf.write(self.file_obj.read(len))
            bf.seek(0)
            return pickle.load(bf)

    def flush(self):
        self.file_obj.flush()
        with open(self.key_file_path, 'wb') as ff:
            pickle.dump(self.index_dict, ff)
