# Written by Mark-Shun(Sonicfreak)
import discord
import logging
import requests

import config
from discord.ext import commands

handler = logging.FileHandler(filename='alisa.log', encoding='utf-8', mode='w')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot_name = ''

# Decorator to check if a command is executed in the right channel
def in_allowed_channel(ctx):
    return ctx.channel.id in in_allowed_channel

# Function to check if an asked role is the allowed list.
def is_valid_role(role):
    for i in config.VALID_ROLES:
        if i == str(role):
            return True
    return False

class Alisa(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        bot_name = (str(self.user)[0:-5])
        print(f'{bot_name} is now awake.')
        #await message.channel.send("Alisa has been booted up")

bot = Alisa(command_prefix=config.PREFIX, intents=intents, log_handler=handler)

# Role management
@bot.command()
@commands.check(lambda ctx: ctx.channel.id == config.ROLES_CHANNEL)
async def iam(ctx, *, role: discord.Role):
    #Check if the role exists
    guild = ctx.guild
    role_obj = discord.utils.get(guild.roles, name=role.name)
    if role_obj is None:
        await ctx.send(f"Excuse me, but the {role} role does not exist.")

    if is_valid_role(role_obj):
        if role_obj in ctx.author.roles:
            await ctx.channel.send(f"You already have the {role_obj.name} role.")
        else:
            try:
                await ctx.author.add_roles(role_obj)
                await ctx.channel.send(f"You now have the {role_obj.name} role!")
            except discord.errors.Forbidden:
                await ctx.send("I do not have permission to grant this role.")
    else:
        await ctx.channel.send(f"Sorry, {role_obj.name} is not a valid role.")

@iam.error
async def iam_error(ctx,error):
    if isinstance(error, commands.RoleNotFound):
        await ctx.send(f"Excuse me, but that role does not exist.")

@bot.command()
@commands.check(lambda ctx: ctx.channel.id == config.ROLES_CHANNEL)
async def iamnot(ctx, *, role: discord.Role):
    #Check if the role exists
    print("Role to check: " + str(role))
    guild = ctx.guild
    role_obj = discord.utils.get(guild.roles, name=role.name)
    if role_obj is None:
        await ctx.send(f"Excuse me, but the {role} role does not exist.")
    if is_valid_role(role_obj):
        if role_obj not in ctx.author.roles:
            await ctx.channel.send(f"You don't have the {role_obj.name} role!")
        else:
            await ctx.author.remove_roles(role_obj)
            await ctx.channel.send(f"You no longer have the {role_obj.name} role.")
    else:
        await ctx.channel.send(f"Sorry, {role_obj.name} is not a valid role.")

@iamnot.error
async def iamnot_error(ctx,error):
    if isinstance(error, commands.RoleNotFound):
        await ctx.send(f"Excuse me, but that role does not exist.")

# Replying to defined messages
@bot.event
async def on_message(message):
    await bot.process_commands(message)
    print(f'Noticed a message: ' + str(message.content))
    if message.author == bot.user:
        return # Ignore Alisa's own messages
    
    if message.content.startswith(config.PREFIX):
        return # Ignore messages that start with the command prefix

    if message.content.startswith('hello'):
        await message.reply('Hi there!', mention_author=True)

bot.run(config.MAIN_TOKEN)