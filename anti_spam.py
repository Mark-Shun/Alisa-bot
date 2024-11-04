import discord
import warnings
import re
import config
import asyncio

bot_logs_id = config.BOT_LOGS

# Keeps track how often an user sent a spam message in a specific amount of time.
author_spam_count = {}

# List of regex rules that will trigger a spam message
regex_list = [
    r"(https?:\/\/discord\.gg\/\S+)",
    r"(sex|porn|teen|only\s*?fans)(.|\n)*?(discord\.gg\/(?!s83mVcT)\w*|discord\S*invite\/(?!s83mVcT)\w*)",
    r"(steam.*gift.*https?:\/\/)",
    r"(\bhttps?:\/\/\S*shorturl\S*\b)"
]

# Checks if the message contains any of the regex rules
async def regex_check(message):
    for regex in regex_list:
        if re.search(regex, message.content.lower()):
            return True, regex
    return False, "-"

# Sets up the embed message which gets sent to staff when a spam message is detected
async def setup_spam_embed(title,description,message,triggered_regex):
    spam_embed = discord.Embed(
        title=title,
        description=description,
        color=0xffa500  # Orange color
    )
    spam_embed.add_field(name="Message content", value=message.content)
    spam_embed.add_field(name="Author", value=message.author)
    spam_embed.add_field(name="Channel", value=message.channel)
    spam_embed.add_field(name="Regex triggered", value=triggered_regex)
    return spam_embed

# Checks if an author has sent too many spam messages in a specific amount of time
async def check_spam_author(message, logs_channel):
    author_id = str(message.author.id)
    if author_id in author_spam_count:
        author_spam_count[author_id] += 1
    else:
        author_spam_count[author_id] = 1

    # Check if user count reaches 3 within 10 seconds
    if author_spam_count[author_id] >= 3:
        await message.author.kick(reason="Spam detected")
        await logs_channel.send(f"{message.author.mention} has been kicked for spamming.")
        author_spam_count[author_id] = 0  # Reset the count
    
    # Reset the count after 10 seconds
    await asyncio.sleep(10)
    if author_id in author_spam_count:
        author_spam_count[author_id] = 0

# Class for anti-spam functionality with the bot
class AntiSpam:
    def __init__(self, bot, bot_logs, main_role, sub_role, guest_role):
        self.bot = bot
        self.anti_spam = {}
        self.bot_logs = bot_logs
        self.member_roles = [main_role.name, sub_role.name, guest_role.name]

    # Checks if the message contains any of the regex rules and handles spam messages
    async def spam_handle_message(self, message):
        regex_check_result, triggered_regex = await regex_check(message)
        if regex_check_result:
            if(triggered_regex == "(https?:\/\/discord\.gg\/\S+)"): # Any Discord invite link
               if any(discord.utils.get(message.author.roles, name=role) for role in self.member_roles):
                   return # The author has the appropiate role to send a Discord invite
               else: # The author does not have one of the member roles
                   spam_embed = await setup_spam_embed(title="Server invite link from non-member", description="A user without an Alisa or guest role tried to share a Discord invite.", message=message, triggered_regex=triggered_regex)
                   await self.bot_logs.send(embed=spam_embed)
                   await message.delete()
                   return
            else:
                spam_embed = await setup_spam_embed(title="Spam detected and removed", description="A message has been identified as spam and has been removed.", message=message, triggered_regex=triggered_regex)
                await self.bot_logs.send(embed=spam_embed)
                await message.delete()
                await check_spam_author(message, self.bot_logs)
        else:
            return
        