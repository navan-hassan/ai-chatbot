import os
import discord
import logging
import asyncio
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()

logging.basicConfig(filename="chatbot.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
 
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
intents = discord.Intents.all()
intents.message_content = True
chatbot = discord.Client(intents=intents)

openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_KEY"),)

async def send_prompt_to_chatgpt(prompt):
	chat_completion = await openai_client.chat.completions.create(
		messages=[{"role": "user", "content": prompt,}],
		model="gpt-3.5-turbo"
		)
	response = chat_completion.choices[0].message.content
	return response

@chatbot.event
async def on_ready():
	guild_count = 0
	for guild in chatbot.guilds:
		logger.info('Connected to guild %s with guild id %d', guild.name, guild.id)

		guild_count = guild_count + 1

	logger.info('Chatbot is connected to %d guild(s)', guild_count)

@chatbot.event
async def on_message(message):
	mention = f'<@{chatbot.user.id}>'
	if message.content.startswith(mention):
		prompt = message.content.replace(mention, '').strip()
		response = await send_prompt_to_chatgpt(prompt)
		await message.channel.send(response)

chatbot.run(DISCORD_TOKEN)
