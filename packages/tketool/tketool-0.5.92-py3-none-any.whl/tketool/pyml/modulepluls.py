import torch
from tketool.JConfig import get_config_instance
from tketool.logs import log


class ModulePlus(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.config_obj = get_config_instance()
        self.check_drive()

    def check_drive(self):
        self.is_cuda_available = torch.cuda.is_available()
        self.cuda_count = torch.cuda.device_count()
        self.is_mps_available = torch.backends.mps.is_available()

        if self.is_mps_available:
            self.act_drive = "mps"
        if self.is_cuda_available:
            self.act_drive = "cuda:0"

        config_drive = self.config_obj.get_config('run_drive')
        if config_drive is not None:
            self.act_drive = config_drive

        log(f"ENV: CUDA:{self.is_cuda_available}[{self.cuda_count}], mps:{self.is_mps_available}")
        log(f"ACT: {self.act_drive}")

    def try_to_device(self, item):
        if isinstance(item, torch.Tensor) or isinstance(item, torch.nn.Module):
            return item.to(self.act_drive)
        else:
            return item

    def load_parameters(self, path):
        self.load_state_dict(torch.load(path, map_location=torch.device(self.act_drive)))
