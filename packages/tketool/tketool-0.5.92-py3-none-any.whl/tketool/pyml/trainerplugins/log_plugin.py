from tketool.pyml.modulepluls import ModulePlus
from tketool.pyml.pytrainer import trainer_plugin_base, plugin_invoke_Enum
import os, pickle


class log_plugin(trainer_plugin_base):
    def Invoke(self, base_wall, epoch_wall, batch_wall):
        pass

    @property
    def Invoke_types(self) -> []:
        return [
            (plugin_invoke_Enum.Begin, self.start),
            (plugin_invoke_Enum.End, self.end),
            (plugin_invoke_Enum.Epoch_begin, self.epoch_begin),
            (plugin_invoke_Enum.Epoch_end, self.epoch_end),
            (plugin_invoke_Enum.Batch_begin, self.batch_begin),
            (plugin_invoke_Enum.Batch_end, self.batch_end),
        ]

    def _log(self, pb, content):
        pb.print_log(content)
        # 打开文件，如果文件不存在，则创建
        with open(self.save_file, "a") as log_file:  # 'a' 表示 append mode，即增量方式
            log_file.write(content + "\n")

    def _log_stackcontent(self, base_wall):
        if "logs_stack" in base_wall:
            pb = base_wall["pb"]
            for message in base_wall['logs_stack']:
                self._log(pb, message)
            base_wall['logs_stack'].clear()

    def start(self, base_wall, epoch_wall, batch_wall):
        self.save_file = os.path.join(base_wall["model_folder"], "log.txt")

    def end(self, base_wall, epoch_wall, batch_wall):
        self._log_stackcontent(base_wall)

    def epoch_begin(self, base_wall, epoch_wall, batch_wall):
        self._log_stackcontent(base_wall)

    def epoch_end(self, base_wall, epoch_wall, batch_wall):
        pb = base_wall["pb"]
        epoch = epoch_wall['current_epoch_idx']
        epoch_uuid = epoch_wall['epoch_uuid']
        loss = epoch_wall['epoch_loss']
        self._log(pb, f"Epoch [{epoch + 1}({epoch_uuid})], Total Loss: {loss:.4f}")
        self._log_stackcontent(base_wall)

    def batch_begin(self, base_wall, epoch_wall, batch_wall):
        self._log_stackcontent(base_wall)

    def batch_end(self, base_wall, epoch_wall, batch_wall):
        self._log_stackcontent(base_wall)

    def __init__(self, save_file=None):
        self.save_file = save_file
