import discord
import random

activities = [
    discord.Game(name="TEKKEN 6"),
    discord.Game(name="TEKKEN TAG TOURNAMENT 2"),
    discord.Game(name="TEKKEN 7"),
    discord.Game(name="TEKKEN 8"),
    discord.Activity(type=discord.ActivityType.competing,name="King of Iron Fist Tournament"),
    discord.Streaming(name="Alisa Whiff Tutorial", url="https://www.youtube.com/watch?v=7dgtXQiP7J4")
]

class ActivityChanger:
    def __init__(self, bot):
        self.bot = bot

    async def test(self):
        # activity = discord.Streaming(name="Alisa Whiff Tutorial", url="https://www.youtube.com/watch?v=7dgtXQiP7J4")
        activity = discord.Game(name="TEKKEN REVOLUTION")
        # activity = discord.Activity(type=discord.ActivityType.listening,name="Moonlit Wilderness")
        await self.bot.change_presence(activity=activity)

    async def random(self):
        activity = random.choice(activities)
        await self.bot.change_presence(activity=activity)