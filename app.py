from keep_alive import keep_alive
from dotenv import load_dotenv
import os
import discord
from discord.ext import commands
from discord import app_commands
import logging
import sqlite3
import asyncio
import random

load_dotenv()
token = os.getenv("DISCORD_TOKEN")

handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

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
	# forma desesperada de fazer funfar caso o render caia
	if member.guild.id == 1134246683753054278: # deceint server
		role_id = 1450224602893652029
		role = member.guild.get_role(role_id)
		if role:
			await member.add_roles(role)
			return
		return
	else:
		res = cur.execute(f"SELECT autorole_id FROM guilds WHERE guild_id = {member.guild.id}")
		role_id = res.fetchone()
		if role_id:
			role_id = role_id[0]
			role = member.guild.get_role(role_id)
			if role:
				await member.add_roles(role)
#endregion

#region ping pong
@bot.command()
async def ping(ctx):
	await ctx.reply("pong :ping_pong:")

@bot.command()
async def pong(ctx):
	await ctx.reply("é !ping burro kkkkkk, mas toma seu pong :ping_pong:")
#endregion

#region !mlukinhas
scheduled_tasks = {}
@bot.command()
async def mlukinhas(ctx):
	# lukinhas usa o comando
	if ctx.author.id == lukinhas_id:
		await ctx.reply("Lukinhas, você é um bobinho :stuck_out_tongue_closed_eyes::rofl:", embed="https://cdn.discordapp.com/attachments/1450470865509679114/1450471003640828015/john-cena-looking-downwards.gif?ex=6942a7e3&is=69415663&hm=48b765f095b5c1eb83e2453e8a8d2573bd8af3c80648b58becdd1964a547a782&")
		return

	# alguem que nao seja nem eu nem loren
	allowlist = [909210394139168838, 754371726498070568]
	if ctx.author.id not in allowlist:
		await ctx.reply(
			"Boa fdp, ta achando que vai mutar o Lukinhas :clown:? Você não manda em nada aqui não cuzão :rofl:",
			embed=discord.Embed().set_image(url="https://cdn.discordapp.com/attachments/1450470865509679114/1450471002411765911/bluezao-macaco.gif?ex=6942a7e3&is=69415663&hm=355db46c5d6714a7022e2e68b6ec4f6f57ff1bf1fc21f4a09a87b8f77660feec&")
		)
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

@mlukinhas.error
async def lukinhas_on_error(ctx, error):
	await ctx.reply("O Lukinhas infelizmente não foi encontrado no server :cry:")
	return
#endregion

#region !loren
@bot.command()
async def loren(ctx):
	f = open("media/renan-putasso.mp3", "rb")
	audio = discord.File(f)
	await ctx.reply(f"{ctx.author.mention} mandou um recado pro loren:", file=audio)
	return
#endregion

#region !fabgodamn
@bot.command()
async def fabgodamn(ctx):
	videos = ["https://cdn.discordapp.com/attachments/1450470865509679114/1450470932195053569/12162.mp4?ex=6942a7d2&is=69415652&hm=e64e4c0604d150712116d40a2413e9755681daca0e304d62fd394205f37e931f&", "https://cdn.discordapp.com/attachments/1450470865509679114/1450470932907954226/12163.mp4?ex=6942a7d2&is=69415652&hm=94e2877df6bd2709cb47f6348def5263f5adbc2a5183fbcaa12acd18dfa12c45&", "https://cdn.discordapp.com/attachments/1450470865509679114/1450470933973438586/12164.mp4?ex=6942a7d3&is=69415653&hm=e843b73eae84e6938b3eebc3550d063463b9430b0ac82d26a4ba64e1135a7a34&", "https://cdn.discordapp.com/attachments/1450470865509679114/1450470934925410354/12165.mp4?ex=6942a7d3&is=69415653&hm=784c65cadc7a6a04816cebc3caf5ac7e17c88e86fba122d8871d512faf21cb2d&", "https://cdn.discordapp.com/attachments/1450470865509679114/1450470935697166457/12166.mp4?ex=6942a7d3&is=69415653&hm=76f01e4876ae96ae82cacec09d49b91304150c54c8b756966b4a60b74586de91&", "https://cdn.discordapp.com/attachments/1450470865509679114/1450470936586489856/12167.mp4?ex=6942a7d3&is=69415653&hm=03a8fb69039c24e2d4a183db3209d0c5f8f6e1aee9c332eacf57e796ac668114&", "https://cdn.discordapp.com/attachments/1450470865509679114/1450470943049646180/12168.mp4?ex=6942a7d5&is=69415655&hm=60fb7d21c31d9921e05a1d9cf880a6f88c792b222ddb6c15c58d7afd4bb101b7&", "https://cdn.discordapp.com/attachments/1450470865509679114/1450470944677298248/12169.mp4?ex=6942a7d5&is=69415655&hm=0653b5e9909699cd39afd78e931c3332bb7211f5f79fa4723c12dbced33834fc&", "https://cdn.discordapp.com/attachments/1450470865509679114/1450470945788657808/12161.mp4?ex=6942a7d5&is=69415655&hm=4290d0fda1a176aad81b119c30b274c53e48f56baaa4b02d51acdae85e5ab2ef&", "https://cdn.discordapp.com/attachments/1450470865509679114/1450470962200973332/1216.mp4?ex=6942a7d9&is=69415659&hm=c8194e3a098a2e8bb9312ef51a743c9b1a31341dbc84cc382247091022aeb945&", "https://cdn.discordapp.com/attachments/1450470865509679114/1450470962914132100/121610.mp4?ex=6942a7da&is=6941565a&hm=65ecebab3adb6010dc46c57458982e760c4fd70f49c835365ece63d3b123a369&"]
	video = videos[random.randint(0, len(videos) - 1)]
	await ctx.reply(f"FABGODAMN\n{video}")
	return
#endregion

#region help
@bot.command()
async def help(ctx):
	comandos = [command.name for command in bot.commands]
	text = ""
	for c in comandos:
		text += f"```!{c}```\n"
	await ctx.reply(text)
#endregion

#region generational roast
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    await bot.process_commands(message)

    if not message.content.startswith("!"):
        return

    comandos = [c.name for c in bot.commands]
    comando = message.content[1:].split()[0]

    if comando not in comandos:
        membro = discord.utils.get(message.guild.members, name=comando)
        if not membro:
            membro = discord.utils.get(message.guild.members, nick=comando)
        if membro:
            await message.reply(f"{membro.mention} vai se fuder")
        else:
            await message.reply("Comando ou usuário não existente.")
#endregion

if __name__ == "__main__":
	keep_alive()
	bot.run(token, log_handler=handler, log_level=logging.DEBUG)
