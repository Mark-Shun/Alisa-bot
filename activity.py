import discord
import warnings
import random

activities = [
    discord.Game(name="TEKKEN 6"),
    discord.Game(name="TEKKEN TAG TOURNAMENT 2"),
    discord.Game(name="TEKKEN 7"),
    discord.Activity(type=discord.ActivityType.competing,name="Iron Fist Tournament"),
    discord.Activity(type=discord.ActivityType.watching,name="Gajimaru guides"),
    discord.Streaming(name="Alisa Whiff Tutorial", url="https://www.youtube.com/watch?v=7dgtXQiP7J4&t=47s")
]

class ActivityChanger:
    def __init__(self, bot):
        self.bot = bot

    async def test(self):
        # activity = discord.Streaming(name="Alisa Whiff Tutorial", url="https://www.youtube.com/watch?v=7dgtXQiP7J4&t=47s")
        activity = discord.Game(name="TEKKEN REVOLUTION")
        # activity = discord.Activity(type=discord.ActivityType.listening,name="Moonlit Wilderness")
        await self.bot.change_presence(activity=activity)

    async def random(self):
        activity = random.choice(activities)
        await self.bot.change_presence(activity=activity)