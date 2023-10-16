from tketool.pyml.modulepluls import ModulePlus
from tketool.pyml.pytrainer import trainer_plugin_base, plugin_invoke_Enum
import os, pickle


class train_epoch_state_save(trainer_plugin_base):
    @property
    def Invoke_types(self) -> []:
        return [(plugin_invoke_Enum.Epoch_end, self.Invoke)]

    def Invoke(self, base_wall, epoch_wall, batch_wall):
        save_dict = {
            'epoch_uuid': epoch_wall['epoch_uuid'],
            'epoch_loss': epoch_wall['epoch_loss'],
            'start_time': epoch_wall['start_time'],
            'end_time': epoch_wall['end_time']
        }
        for a_key in self.addition_keys:
            if a_key in epoch_wall:
                save_dict[a_key] = epoch_wall[a_key]

        file_path = os.path.join(base_wall['model_folder'], self.save_file)
        with open(file_path, 'ab') as f:
            pickle.dump(save_dict, f)

    def __init__(self, addition_keys=[], save_file='train_data.pkl'):
        self.addition_keys = addition_keys
        self.save_file = save_file
