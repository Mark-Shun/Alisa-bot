import os
import warnings
import sys

DEV = None
MAIN_TOKEN = None
ROLES_CHANNEL = None
STAFF_COMMANDS_CHANNEL = None
GUILD_ID = None
BOT_LOGS = None

# Ran at the start of the program to decide which tokens/keys to use depending on the dev argument being passed.
def setup(dev_arg):
    global DEV
    global MAIN_TOKEN
    global ROLES_CHANNEL
    global GUILD_ID
    global STAFF_COMMANDS_CHANNEL
    global VALID_ROLES_LOWER
    global BOT_LOGS

    DEV = dev_arg

    if DEV:
        if 'ALISA_TEST_BOT_TOKEN' not in os.environ:
            warnings.warn("Environment variable ALISA_TEST_BOT_TOKEN not found. The bot will be closed down.")
            sys.exit(0)
        MAIN_TOKEN = os.environ.get('ALISA_TEST_BOT_TOKEN')
    else:
        if 'ALISA_BOT_TOKEN' not in os.environ:
            warnings.warn("Environment variable ALISA_BOT_TOKEN not found. The bot will be closed down.")
            sys.exit(0)
        MAIN_TOKEN = os.environ.get('ALISA_BOT_TOKEN')

    # if 'OPENAI_ALISA_KEY' not in os.environ:
        # warnings.warn("Environment variable OPENAI_ALISA_KEY not found.")
        
    if DEV:
        # This is the ID for the test server roles channel, this is used to check if the role commands are used in the right channel
        ROLES_CHANNEL = 1083761874979532901
        # This is the ID of the test guild (server)
        GUILD_ID = 427866625899888640
        # This is the ID for the staff commands channel, this is used to check if the Alisa bot staff commands are used in the right channel
        STAFF_COMMANDS_CHANNEL = 1083354072972791848
        # THis is the ID for the test server logs channel
        BOT_LOGS = 1228993022679842838
    else:
        # This is the ID for the roles channel, this is used to check if the role commands are used in the right channel
        ROLES_CHANNEL = 352128965827231755
        # This is the ID of the Alisa server guild (server)
        GUILD_ID = 352127467223384076
        # This is the ID for the staff commands channel, this is used to check if the Alisa bot staff commands are used in the right channel
        STAFF_COMMANDS_CHANNEL = 1133070771103744020
        # This is the ID for the logs channel
        BOT_LOGS = 1228355954978853025
    VALID_ROLES_LOWER = [role.lower() for role in VALID_ROLES]

# CHAT_KEY = os.environ.get('OPENAI_ALISA_KEY')

PREFIX = '.'
WORD_LIMIT = 200

CHARACTER_ROLES = ["Alisa Main", "Alisa Sub"]
REGION_ROLES = ["NA-EAST", "NA-WEST", "EU-EAST", "EU-WEST", "SOUTH-AMERICA", "OCE", "MEA", "EAST-ASIA", "SOUTH-ASIA", "SEA"]
PLATFORM_ROLES = ["PC", "PS5","PS4", "XBOX SERIES", "XBOX ONE"]
MISC_ROLES = ["Guest", "Streamer"]

VALID_ROLES = CHARACTER_ROLES + REGION_ROLES + PLATFORM_ROLES + MISC_ROLES
VALID_ROLES_LOWER = []

Alisa_Server_ID = 352127467223384076

Welcome_Message = "*こんにちは！*\nWelcome to the Alisa Bosconovitch Discord server!\nI'm Alisa bot and I hope you'll enjoy your stay.\nMake sure to take a look at the ***quick-start*** channel for the server rules, and grab some roles by heading over to the ***roles*** channel."