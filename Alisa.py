# Written by Mark-Shun(Sonicfreak) for the Alisa Discord server.
import discord
import logging
import warnings
import requests
import asyncio
import aiohttp
import sys

import config
from responses import Responses
from talk import OpenAI
from discord.ext import commands

# Logger that outputs to alisa.log with basic info and ERROR messages
logger = logging.basicConfig(filename='alisa.log', 
                             level=logging.ERROR,
                             format='%(asctime)s %(levelname)s: %(message)s',
                             datefmt='%Y-%m-%d %H:%M:%S',
                             filemode='a')

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
        self.responses = None
        self.openai = None
        self.guild = None
        self.alisa_main = None
        self.alisa_sub = None

    async def on_ready(self):
        # Checks if bot is being run on the Alisa server. For developing/testing change DEV in config.
        if(not(config.DEV)):
            if bot.guilds[0].id != config.Alisa_Server_ID:
                warnings.warn("NOTE: This bot is currently not executing on the Alisa server. \nClosing Alisa")
                await bot.close()
                sys.exit(0)
        self.responses = Responses(self)
        self.openai = OpenAI(self)
        bot_name = (str(self.user)[0:-5])
        self.guild = bot.get_guild(config.GUILD_ID)
        self.alisa_main = discord.utils.get(self.guild.roles, name="Alisa Main")
        self.alisa_sub = discord.utils.get(self.guild.roles, name="Alisa Sub")
        print(f'{bot_name} is now awake.')


bot = Alisa(command_prefix=config.PREFIX, intents=intents, log_file='alisa.log')

# Error handler
@bot.event
async def on_command_error(ctx,error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.reply(f"That command is not recognized, use {config.PREFIX}help for guidance.", mention_author=True)

# Role management
@bot.command(aliases=["am"])
@commands.check(lambda ctx: ctx.channel.id == config.ROLES_CHANNEL)
async def iam(ctx, *, role: discord.Role):
    """ Assign a role (only in #roles) """
    #Check if the role exists
    guild = ctx.guild
    role_obj = discord.utils.get(guild.roles, name=role.name)
    if role_obj is None:
        await ctx.send(f"Excuse me, but the {role} role does not exist.")

    if is_valid_role(role_obj):
        if role_obj in ctx.author.roles:
            await ctx.channel.send(f"You already have the {role_obj.name} role.")
        else:
            # Checking if character role gets changed, to eventually remove the other one
            if role_obj == bot.alisa_main:
                opp_role = bot.alisa_sub
            elif role_obj == bot.alisa_sub:
                opp_role = bot.alisa_main
            else:
                opp_role = None
                
            try:
                await ctx.author.add_roles(role_obj)
                message = f"You now have the {role_obj.name} role!"
                if opp_role and opp_role in ctx.author.roles:
                    await ctx.author.remove_roles(opp_role)
                    message += f"\n And I removed the {opp_role.name} role."
                await ctx.channel.send(message)
            except discord.errors.Forbidden:
                await ctx.send("I do not have permission to grant this role.")
    else:
        await ctx.channel.send(f"Sorry, {role_obj.name} is not a valid role.")

@iam.error
async def iam_error(ctx,error):
    if isinstance(error, commands.RoleNotFound):
        await ctx.send(f"Excuse me, but that role does not exist.")

@bot.command(aliases=["imnot"])
@commands.check(lambda ctx: ctx.channel.id == config.ROLES_CHANNEL)
async def iamnot(ctx, *, role: discord.Role):
    """ Remove a role (only in #roles)"""
    #Check if the role exists
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

# Displays all the roles
@bot.command(aliases=["lsar"])
@commands.check(lambda ctx: ctx.channel.id == config.ROLES_CHANNEL)
async def roles(ctx):
    """ 
    Display all the available roles you can assign
    """
    message = "These are the current roles that you can assign:"
    message += "\n**Character roles:**\n- "
    message += "\n- ".join(config.CHARACTER_ROLES)
    message += "\n**Region roles:**\n- "
    message += "\n- ".join(config.REGION_ROLES)
    message += "\n**Platform roles:**\n- "
    message += "\n- ".join(config.PLATFORM_ROLES)
    message += "\n**Misc roles:**\n- "
    message += "\n- ".join(config.MISC_ROLES)
    await ctx.channel.send(message)

# Prints an about message
@bot.command()
async def about(ctx):
    """ Introduces the bot """
    alisa_happy = discord.utils.get(bot.emojis, name="Alisa_Happy")
    if alisa_happy == None:
        alisa_happy = ""
    message = f"Hello I'm the Alisa Bosconovitch Bot V1.2, nice to meet you! {alisa_happy}\n\nI've been created by and for this Discord server.\nThere are certain commands I react to which you can see with .help.\nFurthermore I can react to some messages, but over time you'll figure out for what I keep an eye out.\n\nBesides that I'm still being tinkered on so please bear with me.\nIf I start to break down please contact the staff :)"
    await ctx.reply(message)

@bot.command(aliases=["speak","chat"])
async def talk(ctx, *, message):
    """ Use AI to talk with the bot. (Limited use) """
    if len(message.split()) > config.WORD_LIMIT:
        await ctx.reply(f"Owh that's a bit much to compute, please keep your message under the {config.WORD_LIMIT} words size limit.")
        return
    response = await bot.openai.generate_response(message)
    await ctx.reply(str(response), mention_author = True)

# Replying to defined messages
@bot.event
async def on_message(message):
    # Wait for the bot to finish initializing before processing messages
    await bot.wait_until_ready()
    await bot.process_commands(message)

    if message.author == bot.user:
        return # Ignore Alisa's own messages
    
    if message.content.startswith(config.PREFIX):
        return # Ignore messages that start with the command prefix

    # Send message to the handle_message function to check and respond to
    await bot.responses.handle_message(message)

bot.run(config.MAIN_TOKEN)