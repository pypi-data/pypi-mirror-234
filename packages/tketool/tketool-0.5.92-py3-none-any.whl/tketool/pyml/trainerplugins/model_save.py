from tketool.pyml.modulepluls import ModulePlus
from tketool.logs import convert_print_color, log_color_enum
from tketool.pyml.pytrainer import trainer_plugin_base, plugin_invoke_Enum
from enum import Enum
from tketool.files import create_folder_if_not_exists
import os, pickle, torch


class model_preload_Enum(Enum):
    NoLoad = 1
    Load_latest = 2


class model_save(trainer_plugin_base):
    def __init__(self, pre_load: model_preload_Enum, save_per_epoch=1, max_saved_count=5, save_folder='saved_model'):
        self.pre_load = pre_load
        self.save_per_epoch = save_per_epoch
        # self.save_per_batch = save_per_batch
        self.save_folder = save_folder
        self.max_saved_count = max_saved_count
        self.saved_models = []

    @property
    def Invoke_types(self) -> []:
        return [(plugin_invoke_Enum.Begin, self.BeginInvoke),
                (plugin_invoke_Enum.Epoch_end, self.EpochInvoke),
                ]

    def BeginInvoke(self, base_wall, epoch_wall, batch_wall):
        create_folder_if_not_exists(base_wall["model_folder"], self.save_folder)

        # 获取所有保存的模型文件
        self.saved_models = os.listdir(os.path.join(base_wall["model_folder"], self.save_folder))
        # 按创建时间排序，获取最后一个模型文件
        self.saved_models.sort(key=lambda x: x)

        if self.pre_load == model_preload_Enum.NoLoad:
            base_wall['logs_stack'].append(f" 从随机参数开始训练,没有加载任何模型参数.")
            return

        if self.pre_load == model_preload_Enum.Load_latest:
            if len(self.saved_models) == 0:
                return

            last_model_file = self.saved_models[-1]
            # 加载模型参数
            result = base_wall["model"].load_state_dict(
                torch.load(os.path.join(base_wall["model_folder"], self.save_folder, last_model_file)))
            base_wall['logs_stack'].append(f"加载最后一次训练的模型参数：{last_model_file}, {result}")

    def EpochInvoke(self, base_wall, epoch_wall, batch_wall):
        epoch_count = epoch_wall['current_epoch_idx']
        if epoch_count % self.save_per_epoch != 0:
            return

        save_path = os.path.join(base_wall["model_folder"], self.save_folder, str(epoch_wall['epoch_uuid']))
        torch.save(base_wall["model"].state_dict(), save_path)
        self.saved_models.append(str(epoch_wall['epoch_uuid']))
        base_wall['logs_stack'].append(f" Model save: {save_path}")

        while len(self.saved_models) > self.max_saved_count:
            file_path = os.path.join(base_wall["model_folder"], self.save_folder, self.saved_models[0])
            os.remove(file_path)
            self.saved_models = self.saved_models[1:]

    def Invoke(self, base_wall, epoch_wall, batch_wall):
        pass


class model_save_by_best_metric(trainer_plugin_base):
    def Invoke(self, base_wall, epoch_wall, batch_wall):
        pass

    def __init__(self, load_best_metrics_name=None, save_folder='saved_best_model'):
        self.save_folder = save_folder
        self.load_best_name = load_best_metrics_name
        # Initialize best metrics as None for maximization and Inf for minimization problem
        self.best_metrics = {}

    @property
    def Invoke_types(self) -> []:
        return [(plugin_invoke_Enum.Begin, self.BeginInvoke),
                (plugin_invoke_Enum.Epoch_end, self.EpochInvoke),
                ]

    def BeginInvoke(self, base_wall, epoch_wall, batch_wall):
        create_folder_if_not_exists(base_wall["model_folder"], self.save_folder)
        # Load previous best metrics if exists
        try:
            with open(os.path.join(base_wall["model_folder"], self.save_folder, "best_metrics.txt"), 'r') as f:
                for line in f:
                    metric, uuid, value = line.strip().split()
                    self.best_metrics[metric] = {'value': float(value), 'uuid': uuid}

            if self.load_best_name is not None and self.load_best_name in self.best_metrics:
                last_model_file = self.best_metrics[self.load_best_name]['uuid']
                # 加载模型参数
                result = base_wall["model"].load_state_dict(
                    torch.load(os.path.join(base_wall["model_folder"], self.save_folder, last_model_file)))
                base_wall['logs_stack'].append(
                    f"加载最佳{self.load_best_name}模型参数(v={self.best_metrics[self.load_best_name]['value']})：{last_model_file}, {result}")

        except FileNotFoundError:
            pass

    def EpochInvoke(self, base_wall, epoch_wall, batch_wall):
        evaluations = {}
        if 'evaluations' in epoch_wall:
            evaluations.update(epoch_wall['evaluations'])
        if 'epoch_loss' in epoch_wall:
            evaluations['epoch_loss'] = epoch_wall['epoch_loss']

        for metric, current_value in evaluations.items():
            if current_value is not None and (metric not in self.best_metrics or
                                              (metric == 'epoch_loss' and current_value < self.best_metrics[metric][
                                                  'value']) or
                                              (metric != 'epoch_loss' and current_value > self.best_metrics[metric][
                                                  'value'])):
                save_path = os.path.join(base_wall["model_folder"], self.save_folder, str(epoch_wall['epoch_uuid']))

                # Remove old model file
                if metric in self.best_metrics and 'uuid' in self.best_metrics[metric]:
                    old_model_path = os.path.join(base_wall["model_folder"], self.save_folder,
                                                  str(self.best_metrics[metric]['uuid']))
                    # 判断要删除的指标是否为其他指标的最优质
                    has_other_link = False
                    for k, v in self.best_metrics.items():
                        if k != metric and v['uuid'] == self.best_metrics[metric]['uuid']:
                            has_other_link = True
                            break

                    if has_other_link is False and os.path.exists(old_model_path):
                        os.remove(old_model_path)

                torch.save(base_wall["model"].state_dict(), save_path)

                self.best_metrics[metric] = {'uuid': epoch_wall['epoch_uuid'], 'value': current_value}

                base_wall['logs_stack'].append(convert_print_color((
                    f"New best model saved: {save_path} for metric {metric}: {current_value: .4f}",
                    log_color_enum.GREEN)))

        if "Best_model_state" not in base_wall:
            base_wall['Best_model_state'] = {}

        # Save best metrics to a file after each epoch
        with open(os.path.join(base_wall["model_folder"], self.save_folder, "best_metrics.txt"), 'w') as f:
            for metric, metric_info in self.best_metrics.items():
                f.write(f"{metric} {metric_info['uuid']} {metric_info['value']}\n")
                base_wall['Best_model_state'][metric] = f"{metric_info['value']:.4f} ({metric_info['uuid']})"
