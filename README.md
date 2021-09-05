# Chirppy for Windows
This is a Bot that reads the channel in Discord. It runs on Windows and Python 3.8 or later.

## Invitation
Server administrators can invite bots from the following URL.  
<https://discord.com/api/oauth2/authorize?client_id=883969791554101270&permissions=0&scope=bot>

## Usage
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