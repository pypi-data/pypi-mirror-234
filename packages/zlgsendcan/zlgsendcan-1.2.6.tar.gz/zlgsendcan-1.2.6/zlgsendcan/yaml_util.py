import os
import yaml


class YamlRead(object):
    def __init__(self, yaml_file):
        if os.path.exists(yaml_file):
            self.yaml_file = yaml_file
        else:
            raise FileNotFoundError("文件不存在")
        self._data = None
        self._data_all = None

    def read_data(self):
        """
        单个文档读取
        :return:
        """
        if not self._data:
            with open(self.yaml_file, "r", encoding='utf-8') as f:
                self._data = yaml.safe_load(f)
        return self._data

    def read_data_all(self):
        if not self._data_all:
            with open(self.yaml_file, "r", encoding='utf-8') as f:
                self._data_all = list(yaml.safe_load_all(f))
        return self._data_all

    def updata_yaml(self, old_data):
        # old_data = self.read_data()  # 读取文件数据
        # old_data['can初始化配置'][k] = v  # 修改读取的数据（k存在就修改对应值，k不存在就新增一组键值对）
        with open(self.yaml_file, "w", encoding="utf-8") as f:
            yaml.dump(old_data, f, allow_unicode=True)
