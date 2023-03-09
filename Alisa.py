import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='.', intents=intents)

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

bot.run('MTA4MzEyMjQ1ODkxMzE0NDg4Mw.GU6Bw-.WaeOyTDm_D1Mgdv-xCBO7wKHTAro-Ld5R4rnF4')
