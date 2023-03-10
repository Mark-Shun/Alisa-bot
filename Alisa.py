# Written by Mark-Shun(Sonicfreak)
import discord
import logging
import requests

import config
from responses import Responses
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
        self.responses = None
        self.guild = None
        self.alisa_main = None
        self.alisa_sub = None

    async def on_ready(self):
        self.responses = Responses(self)
        bot_name = (str(self.user)[0:-5])
        self.guild = bot.get_guild(config.GUILD_ID)
        self.alisa_main = discord.utils.get(self.guild.roles, name="Alisa Main")
        self.alisa_sub = discord.utils.get(self.guild.roles, name="Alisa Sub")
        print(f'{bot_name} is now awake.')


bot = Alisa(command_prefix=config.PREFIX, intents=intents, log_handler=handler)

# Error handler
@bot.event
async def on_command_error(ctx,error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.reply(f"That command is not recognized, use {config.PREFIX}help for guidance.", mention_author=True)

# Role management
@bot.command(aliases=["am"])
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

@bot.command(aliases=["lsar"])
async def roles(ctx):
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


# Replying to defined messages
@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message.author == bot.user:
        return # Ignore Alisa's own messages
    
    if message.content.startswith(config.PREFIX):
        return # Ignore messages that start with the command prefix

    await bot.responses.handle_message(message)

bot.run(config.MAIN_TOKEN)