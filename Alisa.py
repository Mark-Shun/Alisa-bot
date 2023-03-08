import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='>')

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

bot.run('MTA4MzEyMjQ1ODkxMzEoNDg4Mw.GEMLoM.u3Y1c9bcuMlxOB-lcX_HQ9tUyeNPsmojOsud_M')
