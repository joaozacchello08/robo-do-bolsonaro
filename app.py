from dotenv import load_dotenv
import os
from keep_alive import keep_alive
import discord
from discord.ext import commands
import logging

load_dotenv()
token = os.getenv("DISCORD_TOKEN")

keep_alive()

handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

role_id = 1450224602893652029 # main server role
test_role_id = 1450294816888852480

@bot.event
async def on_ready():
	print(f"Bot is running, {bot.user.name} is ready!")

@bot.event
async def on_member_join(member):
	role = member.guild.get_role(role_id)
	if role:
		await member.add_roles(role)
	elif not role:
		await member.add_roles(test_role_id)
	else:
		print("Couldn't find and assign the role.")

bot.run(token, log_handler=handler, log_level=logging.DEBUG)
