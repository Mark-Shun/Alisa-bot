import discord
import logging
from discord.ext import commands

handler = logging.FileHandler(filename='alisa.log', encoding='utf-8', mode='w')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

class Alisa(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        print(f'Alisa has been booted up')

    async def on_message(self, message):
        # Alisa should not reply to herself
        print(f'Noticed a message: ' + str(message.content))
        if message.author.id == self.user.id:
            return
        if message.content.startswith('hello'):
            await message.reply('Hi there!', mention_author=True)


client = Alisa(command_prefix='.', intents=intents, log_handler=handler)
client.run('MTA4MzEyMjQ1ODkxMzE0NDg4Mw.GU6Bw-.WaeOyTDm_D1Mgdv-xCBO7wKHTAro-Ld5R4rnF4')
