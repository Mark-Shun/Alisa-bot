import discord
import warnings
import config
import asyncio

async def setup_warn_embed(reason):
    warn_embed = discord.Embed(
        title="A warning from Alisacord staff has been issued",
        description="Dear Alisacord member,\nYou've been given a warning by the staff.\nIf you would like to discuss this matter please create a ticket.",
        color=0xff0000  # Red color
    )
    warn_embed.add_field(name="Explanation", value=reason)
    return warn_embed

async def setup_warn_log_embed(ctx, user, reason):
    warn_log_embed = discord.Embed(
        title="Warning issued",
        description="An Alisacord member has been given a warning.",
        color=0xff0000  # Red color
    )
    warn_log_embed.add_field(name="Moderator", value=ctx.author.name)
    warn_log_embed.add_field(name="User in question", value=user.name)
    warn_log_embed.add_field(name="User ID", value=user.id)
    warn_log_embed.add_field(name="Explanation", value=reason)
    return warn_log_embed

class Moderation:
    def __init__(self, bot, bot_logs):
        self.bot = bot
        self.bot_logs = bot_logs

    async def warn_user(self, ctx, user, reason):
        warn_embed = await setup_warn_embed(reason)
        warn_log_embed = await setup_warn_log_embed(ctx, user, reason)
        try:
            await user.send(embed=warn_embed)
            await self.bot_logs.send(embed=warn_log_embed)
        except discord.errors.Forbidden:
            warnings.warn(f"Forbidden to send warning to: {user.name}")
            await ctx.channel.send(f"Failed to send warning to: {user.name}\nReason: I don't have permission to send DMs to this user.")
        