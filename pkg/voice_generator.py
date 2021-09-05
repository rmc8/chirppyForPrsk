import os
import re

import pyttsx3


def rm_custom_emoji(text):
    """
    絵文字IDは読み上げないようにする
    :param text: オリジナルのテキスト
    :return: 絵文字IDを除去したテキスト
    """
    pattern = r'<:[a-zA-Z0-9_]+?>'
    return re.sub(pattern, '', text)


def omit_url(text):
    """
    URLを省略する
    :param text: オリジナルのテキスト
    :return: URLの省略したテキスト
    """
    pattern = r'https?://[\w/:%#\$&\?\(\)~\.=\+\-]+'
    return re.sub(pattern, 'URL省略', text)  # 置換処理


def rm_picture(text):
    """
    画像の読み上げを止める
    :param text: オリジナルのテキスト
    :return: 画像の読み上げを省略したテキスト
    """
    pattern = r'.*(\.jpg|\.jpeg|\.gif|\.png|\.bmp)'
    return re.sub(pattern, '', text)  # 置換処理


def rm_command(text):
    """
    コマンドの読み上げを止める
    :param text: オリジナルのテキスト
    :return: コマンドを省略したテキスト
    """
    return re.sub(r'^(!|\?|$).*', '', text)  # 置換処理


def rm_log(text):
    """
    参加ログを除去する
    :param text: オリジナルのテキスト
    :return: 参加ログを除去したテキスト
    """
    pattern = r'(\【VC参加ログ\】.*)'
    return re.sub(pattern, '', text)  # 置換処理


def user_custom(text):
    """
    辞書のデータを読み上げる
    :param text:
    :return:
    """
    user_dict: str = f'{os.getcwd()}/dict/dict.csv'
    if not os.path.exists(user_dict):
        return text

    with open(user_dict, 'r', encoding='utf-8') as f:
        lines = f.readline()
        lines = [ln for ln in lines if "," in ln]
        for line in lines:
            pattern = line.strip().split(',')
            if pattern[0] in text:
                text = text.replace(pattern[0], pattern[1])
                print('置換後のtext:' + text)
    return text


def gen_mp3(text, path):
    engine = pyttsx3.init()
    rate = engine.getProperty('rate')
    engine.setProperty(rate, 150)
    engine.save_to_file(text, path)
    engine.runAndWait()


def create_wav(input_text, output_path):
    """
    message.contentをテキストファイルと音声ファイルに書き込む
    :param input_text:
    :return:
    """
    # message.contentをテキストファイルに書き込み
    fxs = (rm_command, omit_url,
           rm_picture, rm_log, user_custom, rm_custom_emoji)
    for fx in fxs:
        input_text = fx(input_text)  # 絵文字IDは読み上げない
    gen_mp3(input_text, output_path)


if __name__ == '__main__':
    from util import mkdir

    mkdir('./dict/')
    mkdir('./output/')
    create_wav('テスト', '../output/output.mp3')
