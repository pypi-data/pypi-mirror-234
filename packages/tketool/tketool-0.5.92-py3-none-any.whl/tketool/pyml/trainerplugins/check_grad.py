from tketool.pyml.modulepluls import ModulePlus
from tketool.files import create_folder_if_not_exists
from tketool.pyml.pytrainer import trainer_plugin_base, plugin_invoke_Enum
import os, pickle, torch


class check_grad(trainer_plugin_base):
    @property
    def Invoke_types(self) -> []:
        return [
            (plugin_invoke_Enum.After_Backward, self.Invoke),
            (plugin_invoke_Enum.Begin, self.begin),
        ]

    def begin(self, base_wall, epoch_wall, batch_wall):
        create_folder_if_not_exists(base_wall["model_folder"], self.report_folder)

    def write_grad_info_to_txt(self, filename):
        with open(filename, 'w') as f:
            for name, grad_info in self.grad_info_set.items():
                # 写入第一行：name、count、shape和所有title
                first_line = [name, str(grad_info['count']), str(grad_info['shape'])] + grad_info['title']
                f.write('\t'.join(first_line) + '\n')

                # 转换mean为字符串并写入第二行
                second_line_means = list(map(str, grad_info['mean']))
                f.write('\t'.join(second_line_means) + '\n')

                # 转换var为字符串并写入第三行
                third_line_vars = list(map(str, grad_info['var']))
                f.write('\t'.join(third_line_vars) + '\n')

                # 添加空行作为不同name之间的分隔符
                f.write('\n')

    def Invoke(self, base_wall, epoch_wall, batch_wall):
        model = base_wall['model']
        epoch_id = epoch_wall['current_epoch_idx']
        batch_id = batch_wall['batch_idx']
        current_update_mean = []
        current_update_var = []
        for name, param in model.named_parameters():
            if param.grad is not None:
                grad_data = param.grad.data

                # Shape = grad_data.shape
                # Numberelements = torch.numel(grad_data).item()
                Mean = torch.mean(grad_data).item()
                Variance = torch.var(grad_data).item()

                # if name not in self.grad_info_set:
                # self.grad_info_set[name] = {
                #     'shape': Shape,
                #     'count': Numberelements,
                #     'mean': [],
                #     'var': [],
                #     'title': []
                # }
                current_update_var.append(Variance)
                current_update_mean.append(Mean)

                # self.grad_info_set[name]['var'].append(Variance.item())
                # self.grad_info_set[name]['mean'].append(Mean.item())
                # self.grad_info_set[name]['title'].append(f"{epoch_id}_{batch_id}")
        base_wall['logs_stack'].append(f"梯度跟踪： mean{sum(current_update_mean) / len(current_update_mean)}, "
                                       f" avg {sum(current_update_var) / len(current_update_var)} ")
        # self.write_grad_info_to_txt(os.path.join(base_wall["model_folder"], self.report_folder, "report.txt"))

    def __init__(self, grad_report_folder="grad_report"):
        self.report_folder = grad_report_folder
        # self.grad_info_set = {}
