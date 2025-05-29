import discord
import re

# This class is used for responding to specific messages in the discord server
class Responses:
    # Initializes the bot with specific emojis
    def __init__(self, bot):
        self.bot = bot
        self.alisa_notes = discord.utils.get(self.bot.emojis, name='AlisaNotes')
        self.alisa_dancing = discord.utils.get(self.bot.emojis, name='AlisaDancing')
        self.alisa_baila = discord.utils.get(self.bot.emojis, name='AlisaBaila')
        self.alisa_pout = discord.utils.get(self.bot.emojis, name='AlisaPout')
        self.arisa = discord.utils.get(self.bot.emojis, name="arisabig")
        self.alisa_cry = discord.utils.get(self.bot.emojis, name="alisacry")
        self.heart = discord.utils.get(self.bot.emojis, name="Heart")
        self.alisa_happy = discord.utils.get(self.bot.emojis, name="Alisa_Happy")
        self.alisa_stronk = discord.utils.get(self.bot.emojis, name="Alisa_Stronk")
        self.alisus = discord.utils.get(self.bot.emojis, name="alisus")
        self.alisa_laugh = discord.utils.get(self.bot.emojis, name="AlisaLaugh")
        self.chainsaw_ok = discord.utils.get(self.bot.emojis, name=":arisabrrrr")

    # Check if an user message contains a specific response
    async def handle_message(self, message):
        p_message = message.content.lower()
        if re.search(r"\balisa is c tier\b", p_message):
            await message.channel.send(f'So true! {self.alisa_notes}')
        if re.search(r"^\balisa dance\b$", p_message):
            await message.channel.send(self.alisa_dancing)
        if re.search(r"^\balisa baila\b$", p_message):
            await message.channel.send(self.alisa_baila)
        if re.search(r"\balisa sucks\b", p_message) or re.search(r"\balisa is bad\b", p_message):
            await message.channel.send(self.alisa_pout)
        if re.search(r"\balisa is top tier\b", p_message):
            await message.channel.send(self.arisa)
        if re.search(r"\balisa is low tier\b", p_message) or re.search(r"\balisa is bottom tier\b", p_message):
            await message.channel.send(self.alisa_cry)
        if re.search(r"^\balisa bible\b$", p_message):
            await message.channel.send("Find the Alisa Bible here: https://docs.google.com/document/d/1hntdSiK3CBprurfSRCm5mKmc7hsGxBwA2ILQZBX2l8Y/edit?usp=sharing")
        if re.search(r"^\bheart\b$", p_message):
            await message.channel.send(self.heart)
        if re.search(r"^\bi love alisa\b$", p_message):
            await message.reply(f'I love you too {self.alisa_happy}')
        if re.search(r"^\bnerf alisa\b$", p_message):
            await message.reply(self.alisa_pout)
        if re.search(r"\bbuff alisa\b", p_message):
            await message.reply(self.alisa_stronk)
        if re.search(r"\bnsfw alisa\b", p_message):
            await message.reply(self.alisus)
        if re.search(r"\bi love chainsaws\b", p_message) or re.search(r"\bi love design\b", p_message):
            await message.reply(self.chainsaw_ok)
        