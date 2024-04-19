import discord
import warnings
import re
import config
import asyncio

bot_logs_id = config.BOT_LOGS

author_spam_count = {}

regex_list = [
    r"(teen|only\s*?fans)(.|\n)*?(discord\.gg\/(?!s83mVcT)\w*|discord\S*invite\/(?!s83mVcT)\w*)",
    r"(discord\.gg\/(?!s83mVcT)\w*|discord\S*invite\/(?!s83mVcT)\w*)(.|\n)*?(teen|only\s*?fans)"
]

async def regex_check(message):
    for regex in regex_list:
        if re.search(regex, message.content.lower()):
            return True, regex
    return False, "-"

async def setup_spam_embed(message,triggered_regex):
    spam_embed = discord.Embed(
        title="Spam message detected and deleted",
        description="A message has been identified as spam and removed.",
        color=0xffa500  # Orange color
    )
    spam_embed.add_field(name="Message content", value=message.content)
    spam_embed.add_field(name="Author", value=message.author)
    spam_embed.add_field(name="Channel", value=message.channel)
    spam_embed.add_field(name="Regex triggered", value=triggered_regex)
    return spam_embed

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
    def __init__(self, bot, bot_logs):
        self.bot = bot
        self.anti_spam = {}
        self.bot_logs = bot_logs

    async def spam_handle_message(self, message):
        regex_check_result, triggered_regex = await regex_check(message)
        if regex_check_result:
            spam_embed = await setup_spam_embed(message, triggered_regex)
            await self.bot_logs.send(embed=spam_embed)
            await message.delete()
            await check_spam_author(message, self.bot_logs)
        else:
            return
        