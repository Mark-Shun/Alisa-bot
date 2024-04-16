
![Alisa Sleepers Image](./images/AlisaSleepers.png?raw=true "Title")
# Alisa Discord Bot

Welcome to the repository for the Alisa Discord bot. Due to having lost the previous iteration of the bot, and discovering that it doesn't compile/run on some IoT devices (Raspberry Pi in this case), I decided to start this little project. The aim is to have a personalized Discord bot that can be run on a low powered device.

## Features

- Can connect to Discord's developer bot service
- Appointing/removing roles through commands
- Alisa responses in chat
- Spam check and deletion
- Directed welcome message when new member joins the server
- Error handling
- ~~Interface with chatGPT API for chatting~~ (Ran out of tokens :) )


## Planned Features
- Admin/mod command tools for configuration
- Local role database that can be updated through discord commands
- Incorporate different conversation model (run locally?)

## Installation

Alisa bot uses the Discord.py API wrapper.
Due to this to run Alisa bot you need two things: python3 and pip (or another package manager) to get the required packages.

```bash
  install python
  install pip
```

Go into the desired terminal (e.x: command prompt)
And install the required packages to run this program
```bash
  pip install -r requirements.txt
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

To run the bot on a testing server, parse the appropriate flag
```bash
  python Alisa.py dev
```

## Environment
The code uses tokens for two bots, namely the main Alisa bot and a testing bot.
Besides that a key for openAI's API is also used.
To get these tokens and key the script retrieves them from the system environment. Make sure they're stored in the environment with the following variable names:
- ALISA_BOT_TOKEN
- ALISA_TEST_BOT_TOKEN
- OPENAI_ALISA_KEY

## Configuration
Configuration is done in the config.py file, tokens, keys and variables can be found there.

## Appendix
The code is specifically written for the Alisa Discord server, it also contains checks to see if it is running on said server.
However with tinkering it could be used for other servers as well, but this code is not intended to be used as a template.
