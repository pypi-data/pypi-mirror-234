import os
from tketool.logs import log


class ConfigManager:
    """
    A manager class to handle configurations.
    Reads configurations from a given file and provides access to these configurations.
    """

    def __init__(self, config_file_path):
        """
        Initialize the ConfigManager with the given configuration file path.
        If no path is provided, a default path 'config.jconfig' in the current working directory is used.

        :param config_file_path: Path to the configuration file.
        """
        self._config_map = {}

        self._config_file_path = config_file_path

        self._load_configs()

    def _load_configs(self):
        """
        Load configurations from the file into the config_map.
        """
        if os.path.exists(self._config_file_path):
            with open(self._config_file_path, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    key, sep, value = line.strip().partition('=')
                    if sep:  # ensure that '=' is present
                        self._config_map[self._sanitize_string(key)] = self._sanitize_string(value)
        else:
            with open(self._config_file_path, 'w') as f:
                f.writelines("")

    @staticmethod
    def _sanitize_string(s):
        """
        Remove starting and ending quotes from a string if they exist.

        :param s: Input string.
        :return: Sanitized string.
        """
        return s.strip('"').strip("'")

    def get_config(self, key, default_value=""):
        """
        Fetch the configuration for the provided key.
        If the key is not found, set it to the default value and return the default value.

        :param key: Key of the configuration.
        :param default_value: Default value to return/set if key is not found.
        :return: Value of the configuration.
        """
        if key in self._config_map:
            return self._config_map[key]

        log(f"No config key: {key}")
        with open(self._config_file_path, 'a') as f:
            f.writelines(f'{key}="{default_value}"\n')

        return default_value


_config_instance = {}


def get_config_instance(filename=None):
    """
    Get the singleton instance of ConfigManager.
    :filename: Path to the configuration file.
    :return: Instance of ConfigManager.
    """
    global _config_instance

    if not filename:
        filename = os.path.join(os.getcwd(), 'config.jconfig')

    if filename not in _config_instance:
        # if _config_instance is None:
        _config_instance[filename] = ConfigManager(filename)
        log(f"use config_file in {filename}")
    return _config_instance[filename]
