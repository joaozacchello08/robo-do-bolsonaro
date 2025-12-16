from keep_alive import keep_alive
from dotenv import load_dotenv
import os
import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
import logging
import asyncio

load_dotenv()
token = os.getenv("DISCORD_TOKEN")

# keep_alive() # keep it off for render

handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

role_id = 1450224602893652029 # main server role
test_role_id = 1450294816888852480
lukinhas_id = 837599708235038730
adm_role = 1423426169381978173
loren_id = 754371726498070568
xongs_id = 909210394139168838

ffmpeg_executable = "./ffmpeg"

@bot.event
async def on_ready():
	print(f"Bot is running, {bot.user.name} is ready!")
	return

@bot.event
async def on_member_join(member):
	role = member.guild.get_role(role_id)
	test_role = member.guild.get_role(test_role_id)
	if role:
		await member.add_roles(role)
		return
	elif not role:
		await member.add_roles(test_role)
		return
	else:
		print("Couldn't find and assign the role.")
		return

@bot.command()
async def ping(ctx):
	await ctx.reply("pong")

@bot.command()
# @commands.has_role(adm_role)
async def lukinhas(ctx):
	if ctx.author.id not in [loren_id, xongs_id, lukinhas_id]: # not working
		file = discord.File("assets/bluezao-macaco.gif", filename="bluezao-puto-com-macaquisse.gif")
		await ctx.reply("Tá querendo mutar o MEU Lukinhas sem ser adm? Você não manda em nada aqui porra. ", file=file)
		return

	if ctx.author.id == lukinhas_id:
		file = discord.File("assets/john-cena-looking-downwards.gif", filename="john-cena-decepcionado-com-macaquisse.gif")
		await ctx.reply("Lukinhas, você é um bobinho :rofl::rofl:", file=file)
		return

	member = ctx.guild.get_member(lukinhas_id) # member = lukinhas
	if not member:
		await ctx.reply(f"Usuário Lukinhas (ID: {lukinhas_id}) não encontrado.")
		return

	if not member.voice:
		await ctx.reply(f"Porra {ctx.author.name}, o Lukinhas nem tá na call :rofl::rofl:")
		return

	# mutar
	await member.edit(mute=True)
	await ctx.reply(f"Lukinhas mutado com sucesso, desmutando em 15 segundos. {ctx.author.mention}")

	# fazer o bot entrar e tocar o audio do renan puto
	channel = member.voice.channel
	vc = ctx.voice_client
	if vc and vc.is_connected():
		pass
	else:
		vc = await channel.connect()

	audio = FFmpegPCMAudio(
		source="assets/renan-putasso.mp3",
		executable=ffmpeg_executable
	)
	vc.play(audio)

	# esperar, desmutar
	await asyncio.sleep(15)
	await member.edit(mute=False)
	await ctx.send(f"Lukinhas ~~infelizmente~~ desmutado. {ctx.author.mention} {member.mention}")

bot.run(token, log_handler=handler, log_level=logging.DEBUG)
