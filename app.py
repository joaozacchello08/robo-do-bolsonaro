from keep_alive import keep_alive
from dotenv import load_dotenv
import os
import discord
from discord.ext import commands
import logging
import asyncio

load_dotenv()
token = os.getenv("DISCORD_TOKEN")

keep_alive()

handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
intents = discord.Intents.all()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

role_id = 1450224602893652029 # main server role
test_role_id = 1450294816888852480
id_lukinhas = 837599708235038730

@bot.event
async def on_ready():
	print(f"Bot is running, {bot.user.name} is ready!")

@bot.event
async def on_member_join(member):
	role = member.guild.get_role(role_id)
	test_role = member.guild.get_role(test_role_id)
	if role:
		await member.add_roles(role)
	elif not role:
		await member.add_roles(test_role)
	else:
		print("Couldn't find and assign the role.")

@bot.command()
async def lukinhas(ctx):
	member = ctx.guild.get_member(id_lukinhas)

	if not member:
		await ctx.reply(f"Usuário Lukinhas (ID: {id_lukinhas}) não encontrado.")
		return

	if not member.voice:
		await ctx.reply(f"Porra {ctx.author.name}, o Lukinhas nem tá na call :rofl::rofl:", mention_author=False)
		return

	# mutar
	await member.edit(mute=True)
	await ctx.send(f"Lukinhas mutado com sucesso, desmutando em 30 segundos. {member.mention}")

	# esperar, desmutar
	await asyncio.sleep(30)
	await member.edit(mute=False)
	await member.send(f"Lukinhas desmutado. {ctx.author.mention}")

bot.run(token, log_handler=handler, log_level=logging.DEBUG)
