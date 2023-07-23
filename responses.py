import discord

# This class is used for responding to specific messages in the discord server
class Responses:
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


    async def handle_message(self, message):
        p_message = message.content.lower()
        if "alisa is c tier" in p_message or "c tier" in p_message:
            await message.channel.send(f'So true! {self.alisa_notes}')
        if "alisa dance" == p_message:
            await message.channel.send(self.alisa_dancing)
        if "alisa baila" == p_message:
            await message.channel.send(self.alisa_baila)
        if "alisa sucks" in p_message or "alisa is bad" in p_message:
            await message.channel.send(self.alisa_pout)
        if "alisa is top tier" in p_message:
            await message.channel.send(self.arisa)
        if "alisa is low tier" in p_message or "alisa is bottom tier" in p_message:
            await message.channel.send(self.alisa_cry)
        if "alisa bible" == p_message:
            await message.channel.send("Find the Alisa Bible here: https://docs.google.com/document/d/1hntdSiK3CBprurfSRCm5mKmc7hsGxBwA2ILQZBX2l8Y/edit?usp=sharing")
        if "heart" == p_message:
            await message.channel.send(self.heart)
        if "i love alisa" == p_message:
            await message.reply(f'I love you too {self.alisa_happy}')
        if "nerf alisa" == p_message:
            await message.reply(self.alisa_pout)
        if "buff alisa" in p_message:
            await message.reply(self.alisa_stronk)
        if "nsfw alisa" in p_message:
            await message.reply(self.alisus)
        
        