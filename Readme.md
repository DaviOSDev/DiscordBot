# BotFTD

A Discord bot made by an student to learn some libraries - [Still in production]
## Topics

- [Commands](#commands)
- [Instalation](#instalation)


## Commands

### Dice commands

>Roll/r -> roll dices of your choice [number]d[number]\
rollshow/rs/r#/roll# -> roll dices and show the result of each of them


### Music commands

>play/p -> plays the audio of a youtube video - ?p [url or title]\
resume -> resume the audio\
pause -> pause the audio\
show-queue -> show the next 4 musics in queue\
clear-queue -> clears the queue\
volume -> change the music volume [should be used before search the video]\
stop -> stops music and disconnect the bot\
next -> skips the current audio [if there's no music in queue disconnect the bot]\


## Instalation

#### Clone the repository
Create a folder, take its path on cmd and type:
``` 
git clone https://github.com/DaviOSDev/DiscordBot.git
```

#### Download the libs used:

On the same path in cmd, type:
```
pip install -r src\Configs\dependencies.txt
```

#### Download ffmpeg

>What is ffmpeg?
>>ffmpeg is a computer program that record, convert and create a audio stream on multiple formats. For this application this program its used to convert the youtube extracted video in a format that [discord.py](https://discordpy.readthedocs.io/en/stable/index.html) supports

Go to [ffmpeg](https://www.ffmpeg.org/download.html) and download the 7zip file./

Once the download is finished copy the path for the ffmpeg folder and put it as an environment variable.
