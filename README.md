# Chirppy for Windows

## TOC
 * [Summary](#summary)
 * [Usage](#usage)
	 * [Discord command (for Users)](#discord-command-for-users)
	 * [Build (for Developers)](#build-for-developers)
		 * [pip](#pip)
		 * [Install ffmpeg](#install-ffmpeg)
		 * [Registering the Bot](#registering-the-bot)
		 * [Invite the Bot](#invite-the-bot)
		 * [Start the Bot](#start-the-bot)

## Summary

This is a Bot that reads the channel in Discord. It runs on Windows and Python 3.8 or later.

## Usage
### Config.yaml

```yaml
token:
voice_state:
  update:
    server_id:
    text_ch_id:
message:
  mute:
    - 235088799074484224 # Rythm
    - 252128902418268161 # Rythm2
    - 533698325203910668 # shovel blue
    - 600611680711606284 # shovel red
    - 600611976024162304 # shovel green
    - 518899666637553667 # しゃべ太郎

```
### Discord command (for Users)
| Command           | Description                                                                                                                                 |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| .join             | Reads out the channel where the `.join` was posted.<br> The Bot will join the voice channel where the user who posted the .join is located. |
| .bye              | Exits the bot from the voice channel.                                                                                                       |
| .register `A` `B` | Register word `A` to be read as word `B`.                                                                                                   |

### Build (for Developers)
#### pip
Use requirements.txt to install the necessary packages.

```shell
pip install -r requirements.txt
```

#### Install ffmpeg
Install ffmpeg and to open the Path to ffmpeg.exe so that it can be executed.

#### Registering the Bot

Create a Discord Bot by referring to the [tutorial](https://ikayome.hateblo.jp/entry/2019/07/03/Discord_bot%E4%BD%9C%E6%88%90%E3%83%81%E3%83%A5%E3%83%BC%E3%83%88%E3%83%AA%E3%82%A2%E3%83%AB), and set the token to the environment variable `CHIRPPY_WIN_TOKEN` after creating the bot and getting the token.

#### Invite the Bot

Share the Bot invitation URL with the server administrator, who can invite the Bot from the URL.

#### Start the Bot

Run `chirppy_for_win.py` to start the bot.

## Reference
* [readBot](https://github.com/Nemy-z2z/readBot)
* [見様見真似でDiscordのチャット読み上げbotを作った](https://qiita.com/Nemy/items/d895114d3ba9a9d7cb62)