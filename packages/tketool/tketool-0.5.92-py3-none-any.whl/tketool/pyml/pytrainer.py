from enum import Enum
import torch
from tketool.pyml.modulepluls import ModulePlus
from tketool.mlsample.SampleSet import SampleSet
from tketool.utils.progressbar import process_status_bar
from tketool.files import create_folder_if_not_exists
import abc, time, pickle, os


class plugin_invoke_Enum(Enum):
    Epoch_begin = 1
    Epoch_end = 2
    Batch_begin = 3
    Batch_end = 4
    Begin = 5
    End = 6
    After_Backward = 7


class update_mode_enum(Enum):
    Per_Batch = 1,
    Per_Epoch = 2


class trainer_plugin_base(metaclass=abc.ABCMeta):

    @property
    @abc.abstractmethod
    def Invoke_types(self) -> []:
        pass

    @abc.abstractmethod
    def Invoke(self, base_wall, epoch_wall, batch_wall):
        pass


class pymodel_trainer():
    def __init__(self, model: ModulePlus, loss_obj, optimizer, update_mode=update_mode_enum.Per_Batch,
                 output_folder='model', plugins=[]):
        self.model = model
        self.loss = loss_obj
        self.optimizer = optimizer
        self.out_folder = output_folder
        self.update_mode = update_mode
        create_folder_if_not_exists(self.out_folder)
        create_folder_if_not_exists(self.out_folder, 'saved_model')

        self.plugin = {}
        for pl in plugins:
            for ty, fun in pl.Invoke_types:
                if ty not in self.plugin:
                    self.plugin[ty] = []
                self.plugin[ty].append(fun)

        self.model = self.model.try_to_device(self.model)
        self.loss = self.model.try_to_device(self.loss)

    def _invoke_plugin(self, plugin_enum, base_wall, epoch_wall, batch_wall):
        if plugin_enum not in self.plugin:
            return

        for pl in self.plugin[plugin_enum]:
            pl(base_wall, epoch_wall, batch_wall)

    def train(self,
              dataset: SampleSet,
              epoch=1000,
              input_convert_func=lambda x: x,
              label_convert_func=lambda x: x
              ):

        pb = process_status_bar()
        self.model.train()

        base_wall = {
            'model': self.model,
            'loss': self.loss,
            'optimizer': self.optimizer,
            'model_folder': self.out_folder,
            'input_convert_func': input_convert_func,
            'label_convert_func': label_convert_func,
            'epoch_count': epoch,
            'train_set': dataset,
            'update_mode': self.update_mode,
            'pb': pb,
            "logs_stack": [],
            "parameter_update_times": 0,
        }

        self._invoke_plugin(plugin_invoke_Enum.Begin, base_wall, None, None)

        for epoch in pb.iter_bar(range(epoch), key='epoch'):

            epoch_uuid = int(time.time() * 10)

            epoch_wall = {
                'current_epoch_idx': epoch,
                'epoch_uuid': epoch_uuid,
                'epoch_loss': 0,
                'start_time': time.time(),
                'batch_count': base_wall['train_set'].count()
            }

            self._invoke_plugin(plugin_invoke_Enum.Epoch_begin, base_wall, epoch_wall, None)

            if base_wall['update_mode'] == update_mode_enum.Per_Epoch:
                base_wall['optimizer'].zero_grad()

            batch_dataset = base_wall['train_set']
            for idx, item in pb.iter_bar(enumerate(batch_dataset), key='batch', max=batch_dataset.count()):
                batch_wall = {
                    "batch_idx": idx,
                    "ori_Item": item,
                    "start_time": time.time(),
                    "Convert_x": base_wall['input_convert_func'](item),
                    "Convert_y": base_wall['label_convert_func'](item)
                }

                self._invoke_plugin(plugin_invoke_Enum.Batch_begin, base_wall, epoch_wall, batch_wall)

                # optimizer = base_wall['optimizer']
                # model = base_wall['model']
                # loss = base_wall['loss']

                batch_X = batch_wall['Convert_x']
                batch_Y = batch_wall['Convert_y']

                batch_X = self.model.try_to_device(batch_X)
                batch_Y = self.model.try_to_device(batch_Y)

                if base_wall['update_mode'] == update_mode_enum.Per_Batch:
                    base_wall['optimizer'].zero_grad()

                # logit= model(batch_x)
                batch_wall['logit'] = base_wall['model'](batch_X)

                # loss_tensor=loss(logit, batch_Y)
                batch_wall['loss_tensor'] = base_wall['loss'](batch_wall['logit'], batch_Y)

                # loss_value= loss_tensor.item()
                batch_wall['loss_value'] = batch_wall['loss_tensor'].item()
                epoch_wall['epoch_loss'] += batch_wall['loss_value']
                batch_wall['end_time'] = time.time()

                batch_wall['loss_tensor'].backward()
                self._invoke_plugin(plugin_invoke_Enum.After_Backward, base_wall, epoch_wall, batch_wall)

                if base_wall['update_mode'] == update_mode_enum.Per_Batch:
                    base_wall['optimizer'].step()
                    base_wall["parameter_update_times"] += 1

                self._invoke_plugin(plugin_invoke_Enum.Batch_end, base_wall, epoch_wall, batch_wall)

            if base_wall['update_mode'] == update_mode_enum.Per_Epoch:
                base_wall['optimizer'].step()
                base_wall["parameter_update_times"] += 1

            epoch_wall['end_time'] = time.time()

            self._invoke_plugin(plugin_invoke_Enum.Epoch_end, base_wall, epoch_wall, None)

        self._invoke_plugin(plugin_invoke_Enum.End, base_wall, None, None)
