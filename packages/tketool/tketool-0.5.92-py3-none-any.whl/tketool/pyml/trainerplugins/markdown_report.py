# from tketool.pyml.modulepluls import ModulePlus
# from tketool.pyml.pytrainer import trainer_plugin_base, plugin_invoke_Enum
# from tketool.utils.progressbar import process_status_bar
# import matplotlib.pyplot as plt
# import seaborn as sns
# import pandas as pd
# from tabulate import tabulate
# from time import strftime, gmtime
# import numpy as np
# import os, pickle
#
#
# class markdown_report(trainer_plugin_base):
#     @property
#     def Invoke_types(self) -> [plugin_invoke_Enum]:
#         return [plugin_invoke_Enum.Epoch_end]
#
#     def Invoke(self, dashboard: dict, model: ModulePlus, pt: process_status_bar, out_folder: str):
#         def get_module_info(module):
#             # 获取模型的层数和参数数量
#             num_layers = len(list(module.children()))
#             num_params = sum(p.numel() for p in module.parameters())
#             return num_layers, num_params
#
#         # 从文件中加载所有训练数据
#         train_data = []
#         if os.path.exists(os.path.join(out_folder, 'train_data.pkl')):
#             with open(os.path.join(out_folder, 'train_data.pkl'), 'rb') as f:
#                 while True:
#                     try:
#                         train_data.append(pickle.load(f))
#                     except EOFError:
#                         break
#         train_data.append(dashboard)
#
#         # 准备数据
#         epoch_data = []
#         for i, state in enumerate(train_data):
#             training_duration = strftime("%H:%M:%S", gmtime(state['end_time'] - state['start_time']))
#             epoch_data.append(
#                 [i + 1, state['epoch_uuid'], round(state['epoch_loss'], 2), len(state['batch_losses']),
#                  training_duration])
#
#         # 获取模型信息
#         num_layers, num_params = get_module_info(model)
#         #
#         report_content = []
#         report_content.append("# Model Training Report")
#         report_content.append("\n## Basic Information")
#         # report_content.append(f"Model Name: {model.name}")
#         report_content.append(f"Number of Layers: {num_layers}")
#         report_content.append(f"Number of Parameters: {num_params}")
#         report_content.append("\n## Epoch Information")
#
#         # 创建表格
#         report_content.append(
#             tabulate(epoch_data[-10:],
#                      headers=['Epoch', 'UUID', 'Epoch Loss', 'Number of Batches', 'Training Duration'],
#                      tablefmt='pipe'))
#
#         # 创建 DataFrame 用于绘制损失变化图
#         loss_data = [(i + 1, state['epoch_loss']) for i, state in enumerate(train_data)]
#         df = pd.DataFrame(loss_data, columns=['Epoch', 'Batch Loss'])
#
#         # 打印最后10个 epochs
#         # print(df.tail(10))
#
#         # 使用 seaborn 绘制损失变化图表
#         plt.figure(figsize=(10, 6))
#         sns.lineplot(x='Epoch', y='Batch Loss', data=df)
#         plt.title('Model Loss Over Batches')
#         plt.xticks(np.arange(1, len(train_data) + 1, step=1))  # 设置x轴为整数
#         plt.ylim([0, max(df['Batch Loss']) * 1.5])
#         plt.savefig(os.path.join(out_folder, 'loss_curve.png'))
#         plt.close()
#
#         # 将图片添加进报告
#         report_content.append("\n![Loss Curve](loss_curve.png)")
#
#         evaluation_keys = train_data[0]['evaluations'].keys()
#
#         for key in evaluation_keys:
#             # 创建 DataFrame 用于每个评估指标的变化图
#             eval_data = [(i + 1, state['evaluations'][key]) for i, state in enumerate(train_data)]
#             df_eval = pd.DataFrame(eval_data, columns=['Epoch', key])
#
#             # 指标变化图
#             plt.figure(figsize=(10, 6))
#             sns.lineplot(x='Epoch', y=key, data=df_eval)
#             plt.title(f'{key} Change Over Batches')
#             plt.xticks(np.arange(1, len(train_data) + 1, step=1))  # 设置x轴为整数
#             plt.ylim([0, max(df_eval[key]) * 1.5] if max(df_eval[key]) != 0 else 1)
#             img_name = f'{key}_curve.png'
#             plt.savefig(os.path.join(out_folder, img_name))
#             plt.close()
#
#             # 将图片添加进报告
#             report_content.append(f"\n![{key} Curve]({img_name})")
#
#         # 保存 markdown 报告
#         with open(os.path.join(out_folder, 'training_report.md'), 'w') as f:
#             f.write('\n'.join(report_content))
#
# # test = markdown_report()
# # test.Invoke({}, None, None, "/Users/jiangke/Code/qagpt/source/common/sample_data")
