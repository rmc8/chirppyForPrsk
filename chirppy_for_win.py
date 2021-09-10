import os
import time
import traceback
import warnings
from glob import glob
from datetime import datetime
from typing import Optional, Union

import discord
from pandas import DataFrame, merge
from discord.ext import commands

from pkg.util import mkdir, get_token, gen_code_block
from pkg.voice_generator import create_mp3
from pkg.prsk import PSEKAI

client = commands.Bot(command_prefix='.')
voice_client = None
warnings.simplefilter("ignore")


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.command()
async def join(ctx):
    print('#join')
    print('#voicechannelを取得')
    vc = ctx.author.voice.channel
    print('#voicechannelに接続')
    await vc.connect()


@client.command()
async def bye(ctx):
    print('#bye')
    print('#切断')
    await ctx.voice_client.disconnect()


@client.command()
async def register(ctx, arg1, arg2):
    with open('./dict/dict.csv', mode='a', encoding='utf-8') as f:
        f.write(f'{arg1},{arg2}\n')
        print(f'dic.txtに書き込み：\n{arg1}, {arg2}')
    await ctx.send(f'`{arg1}`を`{arg2}`として登録しました')


@client.command()
async def eventid(ctx):
    ps = PSEKAI()
    df: DataFrame = ps.get_event_name()
    msg = gen_code_block(df)
    await ctx.send(msg)


@client.command()
async def border(ctx, event_id=None, top_num=None):
    ps = PSEKAI()
    if event_id is None or top_num is None:
        msg = 'event_idやtop_numが空です。`.border 22 1000`のように値を設定してください。'
        await ctx.send(msg)
        return
    res: Union[str, DataFrame] = ps.get_border(event_id, top_num)
    if type(res) is not str:
        rec = res.to_dict(orient="records")[-1]
        key = f"TOP{top_num}"
        res = f"`{rec['eventName']}` > `{rec['datetime']}` > `TOP{top_num}` > `{rec[key]:,} P`"
    await ctx.send(res)


@client.command()
async def bsummary(ctx, event_id=None, limit=10000):
    if event_id is None:
        await ctx.send('取得対象のevent_idを`.bsummary 31`のように設定してください。')
        return
    ps = PSEKAI()
    await ctx.send('ボーダーの取得を開始します。')
    df: DataFrame = DataFrame()
    rank_list = ps.get_tar_rank(limit)
    for rank in rank_list:
        print(f"Get the TOP{rank} border")
        cdf: Union[DataFrame, str] = ps.get_border(event_id, str(rank))
        if type(cdf) is str:
            print(cdf)
            await ctx.send(cdf)
            return
        time.sleep(1)
        if df.empty:
            df = cdf
            continue
        df = merge(df, cdf, on="datetime")
    rec = df.to_dict(orient="records")[-1]
    msg_lines = [
        '```',
        f"{rec['eventName']} - {rec['datetime']:%Y/%m/%d %H:%M:%S}",
    ]
    for rank in rank_list:
        key = f'TOP{rank}'
        msg_lines.append(f'TOP{rank}: {rec[key]:,} P')
    msg_lines.append('```')
    await ctx.send('\n'.join(msg_lines))


@client.event
async def on_voice_state_update(member, before, after):
    server_id_test: Optional[int] = None
    text_id_test: Optional[int] = None
    if member.guild.id == server_id_test:  # server_id
        text_ch = client.get_channel(text_id_test)
        print(text_ch)
        if before.channel is None:
            msg = f'`{member.name}` が `{after.channel.name}` に参加しました。'
            await text_ch.send(msg)


@client.event
async def on_message(message):
    print('---on_message_start---')
    msg_client = message.guild.voice_client
    print(msg_client)
    now = datetime.now()
    mp3_path = f'./output/output_{now:%Y%m%d_%H%M%S}.mp3'
    if not message.content.startswith('.') and message.guild.voice_client:
        print('#message.content:' + message.content)
        exists: bool = create_mp3(message.content, mp3_path)
        if exists:
            source = discord.FFmpegPCMAudio(mp3_path)
            message.guild.voice_client.play(source)
    await client.process_commands(message)
    print('---on_message_end---')


def init():
    for path in glob("./output/output*.mp3"):
        os.remove(path)


def main():
    mkdir('./dict/')
    mkdir('./output/')
    init()
    token: Optional[str] = os.environ.get("CHIRPPY_WIN_TOKEN", None)
    if token is None:
        token = get_token(path="./config.yaml")
    while True:
        try:
            client.run(token)
        except RuntimeError:
            break
        except Exception as e:
            print(e)
            print(traceback.format_exc())


if __name__ == '__main__':
    main()
