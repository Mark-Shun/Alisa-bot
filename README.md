
![Alisa Sleepers Image](./images/AlisaSleepers.png?raw=true "Title")
# Alisa Discord Bot

Welcome to the repository for the Alisa Discord bot. Due to having lost the previous iteration of the bot, and discovering that it doesn't compile/run on some IoT devices (Raspberry Pi in this case), I decided to start this little project.

## Features

- Can connect to Discord's developer bot service
- Appointing/removing roles by standard members
- Alisa responses in chat
- Error handling
- Interface with chatGPT API for chatting


## Planned Features
- Admin/mod chat tools to change role handling

## Installation

Alisa bot uses the Discord.py API wrapper.
Due to this to run Alisa bot you need two things: python3 and discord.py
Besides that for the chatting feature the bot also used the openAI library

```bash
  install python
  install pip
```

Go into the desired terminal (e.x: command prompt)

```bash
  pip install discord.py
  pip install openai
```
    
## Run Locally

Clone the project

```bash
  git clone git@github.com:Mark-Shun/Alisa-bot.git
```

Go to the project directory

```bash
  cd Alisa-bot
```

Run the Alisa bot (note: make sure that Python3 is run, some terminals require entering python3 instead of just python)

```bash
  python Alisa.py
```

## Environment
The code uses tokens for two bots, namely the main Alisa bot and a testing bot.
Besides that a key for openAI's API is also used.
To get these tokens and key the script retrieves them from the system environment. Make sure they're stored in the environment with the following variable names:
- ALISA_BOT_TOKEN
- ALISA_TEST_BOT_TOKEN
- OPENAI_ALISA_KEY

## Configuration
Configuration is done in the config.py file, tokens, keys and variables can be found here.
When developing it's important to change the DEV variable to True. And when running the bot normally to set it to False.

## Appendix
While tiny in scope, I hope it will be useful for the Discord server.
![Alisa happy](./images/AlisaHappy.png?raw=true "Title")

