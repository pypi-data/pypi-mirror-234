import json_convenience as jsonx
from pathlib import Path
from typing import Any


Setting = jsonx.Property


class Settings(object):
    """
    represents a json file containing settings
    """
    def __init__(self, file: Path):
        """
        initialize a Settings object

        :param file: the path to the json file
        """
        if not file.exists():
            raise FileNotFoundError(f"{file} doesn't exist")
        elif not file.is_file() or not file.suffix == ".json":
            raise FileNotFoundError(f"{file} is no .json file")
        self.__dict__["_all_keys"] = tuple(jsonx.read_json_file(file_path=file).keys())
        self.__dict__["_file"] = file

    def __getattr__(self, name: str) -> Setting:
        if name not in self.__dict__:
            self.__dict__[name] = jsonx.get_property(file_path=self._file, keys=(name, ))
        return self.__dict__[name]

    def __setattr__(self, name: str, value: Any) -> None:
        if name not in self._all_keys:
            if name not in self.__dict__.keys():
                raise AttributeError(f"'{self.__class__}' object has no setting or attribute '{name}'")
            else:
                self.__dict__[name] = value
            return
        if not isinstance(value, Setting):
            raise jsonx.NotAPropertyError(no_property_object=value)
        self.__dict__[name] = value

    def get(self, name: str) -> Setting:
        """
        get a setting

        :param name: the name of the setting
        :return: the value of the setting
        """
        return self.__getattr__(name=name)

    def set(self, name: str, value: Any):
        """
        set the value of a setting

        :param name: the name of the setting
        :param value: the new value of the setting
        :return:
        """
        self.__setattr__(name=name, value=value)

    def save(self) -> int:
        """
        save the settings to the json file

        :return: the number of saved settings (settings that were not changed excluded)
        """
        counter = 0
        for name in self.__dict__:
            if jsonx.contains_property(file_path=self._file, keys=(name, )):
                file_property = jsonx.get_property(file_path=self._file, keys=(name, ))
                if not file_property == self.__dict__[name]:
                    jsonx.set_property(file_path=self._file, keys=(name, ), value=self.__dict__[name])
                    counter += 1
        return counter
