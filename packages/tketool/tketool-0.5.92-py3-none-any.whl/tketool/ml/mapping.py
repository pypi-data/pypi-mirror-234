from tketool.ml.modelbase import Model_Base


class mapping(Model_Base):
    @property
    def model_name(self):
        return "mapping"

    def __init__(self):
        super().__init__()
        self.save_variables['left_dic'] = {}
        self.save_variables['right_dic'] = {}
        self.save_variables['content'] = []
        # self.left_dic = {}
        # self.right_dic = {}
        # self.content = []

    def add(self, left, right):
        index = len(self.save_variables['content'])
        self.save_variables['content'].append([left, right])
        if left not in self.save_variables['left_dic']:
            self.save_variables['left_dic'][left] = []
        self.save_variables['left_dic'][left].append(index)
        if right not in self.save_variables['right_dic']:
            self.save_variables['right_dic'][right] = []
        self.save_variables['right_dic'][right].append(index)

    def left(self, left):
        if left in self.save_variables['left_dic']:
            return [self.save_variables['content'][idx][1] for idx in self.save_variables['left_dic'][left]]
        return None

    def right(self, right):
        if right in self.save_variables['right_dic']:
            return [self.save_variables['content'][idx][0] for idx in self.save_variables['right_dic'][right]]
        return None
