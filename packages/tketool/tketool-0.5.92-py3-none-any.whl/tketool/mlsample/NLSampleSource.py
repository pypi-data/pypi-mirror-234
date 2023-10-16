import abc
from tketool.logs import log


class NLSampleSourceBase(metaclass=abc.ABCMeta):
    """
    数据存储源的基类，抽象类
    """

    @abc.abstractmethod
    def create_new_set(self, name: str, description: str, tags: [str], keys: [str], base_set="") -> bool:
        """
        创建新的数据set，抽象方法
        :param name: 新set的名称
        :param description: 新set的描述信息
        :param tags: 新set的tag信息
        :param keys: 新set的列名
        :param base_set: 父set的名称
        :return: 是否成功，bool类型返回
        """
        pass

    @abc.abstractmethod
    def has_set(self, name: str) -> bool:
        """
        此数据源中是否包含特定的数据set
        :param name: 需要查找的set名称
        :return: 结果bool类型的值
        """
        pass

    @abc.abstractmethod
    def add_row(self, name: str, data: []) -> bool:
        """
        添加新行
        :param name: 添加的目标set
        :param data: 列信息，list形式，顺序与set的列名顺序相同
        :return: 是否成功的bool返回
        """
        pass

    @abc.abstractmethod
    def get_metadata_keys(self, name: str) -> {}:
        """
        获得set的metadata信息，包括set的定义信息、数量等
        :param name: set名称
        :return: 字典类型的属性集合
        """
        pass

    @abc.abstractmethod
    def get_dir_list(self) -> {}:
        """
        获得当前源的所有set的列表信息
        :return: 字典类型的set集合
        """
        pass

    @abc.abstractmethod
    def iter_data(self, name: str):
        """
        遍历set中所有数据行
        :param name: set名称
        :return: 可迭代的数据对象，每个迭代是一行数据
        """
        pass

    @abc.abstractmethod
    def iter_pointer(self, name: str):
        """
        遍历返回set中所有行的指针信息
        :param name: set名称
        :return: 可迭代的指针对象
        """
        pass

    @abc.abstractmethod
    def delete_set(self, name: str):
        """
        删除特定的set
        :param name: 要删除的set名称
        :return: 无返回
        """
        pass

    @abc.abstractmethod
    def load_pointer_data(self, name: str, pointer):
        """
        通过特定的指针信息获得该指针信息的行
        :param name: set名称
        :param pointer: 指针信息
        :return: 该指针指向的行信息
        """
        pass

    @abc.abstractmethod
    def get_set_count(self, name: str):
        """
        获得set的数量
        :param name: set名称
        :return: 返回数量信息
        """
        pass

    @abc.abstractmethod
    def add_attachment(self, set_name: str, key, data):
        """
        向set添加特定的附加信息
        :param set_name: 添加的set
        :param key: 附加信息的key
        :param data: 附加信息
        :return: 无返回
        """
        pass

    @abc.abstractmethod
    def read_attachment(self, set_name: str):
        """
        读取set的附加信息
        :param set_name: 读取的set名称
        :return: 返回附加信息
        """
        pass

    @abc.abstractmethod
    def read_one_row(self, set_name: str):
        """
        读取set的第一行信息
        :param set_name: set名称
        :return: 第一行的数据
        """
        pass

    def arrange_dir_list(self):
        """
        构建基于树形目录的控制台输出
        :param dir_list: metadata列表，一般取自 get_metadata_keys
        :return: 返回树形字典，表示此数据源所有set的树形结构
        """

        dir_list = self.get_dir_list()

        new_dic = {key: {
            'meta': dir_list[key]['meta'],
            'children': {},
            'count': dir_list[key]['count'],
            'base_set': dir_list[key]['meta']['base_set']
        } for key in dir_list.keys()}

        for set_key in new_dic.keys():
            if new_dic[set_key]['base_set'] != "":
                if new_dic[set_key]['base_set'] not in new_dic:
                    log(f"没有找到{set_key}的父节点，置顶输出")
                    new_dic[set_key]['base_set'] = ""
                else:
                    base_set_name = new_dic[set_key]['base_set']
                    new_dic[base_set_name]['children'][set_key] = new_dic[set_key]

        # if print:
        #     def printsub(level: int, name, item):
        #         blank_str = ""
        #         for _ in range(level):
        #             blank_str += "\t"
        #         print(f"{blank_str} - {name}({item['count']}): {item['meta']['des']}")
        #         for sub_item in item['children'].keys():
        #             printsub(level + 1, sub_item, item['children'][sub_item])
        #
        #     for key in new_dic.keys():
        #         printsub(0, key, new_dic[key])

        return {key: new_dic[key] for key in new_dic if new_dic[key]['base_set'] == ""}

    def print_markdown_arrange_dir_list(self, path=None, max_length=1000):
        """
        打印此数据源所有数据set的预览页（markdown）
        :param dir_list: metadata列表，一般取自 get_metadata_keys
        :param path: 输出目录
        :param max_length: 每行数据的最大现实长度
        :return:
        """

        dir_list = self.get_dir_list()

        local_path = path
        if local_path is None:
            local_path = "data_list.md"

        def doc_to_markdown(s):
            if not isinstance(s, str):
                return s
            alllines = s.split('\n')[:20]
            return "\n >".join(alllines)[:max_length]

        with open(local_path, "w") as file:
            lines = ["[toc]"]
            new_dic = {}
            files_order_list = sorted([k for k in dir_list.keys()], key=lambda item: len(item.split('_')))
            key_pointers = {}
            for set_key in files_order_list:
                row_key = dir_list[set_key]['meta']['label_keys']
                one_row = self.read_one_row(set_key)
                if dir_list[set_key]['meta']['base_set'] == "":
                    new_dic[set_key] = {
                        'meta': dir_list[set_key]['meta'],
                        'children': {},
                        'count': dir_list[set_key]['count'],
                        'row_sample': zip(row_key, one_row)
                    }
                    key_pointers[set_key] = new_dic[set_key]
                else:
                    base_set_name = dir_list[set_key]['meta']['base_set']
                    key_pointers[base_set_name]['children'][set_key] = {
                        'meta': dir_list[set_key]['meta'],
                        'children': {},
                        'count': dir_list[set_key]['count'],
                        'row_sample': zip(row_key, one_row)
                    }
                    key_pointers[set_key] = key_pointers[base_set_name]['children'][set_key]

            def printsub(level: int, name, item):
                blank_str = "#"
                for _ in range(level):
                    blank_str += "#"
                lines.append(f"{blank_str} {name}")
                lines.append(f"**{item['meta']['des']}**")
                lines.append(f"count: {item['count']}")
                for key, val in item['row_sample']:
                    new_val = doc_to_markdown(val)
                    lines.append(f"key: {key}")
                    lines.append(f"> {new_val}")
                    lines.append(" ")
                for sub_item in item['children'].keys():
                    printsub(level + 1, sub_item, item['children'][sub_item])

            for key in new_dic.keys():
                printsub(0, key, new_dic[key])

            file.writelines("\n".join(lines))

    def flush(self):
        """
        提交所有更改
        :return: 无返回
        """
        pass
