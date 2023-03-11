import os
import warnings
import sys

DEV = True
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

if 'OPENAI_ALISA_KEY' not in os.environ:
    warnings.warn("Environment variable OPENAI_ALISA_KEY not found. The bot will be closed down.")
    sys.exit(0)
CHAT_KEY = os.environ.get('OPENAI_ALISA_KEY')


PREFIX = '.'
WORD_LIMIT = 200

CHARACTER_ROLES = ["Alisa Main", "Alisa Sub"]
REGION_ROLES = ["NA-EAST", "NA-WEST", "EU-EAST", "EU-WEST", "OCE", "EAST-ASIA", "SEA", "MEA"]
PLATFORM_ROLES = ["PC", "PS4", "XBOX"]
MISC_ROLES = ["Guest", "Streamer"]

VALID_ROLES = CHARACTER_ROLES + REGION_ROLES + PLATFORM_ROLES + MISC_ROLES

if DEV:
    # This is the ID for the test server roles channel, this is used to check if the role commands are used in the right channel
    ROLES_CHANNEL = 1083761874979532901
    # This is the ID of the test guild (server)
    GUILD_ID = 427866625899888640
else:
    # This is the ID for the roles channel, this is used to check if the role commands are used in the right channel
    ROLES_CHANNEL = 352128965827231755
    # This is the ID of the Alisa server guild (server)
    GUILD_ID = 352127467223384076

Alisa_Server_ID = 352127467223384076

RECONNECTION_TIME = 300 #Wait 5 minutes