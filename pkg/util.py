import os

import yaml
import PySimpleGUI as sg

def mkdir(dir_path):
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)


class YamlConfig:
    def __init__(self, file_name="./settings/config.yaml"):
        self.file_name = file_name
    
    def load(self) -> dict:
        """
        yamlファイルを読み辞書形式で結果を返す
        :return: yamlファイルのデータ構造（辞書）
        """
        with open(self.file_name, "r") as yf:
            return yaml.load(yf, Loader=yaml.FullLoader)
    
    def write(self, data: dict) -> None:
        """
        yamlを書き出す
        :param data: yamlで出力するデータをまとめた辞書
        """
        with open(self.file_name, "w") as yf:
            yaml.dump(data, yf, default_flow_style=False)


def get_token(path):
    yc = YamlConfig(path)
    if not os.path.exists(path):
        regist_token = sg. PopupGetText("Input the discord bot token")
        if regist_token is None:
            exit()
        yc.write({"token": regist_token})
    res = yc.load()
    return res["token"]
    