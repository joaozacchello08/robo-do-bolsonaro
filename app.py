from keep_alive import keep_alive
from dotenv import load_dotenv
import os
import discord
from discord.ext import commands
import logging
import sqlite3
import asyncio

load_dotenv()
token = os.getenv("DISCORD_TOKEN")

keep_alive()

handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

lukinhas_id = 837599708235038730

#region setting up db
filename = "guild_data.db"
con = sqlite3.connect(filename)
cur = con.cursor()

async def init_guild_data(guild):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS guilds(
            guild_id INTEGER PRIMARY KEY,
            autorole_id INTEGER DEFAULT NULL
        )
    """)
    con.commit()

    cur.execute("""
        INSERT OR IGNORE INTO guilds(guild_id)
        VALUES (?)
    """, (guild.id,))
    con.commit()

@bot.event
async def on_ready():
	for g in bot.guilds:
		await init_guild_data(g)
	print(f"O bot tá rodando nessa porra, {bot.user.name} tá pras foda!")

@bot.event
async def on_guild_join(g):
	await init_guild_data(g)
#endregion

#region autorole
@bot.command()
@commands.has_permissions(administrator=True)
async def setautorole(ctx, role_mention: str):
	try:
		role_id = int(role_mention.strip("<@&>"))
		role = ctx.guild.get_role(role_id)
		if not role:
			await ctx.reply("Cargo não encontrado.")
			return
	except ValueError:
		await ctx.reply("Formato de menção inválido.")
		return
	
	cur.execute("""
		UPDATE guilds
	    SET autorole_id = ?
		WHERE guild_id = ?;
	""", (role_id, ctx.guild.id))
	con.commit()

	await ctx.reply(f"O cargo (ID) {role_id} foi definido como autorole!")

@setautorole.error
async def set_autorole_error(ctx, error):
	if isinstance(error, commands.MissingPermissions):
		await ctx.reply("Você não tem permissão pra isso.")
	elif isinstance(error, commands.BadArgument):
		await ctx.reply("Cargo inválido.")
	else:
		raise error

@bot.event
async def on_member_join(member):
	res = cur.execute(f"SELECT autorole_id FROM guilds WHERE guild_id = {member.guild.id}")
	role_id = res.fetchone()
	if role_id:
		role_id = role_id[0]
		role = member.guild.get_role(role_id)
		if role:
			await member.add_roles(role)
#endregion

# comando teste
@bot.command()
async def ping(ctx):
	await ctx.reply("pong :ping_pong:")

# !lukinhas
scheduled_tasks = {}
@bot.command()
async def lukinhas(ctx):
	# lukinhas usa o comando
	if ctx.author.id == lukinhas_id:
		f = open("assets/john-cena-looking-downwards.gif", "rb")
		gif = discord.File(f)
		await ctx.reply("Lukinhas, você é um bobinho :stuck_out_tongue_closed_eyes::rofl:", file=gif)
		return

	# alguem que nao seja nem eu nem loren
	allowlist = [909210394139168838, 754371726498070568]
	if ctx.author.id not in allowlist:
		f = open("assets/bluezao-macaco.gif", "rb")
		gif = discord.File(f)
		await ctx.reply("O cara achando que vai mutar o Lukinhas :clown: Você não manda em nada aqui não cuzão :rofl:", file=gif)
		return

	member = ctx.guild.get_member(lukinhas_id) or await ctx.guild.fetch_member(lukinhas_id) # member = lukinhas
	if not member or not member.voice:
		await ctx.reply(f"Pô {ctx.author.name}, o Lukinhas nem tá na call :rofl::rofl:")
		return

	# muta
	await member.edit(mute=True)
	await ctx.reply(f"Lukinhas mutado, desmutando em 15 segundos.")

	# cancela a ultima task
	if lukinhas_id in scheduled_tasks:
		scheduled_tasks[lukinhas_id].cancel()

	# agenda desmute
	async def unmute():
		try:
			await asyncio.sleep(15)
			member_check = ctx.guild.get_member(lukinhas_id)
			if member_check and member_check.voice:
				await member_check.edit(mute=False)
				await ctx.send("Lukinhas desmutado.")
		except asyncio.CancelledError:
			pass
	
	task = asyncio.create_task(unmute())
	scheduled_tasks[lukinhas_id] = task

@lukinhas.error
async def lukinhas_on_error(ctx, error):
	await ctx.reply("O Lukinhas infelizmente não foi encontrado no server :cry:")
	return
#endregion

# !loren
@bot.command()
async def loren(ctx):
	f = open("assets/renan-putasso.mp3", "rb")
	audio = discord.File(f)
	await ctx.reply(f"{ctx.author.mention} mandou um recado pro loren:", file=audio)

bot.run(token, log_handler=handler, log_level=logging.DEBUG)
