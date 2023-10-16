import abc, pickle


class Model_Base(metaclass=abc.ABCMeta):

    def __init__(self):
        self.save_variables = {}

    @property
    @abc.abstractmethod
    def model_name(self):
        pass

    def save(self, path_or_stream):
        if isinstance(path_or_stream, str):
            with open(path_or_stream, "wb") as f:
                pickle.dump(self.save_variables, f)
        else:
            pickle.dump(self.save_variables, path_or_stream)

    def load(self, path_or_stream):
        if isinstance(path_or_stream, str):
            with open(path_or_stream, "rb") as f:
                self.save_variables = pickle.load(f)
        else:
            self.save_variables = pickle.load(path_or_stream)
