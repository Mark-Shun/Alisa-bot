DEV = True
if DEV:
    MAIN_TOKEN = 'MTA4MzM5NjE1NDQ2Njc2Mjc4Mg.GRQMjk.maxDv79YYhsIY6nnytvwodrxLnUqcEXipTOF0s'
else:
    MAIN_TOKEN = 'MTA4MzEyMjQ1ODkxMzE0NDg4Mw.Gb6MqV.XWf2KjP-3Sj75QIjMX9W_3SkJoWZ11-q5ZhV78'

CHAT_KEY = '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'
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
    # This is the ID of the guild (server)
    GUILD_ID = 352127467223384076

Alisa_Server_ID = 352127467223384076

RECONNECTION_TIME = 300