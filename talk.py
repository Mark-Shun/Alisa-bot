import discord
import openai
import config
import asyncio

class OpenAI:
    def __init__(self, bot, api_key=config.CHAT_KEY, model='text-currie-001'):
        openai.api_key = api_key
        self.model = model
        self.context = []
        self.personality = "You are the android robot character Alisa Bosconovitch from the game Tekken. Answer questions always as Alisa Bosconovitch."
    
    async def generate_response(self, message):
        prompt = f"{self.personality}\n{message}\n\nAlisa:"
        response = openai.Completion.create(
            engine=self.model,
            prompt=prompt,
            max_tokens=500,
            n=1,
            stop=None,
            temperature=0.7,
            presence_penalty=0.6,
            frequency_penalty=0.6,
        )
        return response.choices[0].text.strip()