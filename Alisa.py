# Written by Mark-Shun(Sonicfreak) for the Alisa Discord server.
import discord
import logging
import warnings
import sys
import re

import config
from responses import Responses
from activity import ActivityChanger
from anti_spam import AntiSpam
from moderation import Moderation
from discord.ext import commands, tasks

# Check if the passed argument is dev or not to set the dev environment in config
if len(sys.argv) > 1 and sys.argv[1].lower() == 'dev':
    config.setup(True)
else:
    config.setup(False)

# Logger that outputs to alisa.log with basic info and ERROR messages
logger = logging.basicConfig(filename='alisa.log', 
                             level=logging.ERROR,
                             format='%(asctime)s %(levelname)s: %(message)s',
                             datefmt='%Y-%m-%d %H:%M:%S',
                             filemode='a')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# client = discord.Client(intents=intents)

# Declaring the Alisa bot name, later gets adjusted.
bot_name = ''

# Decorator to check if a command is executed in the right channel
def in_allowed_channel(ctx):
    return ctx.channel.id in in_allowed_channel

# Function to check if an asked role is the allowed list.
def is_valid_role(role):
    index = 0
    for i in config.VALID_ROLES:
        if i.lower() == str(role.lower()):
            return True, index
        index += 1
    return False, index

# Custom check function to verify if the user has the "Admin" or "Moderator" role
def is_staff():
    async def predicate(ctx):
        return bot.admin_role in ctx.author.roles or bot.moderator_role in ctx.author.roles
    return commands.check(predicate)

