from tketool.mlsample.NLSampleSource import NLSampleSourceBase
import random


class SampleSet:
    """
    数据源复杂遍历的对象，表征一个数据集
    """

    def __init__(self, source_base: NLSampleSourceBase,
                 set_name: str,
                 ):
        """
        初始化方法
        :param source_base: 数据源
        :param set_name: 数据源的set名称
        """
        self._sample_source = source_base
        self._set_name = set_name
        self._shuffle = False

        self._data_keys = source_base.get_metadata_keys(set_name)

        self._iter_keys = []

        self._loaded_pointer = False

        self._func = [self._base_iter]

        self._count = self._sample_source.get_set_count(self._set_name)

    def __iter__(self):
        """
        遍历的内置实现
        :return: 可迭代对象
        """
        return self._func[-1]()

    @property
    def sample_source(self):
        """
        数据源属性
        :return: 返回该set的数据源实例
        """
        return self._sample_source

    @property
    def set_name(self):
        """
        数据set的名称
        :return: 返回数据set名称
        """
        return self._set_name

    def count(self):
        """
        数据set的数量
        :return: 返回数据set的数量
        """
        return self._count

    def _base_iter(self):

        if self._loaded_pointer == False:
            totle_count = 0
            # for file_index, seek_p in self._sample_source.iter_pointer(self._set_name):
            #     if file_index not in self._iter_map:
            #         self._iter_map[file_index] = []
            #         self._iter_keys.append(file_index)
            #     self._iter_map[file_index].append(seek_p)
            #     totle_count += 1
            for pointer in self._sample_source.iter_pointer(self._set_name):
                self._iter_keys.append(pointer)
                totle_count += 1
            self._loaded_pointer = True

        if self._shuffle:
            random.shuffle(self._iter_keys)
            # for key in self._iter_map.keys():
            #     random.shuffle(self._iter_map[key])

        for p in self._iter_keys:
            # for p in self._iter_map[key_list]:
            yield {k: v for k, v in
                   zip(self._data_keys['label_keys'], self._sample_source.load_pointer_data(self._set_name,
                                                                                            p))}

    def shuffle(self):
        """
        打乱顺序
        :return: 返回可迭代的实例本身
        """
        self._shuffle = True
        return self

    def take(self, count):
        """
        取一定数量的数据
        :param count: 需要取的数量
        :return: 返回可迭代的实例本身
        """
        fun_index = len(self._func) - 1

        if self._count >= count:
            self._count = count

        def take_func():
            kcount = count
            for _item in self._func[fun_index]():
                kcount -= 1
                if kcount >= 0:
                    yield _item
                else:
                    break

        self._func.append(take_func)
        return self

    def skip(self, count):
        """
        跳过一定量的数据
        :param count: 跳过的数量
        :return: 返回可迭代的实例本身
        """
        fun_index = len(self._func) - 1

        self._count = self._count - count
        if self._count < 0:
            self._count = 0

        def skip_func():
            kcount = count
            for _item in self._func[fun_index]():
                kcount -= 1
                if kcount >= 0:
                    continue
                else:
                    yield _item

        self._func.append(skip_func)
        return self

    def batch(self, batch_count):
        """
        对数据进行batch分组
        :param batch_count: 每个batch的数量
        :return: 返回可迭代的实例本身
        """
        fun_index = len(self._func) - 1

        n_c_a = self._count // batch_count
        n_c_b = self._count % batch_count
        self._count = n_c_a
        if n_c_b > 0:
            self._count += 1

        def batch_func():
            batch_list = []

            b_batch_c = 0
            for _item in self._func[fun_index]():
                batch_list.append(_item)
                b_batch_c += 1

                if b_batch_c == batch_count:
                    yield batch_list
                    b_batch_c = 0
                    batch_list = []

            if b_batch_c > 0:
                yield batch_list

        self._func.append(batch_func)
        return self

    def func(self, func):
        fun_index = len(self._func) - 1

        def func_func():
            for _item in self._func[fun_index]():
                yield func(_item)

        self._func.append(func_func)
        return self
