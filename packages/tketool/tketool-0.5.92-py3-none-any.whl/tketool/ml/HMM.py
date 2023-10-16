import time
import numpy as np
from tketool.ml.modelbase import Model_Base
from hmmlearn.hmm import CategoricalHMM
import abc


class HMM_Base(Model_Base):

    def __init__(self):
        super().__init__()

    @property
    def init_prob(self):
        return self.save_variables['init_prob']

    @init_prob.setter
    def init_prob(self, v):
        self.save_variables['init_prob'] = v

    @property
    def trans_prob(self):
        return self.save_variables['trans_prob']

    @trans_prob.setter
    def trans_prob(self, v):
        self.save_variables['trans_prob'] = v

    @property
    def emission_prob(self):
        return self.save_variables['emission_prob']

    @emission_prob.setter
    def emission_prob(self, v):
        self.save_variables['emission_prob'] = v

    @property
    def state_count(self):
        return self.save_variables['state_count']

    @abc.abstractmethod
    def seq_match(self, X):
        pass

    @abc.abstractmethod
    def seq_decode(self, X):
        pass

    @abc.abstractmethod
    def train(self, X, *args):
        pass

    @abc.abstractmethod
    def init_model(self, hidden_state_count: int, *args):
        pass

    @abc.abstractmethod
    def load_init_model(self, path_or_stream):
        pass


def _normalized(list_a):
    arr = np.array(list_a)
    sum_arr = np.sum(arr)
    if sum_arr == 0:
        return 0
    else:
        return arr / sum_arr


class categorical_hmm(HMM_Base):

    def __init__(self):
        super().__init__()
        self.model = None

    @property
    def model_name(self):
        return "categorical_hmm"

    def seq_match(self, X):
        return self.model.bic(X)

    def seq_decode(self, X):
        return self.model.decode(X)

    def train(self, X, custom_start_prob=None, custom_trans_prob=None, *args):
        """
        X: shape [ sample, leq, feature]
        """
        if custom_trans_prob is not None:
            self.model.transmat_ = np.array([_normalized(l) for l in custom_trans_prob])

        if custom_start_prob is not None:
            self.model.startprob_ = _normalized(custom_start_prob)

        train_x = []
        length = []
        for sub in X:
            length.append(len(sub))
            for inp in sub:
                train_x.append(inp)
        self.model.fit(train_x, lengths=length)

        self.init_prob = self.model.startprob_.tolist()
        self.trans_prob = self.model.transmat_.tolist()
        self.emission_prob = self.model.emissionprob_.tolist()

    def init_model(self, hidden_state_count: int, *args):
        self.save_variables['state_count'] = hidden_state_count
        self.model = CategoricalHMM(n_components=hidden_state_count)
        time.time()

    def load_init_model(self, load_init_model):
        self.load(load_init_model)
        self.model = CategoricalHMM(n_components=self.save_variables['state_count'])
        self.model.startprob_ = np.array(self.init_prob)
        self.model.transmat_ = np.array(self.trans_prob)
        self.model.emissionprob_ = np.array(self.emission_prob)