# Class consisting of the Alisa bot
class Alisa(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.responses = None
        self.activity_changer = ActivityChanger(self)
        self.guild = None
        self.alisa_main = None
        self.alisa_sub = None
        self.guest = None
        self.admin_role = None
        self.moderator_role = None
        self.anti_spam = None
        self.moderation = None

    # Once the bot is up and running, execute the following statements.
    async def on_ready(self):
        # Checks if bot is being run on the Alisa server. For developing/testing the Alisa bot run it with the "dev" argument in the terminal.
        if(not(config.DEV)):
            if bot.guilds[0].id != config.Alisa_Server_ID:
                warnings.warn("NOTE: This bot is currently not executing on the Alisa server. \nClosing Alisa")
                await bot.close()
                sys.exit(0)
        random_activity_change.start()
        self.responses = Responses(self)
        bot_name = (str(self.user)[0:-5])
        self.guild = bot.get_guild(config.GUILD_ID)
        self.alisa_main = discord.utils.get(self.guild.roles, name="Alisa Main")
        self.alisa_sub = discord.utils.get(self.guild.roles, name="Alisa Sub")
        self.guest = discord.utils.get(self.guild.roles, name="Guest")
        self.admin_role = discord.utils.get(self.guild.roles, name="Admin")
        self.moderator_role = discord.utils.get(self.guild.roles, name="Moderator")
        self.anti_spam = AntiSpam(self, bot.get_channel(config.BOT_LOGS), self.alisa_main, self.alisa_sub, self.guest)
        self.moderation = Moderation(self, bot.get_channel(config.BOT_LOGS))
        print(f'{bot_name} is now awake.')

# Initialize the Alisa bot
bot = Alisa(command_prefix=config.PREFIX, intents=intents, log_file='alisa.log')

# Change bot's activity in regular intervals
@tasks.loop(hours=4)
async def random_activity_change():
    await bot.activity_changer.random()

# Error handler when command is not found
@bot.event
async def on_command_error(ctx,error):
    if isinstance(error, commands.CommandNotFound):
        # A check to see if message should be interpreted as an command (message starts with a . followed by a letter)
        if not re.match(r'^\.[a-zA-Z]', (ctx.message.content)):
            return # The message does not start with a . followed by a letter
        await ctx.reply(f"That command is not recognized, use {config.PREFIX}help for guidance.", mention_author=True)

# Main role management functionality
@bot.command(aliases=["am"])
@commands.check(lambda ctx: ctx.channel.id == config.ROLES_CHANNEL)
async def iam(ctx, *, role):
    """ Assign a role (only in #roles) """
    #Check if the role exists
    role_name = role.lower()
    if (role_name == "admin" or role_name == "moderator"):
        await ctx.channel.send(f"Nice try. {bot.responses.alisa_laugh}")
        return
    guild = ctx.guild
    valid_result, index = is_valid_role(role_name)

    if (valid_result == True):
        role_obj = discord.utils.get(guild.roles, name=config.VALID_ROLES[index])
        if role_obj in ctx.author.roles:
            await ctx.channel.send(f"Don't you already have the {config.VALID_ROLES[index]} role?")
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
                    message += f"\nAnd I removed the {opp_role.name} role for you."
                await ctx.channel.send(message)
            except discord.errors.Forbidden:
                await ctx.send("I do not have permission to grant this role.")
    else:
        await ctx.channel.send(f"Sorry, {role_name} is not a valid role.")

# Error handler when the role doesn't exist
@iam.error
async def iam_error(ctx,error):
    if isinstance(error, commands.RoleNotFound):
        await ctx.send(f"Excuse me, but that role does not exist.")

# Command to remove a role
@bot.command(aliases=["imnot"])
@commands.check(lambda ctx: ctx.channel.id == config.ROLES_CHANNEL)
async def iamnot(ctx, *, role):
    """ Remove a role (only in #roles)"""
    #Check if the role exists
    role_name = role.lower()
    valid_result, index = is_valid_role(role_name)
    if (valid_result == False):
        await ctx.channel.send(f"Sorry, {role} is not a valid role to remove.")
        return
    guild = ctx.guild
    role_obj = discord.utils.get(guild.roles, name=config.VALID_ROLES[index])
    if role_obj not in ctx.author.roles:
        await ctx.channel.send(f"You don't seem to have the {role_obj.name} role?")
    else:
        try:
            await ctx.author.remove_roles(role_obj)
            await ctx.channel.send(f"You no longer have the {role_obj.name} role.")
        except discord.errors.Forbidden:
            await ctx.send("I do not have permission to remove this role.")

# Error handler for assigning roles
@iamnot.error
async def iamnot_error(ctx,error):
    if isinstance(error, commands.RoleNotFound):
        await ctx.send(f"Excuse me, but that role does not exist.")

# Displays all the assignable roles
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

# Prints an about the bot message
@bot.command()
async def about(ctx):
    """ Introduces the bot """
    alisa_happy = discord.utils.get(bot.emojis, name="Alisa_Happy")
    if alisa_happy == None:
        alisa_happy = ""
    message = f"Hello I'm the Alisacord Bot V1.4, nice to meet you! {alisa_happy}\n\nI've been created by and for this Discord server.\nThere are certain commands I react to which you can see with .help.\nFurthermore I can react to some messages, but over time you'll figure out for what I keep an eye out.\n\nBesides that I'm still being tinkered on so please bear with me.\nIf I start to break down, please contact the staff :)"
    await ctx.reply(message)

# Change bot's activity to a randomly chosen one from the list of activities.
@bot.command(aliases=["rnd","random","randomActivity","random_activity"])
@commands.check(lambda ctx: ctx.channel.id == config.STAFF_COMMANDS_CHANNEL)
@is_staff()
async def randomact(ctx):
    """ Change my activity to a randomly chosen one (staff only) """
    await bot.activity_changer.random()
    await ctx.channel.send("Changed my current activity")

# Issue a warning through DM to an user.
@bot.command(aliases=["warnUser", "warning", "warnuser", "warn_user"])
@commands.check(lambda ctx: ctx.channel.id == config.STAFF_COMMANDS_CHANNEL)
@is_staff()
async def warn(ctx, user_input: str, *, reason):
    """ Warn an user through DM (staff only) """
    await ctx.guild.chunk(cache=True)  # Update the guild members list
    user = bot.guild.get_member_named(user_input)
    if user == None:
        await ctx.reply(f"User \"{user_input}\" was not found.\nPlease check your spelling and make sure it is the nickname they use on the server.")
        return
    await ctx.reply(f"Found user: {user.name}.\nSending warning...")
    await bot.moderation.warn_user(ctx, user, reason)

# Perform functions on detected messages
@bot.event
async def on_message(message):
    # Wait for the bot to finish initializing before processing messages
    await bot.wait_until_ready()
    await bot.process_commands(message)

    if message.author == bot.user:
        return # Ignore Alisacord's own messages
    
    if message.content.startswith(config.PREFIX):
        return # Ignore messages that start with the command prefix

    # Send message to the handle_message function to check and potentially reply with an Alisa response
    await bot.responses.handle_message(message)
    # Check if the message contains spam and log/delete it if a regex rule gets triggered
    await bot.anti_spam.spam_handle_message(message)

# Handling welcome message sent as a DM to new members
@bot.event
async def on_member_join(member):
    try:
        await member.send(config.Welcome_Message)
    except discord.Forbidden:
        # The bot doesn't have permission to send DMs to the member
        warnings.warn(f"Failed to send welcome message to: {member.name}")
    try:
        with open("./images/Arisa.png", 'rb') as arisa_picture:
            picture = discord.File(arisa_picture)
            await member.send(file=picture)
    except FileNotFoundError:
        warnings.warn(f"Picture: {arisa_picture.name} could not be found.")
    except discord.errors.HTTPException:
        warnings.warn(f"Failed to send {arisa_picture.name} picture.")
        
bot.run(config.MAIN_TOKEN)