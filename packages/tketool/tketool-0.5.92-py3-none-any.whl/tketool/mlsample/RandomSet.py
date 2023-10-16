from tketool.mlsample.MemorySampleSource import Memory_NLSampleSource
import numpy as np


def create_SampleSet(set_name, input_size, count):
    NSet = Memory_NLSampleSource()

    NSet.create_new_set(set_name, "", [], ["t_input", "a_lable"], "", "")
    for _ in range(count):
        c_list = np.random.rand(input_size).tolist()
        c_result = 1 if np.random.randint(0, 10, 1) > 5 else 0
        NSet.add_row(set_name, [c_list, c_result])

    return NSet
