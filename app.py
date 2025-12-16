from keep_alive import keep_alive
from dotenv import load_dotenv
import os
import discord
from discord.ext import commands
import logging
import sqlite3

load_dotenv()
token = os.getenv("DISCORD_TOKEN")

# keep_alive()
handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

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


@bot.command()
async def ping(ctx):
	await ctx.reply("pong :ping_pong:")

@bot.command()
async def lukinhas(ctx):
	pass

bot.run(token, log_handler=handler, log_level=logging.DEBUG)
