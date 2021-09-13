import os
from typing import Optional

import yaml
import PySimpleGUI as sg
from pandas import DataFrame


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
        with open(self.file_name, "r", encoding="utf-8") as yf:
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
    token: str = ""
    if os.path.exists(path):
        conf = yc.load()
        token = conf["token"]
    register_token: Optional[str] = sg.PopupGetText("Input the discord bot token", "Discord token", token)
    if register_token is None:
        exit()
    yc.write({"token": register_token})
    return register_token


def get_mute_uid(path):
    yc = YamlConfig(path)
    conf = yc.load()
    return conf["message"]["mute"]


def gen_code_block(df: DataFrame):
    lines = []
    for line in df.to_markdown(index=False).splitlines():
        lines.append(line[1:-1])
    msg = '\n'.join(lines)
    msg_lines = ["```", msg, "```"]
    return '\n'.join(msg_lines)


def get_server_ids(path):
    yc = YamlConfig(path)
    conf = yc.load()
    update = conf["voice_state"]["update"]
    return update["server_id"], update["text_ch_id"]
