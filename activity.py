import discord
import random

# Activities list made out of dictionaries consisting of activity and the weight of said activity
activities = [
    {"activity": discord.Game(name="TEKKEN 6"), "weight": 0},
    {"activity": discord.Game(name="TEKKEN TAG TOURNAMENT 2"), "weight": 0},
    {"activity": discord.Game(name="TEKKEN 7"), "weight": 2},
    {"activity": discord.Game(name="TEKKEN 8"), "weight": 6},
    {"activity": discord.Activity(type=discord.ActivityType.competing, name="King of Iron Fist Tournament"), "weight": 2},
    {"activity": discord.Streaming(name="Alisa Whiff Tutorial", url="https://www.youtube.com/watch?v=7dgtXQiP7J4"), "weight": 3},
    {"activity": discord.Streaming(name="Alisa T8 Changes", url="https://www.youtube.com/watch?v=_PzZRJsbuAk"), "weight": 3},
    {"activity": discord.Streaming(name="T8 Alisa Open Stage Combos", url="https://www.youtube.com/watch?v=oTAacEM9stY"), "weight": 3},
    {"activity": discord.Streaming(name="T8 Alisa Wall Combos", url="https://www.youtube.com/watch?v=4m90CLwDnQU"), "weight": 3},
    {"activity": discord.Game(name="Final Fantasy V"), "weight": 1},
    {"activity": discord.Game(name="Harvest Moon 64"), "weight": 1},
    {"activity": discord.Game(name="Final Fantasy XIII"), "weight": 1},
    {"activity": discord.Game(name="Sonic Adventure 2 in Chao Garden"), "weight": 1}
]

# Puts activities in a new list, which multiplies the amount of times the activity is represented according to its weight
weighted_activities = [activity for activity in activities for _ in range(activity["weight"])]

# This class is used to change the activity of the bot
class ActivityChanger:
    def __init__(self, bot):
        self.bot = bot

    # Hardcoded test function
    async def test(self):
        # activity = discord.Streaming(name="Alisa Whiff Tutorial", url="https://www.youtube.com/watch?v=7dgtXQiP7J4")
        activity = discord.Game(name="TEKKEN REVOLUTION")
        # activity = discord.Activity(type=discord.ActivityType.listening,name="Moonlit Wilderness")
        await self.bot.change_presence(activity=activity)

    # Changes the activity of the bot to a random one in the list
    async def random(self):
        chosen_activity = random.choice(weighted_activities)
        await self.bot.change_presence(activity=chosen_activity["activity"])