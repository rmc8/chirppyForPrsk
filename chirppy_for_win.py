import os
import traceback

import discord
from discord.ext import commands

from pkg.util import mkdir, get_token
from pkg.voice_generator import create_wav

client = commands.Bot(command_prefix='.')
voice_client = None


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
        print('dic.txtに書き込み：''\n' + arg1 + ',' + arg2)
    await ctx.send('`' + arg1 + '` を `' + arg2 + '` として登録しました')


@client.event
async def on_voice_state_update(member, before, after):
    server_id_test: str = 'サーバーID'
    text_id_test: int = 0  # 通知させたいテキストチャンネルID
    if member.guild.id == server_id_test:  # server_id
        text_ch = client.get_channel(text_id_test)  # 通知させたいTEXTチャンネルid
        if before.channel is None:
            msg = f'【VC参加ログ】{member.name} が {after.channel.name} に参加しました。'
            await text_ch.send(msg)


@client.event
async def on_message(message):
    print('---on_message_start---')
    msg_client = message.guild.voice_client
    print(msg_client)
    if not message.content.startswith('.') and message.guild.voice_client:
        print('#message.content:' + message.content)
        mp3_path = './output/output.mp3'
        create_wav(message.content, mp3_path)
        source = discord.FFmpegPCMAudio(mp3_path)
        message.guild.voice_client.play(source)
    await client.process_commands(message)
    print('---on_message_end---')


def main():
    mkdir('./dict/')
    mkdir('./output/')
    token: str = os.environ.get("CHIRPPY_WIN_TOKEN",
                                get_token(path="./config.yaml"))
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
