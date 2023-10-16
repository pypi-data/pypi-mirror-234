from tketool.pyml.pytrainer import trainer_plugin_base, plugin_invoke_Enum
import pickle, os, threading
from flask import Flask, send_from_directory, send_file, url_for, redirect
import logging
from jinja2 import Environment, FileSystemLoader, PackageLoader


class dashboard_plugin(trainer_plugin_base):
    @property
    def Invoke_types(self) -> []:
        return [(plugin_invoke_Enum.Begin, self.start),
                (plugin_invoke_Enum.Epoch_end, self.epoch_end),
                ]

    def __init__(self, port=None):
        self.epoch_data = []
        self.port = port

    def start(self, base_wall, epoch_wall, batch_wall):
        # load data from file to self.epoch_data
        path = os.path.join(base_wall["model_folder"], 'epoch_data.pkl')
        try:
            with open(path, 'rb') as f:
                while True:
                    try:
                        self.epoch_data.append(pickle.load(f))
                    except EOFError:
                        break  # No more data in the file
        except FileNotFoundError:
            pass  # It's okay if the file doesn't exist

        if self.port is not None:
            self.start_flask_server(base_wall)

    def epoch_end(self, base_wall, epoch_wall, batch_wall):
        all_evaluations_dic = epoch_wall.get("evaluations", {})
        epoch_loss = epoch_wall['epoch_loss']
        all_keys = {k: v for k, v in all_evaluations_dic.items()}
        model_info = {
            "epoch_count": base_wall['epoch_count'],
            "set_name": base_wall['train_set'].set_name,
            "model_folder": base_wall['model_folder'],
            "train_epoch": len(self.epoch_data),
            "parameter_update_times": base_wall['parameter_update_times'],
        }

        if "Best_model_state" in base_wall:
            for k, v in base_wall["Best_model_state"].items():
                model_info["Best_State_For_" + k] = v

        epoch_data = (epoch_loss, all_keys)
        self.epoch_data.append(epoch_data)

        # 通过追加的方式更新文件
        # Append new epoch data to file
        path = os.path.join(base_wall["model_folder"], 'epoch_data.pkl')
        with open(path, 'ab') as f:
            pickle.dump(epoch_data, f)

        env = Environment(loader=PackageLoader('tketool.pyml', 'trainerplugins'))
        # env = Environment(loader=FileSystemLoader('pyml/trainerplugins/'))
        template = env.get_template("webreport_temp.html")

        # Separate epoch data into different lists for plotting
        epoch_loss_index = list(range(len([data[0] for data in self.epoch_data])))
        epoch_loss = [data[0] for data in self.epoch_data]
        all_keys_data = {key: [] for key in self.epoch_data[0][1].keys()}
        for _, keys in self.epoch_data:
            for key, value in keys.items():
                all_keys_data[key].append(value)

        template_vars = {"model_info": model_info,
                         "epoch_index": epoch_loss_index,
                         "epoch_loss": epoch_loss,
                         "all_keys": all_keys_data,
                         "all_keys_data_length": max([len(v) for v in all_keys_data.values()])}

        wpath = os.path.join(base_wall["model_folder"], 'web_report.html')
        with open(wpath, 'w') as f:
            f.write(template.render(template_vars))

    def start_flask_server(self, base_wall):
        app = Flask(__name__, static_folder=os.path.join(os.getcwd(), base_wall["model_folder"]))

        app.logger.setLevel(logging.ERROR)
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)

        @app.route('/')
        def serve_dashboard():
            return redirect(url_for('static', filename='web_report.html'))

        thread = threading.Thread(target=app.run, kwargs={'port': self.port, 'host': '0.0.0.0'})
        thread.start()

    def Invoke(self, base_wall, epoch_wall, batch_wall):
        pass
