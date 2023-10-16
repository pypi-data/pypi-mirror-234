import numpy as np
from sklearn.metrics import classification_report

from tketool.pyml.pytrainer import trainer_plugin_base, plugin_invoke_Enum
from tketool.mlsample.SampleSet import SampleSet
from tketool.pyml.modulepluls import ModulePlus
from tketool.utils.progressbar import process_status_bar
import torch
from sklearn.metrics import accuracy_score


class multiclass_evaluate_plugin(trainer_plugin_base):

    def __init__(self, dataset: SampleSet, per_epoch=1):
        self.buffer_data = None
        self._dataset = dataset
        self._per_epoch = per_epoch

    @property
    def Invoke_types(self) -> []:
        return [(plugin_invoke_Enum.Epoch_end, self.Invoke)]

    def Invoke(self, base_wall, epoch_wall, batch_wall):

        epoch_count = epoch_wall['current_epoch_idx']

        if epoch_count % self._per_epoch != 0:
            return

        model = base_wall['model']
        pt = base_wall['pb']

        all_output = []
        all_label = []

        with torch.no_grad():
            model.eval()  # 使用

            if self.buffer_data is None:
                pt.start('buffer evaluation data', max=self._dataset.count())
                buffer_data = []
                for item in self._dataset:
                    batch_X = base_wall['input_convert_func'](item)
                    batch_Y = base_wall['label_convert_func'](item)
                    buffer_data.append((batch_X, batch_Y))
                    pt.one_done()
                pt.stop_current()

            for batch_X, batch_Y in pt.iter_bar(buffer_data, key='evaluation'):
                batch_X = model.try_to_device(batch_X)

                outputs = model(batch_X)

                outputs = outputs.cpu().detach().numpy()
                batch_Y = batch_Y.cpu().detach().numpy()
                all_output.append(outputs)
                all_label.append(batch_Y)

        all_output = np.concatenate(tuple(all_output))
        all_label = np.concatenate(tuple(all_label))

        # 将模型的输出通过softmax函数转换为概率分布，然后取得最大概率对应的类别标签
        predictions = np.argmax(torch.from_numpy(all_output).softmax(dim=1).numpy(), axis=1)

        accuracy = accuracy_score(all_label, predictions)

        if "evaluations" not in epoch_wall:
            epoch_wall['evaluations'] = {}

        epoch_wall['evaluations']['accuracy'] = accuracy

        # Generate a classification report
        # classificationReport = classification_report(all_label, predictions, output_dict=True,
        #                                              zero_division=0)
        #base_wall['logs_stack'].append(classificationReport)

        base_wall['logs_stack'].append(
            f"Evalution: acc:{accuracy:.4f}")

        model.train()
