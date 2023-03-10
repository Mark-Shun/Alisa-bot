import discord

# This class is used for responding to specific messages in the discord server
class Responses:
    def __init__(self, bot):
        self.bot = bot
        #self.alisa_notes = bot.get_emoji(826896985826918430)
        self.alisa_notes = discord.utils.get(self.bot.emojis, name='AlisaNotes')
        self.alisa_dancing = discord.utils.get(self.bot.emojis, name='AlisaDancing')
        self.alisa_baila = discord.utils.get(self.bot.emojis, name='AlisaBaila')
        self.alisa_pout = discord.utils.get(self.bot.emojis, name='AlisaPout')
        self.arisa = discord.utils.get(self.bot.emojis, name="arisabig")
        self.alisa_cry = discord.utils.get(self.bot.emojis, name="alisacry")


    async def handle_message(self, message):
        p_message = message.content.lower()
        if "alisa is c tier" in p_message:
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
        
        