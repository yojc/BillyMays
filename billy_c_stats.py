import discord
import asyncio
import sqlite3
import re
import emoji
from datetime import datetime, timedelta
from discord.utils import find
from timeit import default_timer as timer

import billy_shared as sh
from config import STATS_DB_FILENAME, STATS_CHANNELS_TO_OMIT, STATS_USERS_TO_OMIT, STATS_RESULTS_COUNT, STATS_CHANNELS_MORE_RESULTS, STATS_CHANNELS_MORE_RESULTS_COUNT

# Placeholder string
NOT_FOUND = "[nie znaleziono]"

# Channels to hide results from (they are still calculated!)
CHANNELS_TO_OMIT = str(tuple(STATS_CHANNELS_TO_OMIT)).rstrip(',)') + ')'

# Users to hide results from (they are still calculated!)
USERS_TO_OMIT = str(tuple(STATS_USERS_TO_OMIT)).rstrip(',)') + ')'
# !!! NOTE !!!
# This only hides user(s) from the user stat table; other stats are unaffected
# In case you need to expand it, change the stats_channels etc.

# Database init strings

MSG_INIT_STRING = '''CREATE TABLE IF NOT EXISTS messages (
	message INTEGER NOT NULL PRIMARY KEY UNIQUE,
	server INTEGER NOT NULL,
	channel INTEGER,
	user INTEGER NOT NULL,
	time INTEGER NOT NULL,
	everyone INTEGER NOT NULL,
	deleted INTEGER NOT NULL,
	bot INTEGER NOT NULL,
	function TEXT
)'''
EMO_INIT_STRING = '''CREATE TABLE IF NOT EXISTS emojis (
	emoji TEXT NOT NULL,
	server INTEGER NOT NULL,
	channel INTEGER,
	message INTEGER NOT NULL,
	user INTEGER NOT NULL,
	time INTEGER NOT NULL,
	count INTEGER NOT NULL,
	reaction INTEGER NOT NULL,
	custom INTEGER NOT NULL,
	bot INTEGER NOT NULL
)'''

# Open database
stats = sqlite3.connect(sh.file_path(STATS_DB_FILENAME))
stats_c = stats.cursor()

# Init database if necessary
stats_c.execute(MSG_INIT_STRING)
stats_c.execute(EMO_INIT_STRING)
stats.commit()

# Writing into database

def insert_msg(msg, db=stats, cursor=stats_c, tmp=False):
	data = (msg.id, msg.guild.id if msg.guild is not None else 0, msg.channel.id if msg.channel is not None else None, msg.author.id, msg.created_at, msg.mention_everyone, 0, 1 if msg.author.bot else 0, None)
	
	cursor.execute("INSERT INTO messages VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", data)
	if not tmp:
		db.commit()
	
	sh.debug("Inserted message {} into the stat database".format(msg.id))

def update_msg_function(msg, funct, db=stats, cursor=stats_c, tmp=False):
	data = (funct, msg.id)
	
	cursor.execute("UPDATE messages SET function = ? WHERE message = ?", data)
	if not tmp:
		db.commit()
	
	sh.debug("Updated message function: {}".format(funct))

def update_msg_deletion(msg, db=stats, cursor=stats_c):
	data = (msg.id, )
	
	cursor.execute("UPDATE messages SET deleted = 1 WHERE message = ?", data)
	remove_emojis(msg, True)
	
	sh.debug("Deleted message {} from the stat database".format(msg.id))

def insert_emojis_post(msg, emojis, customs, edited=False, db=stats, cursor=stats_c, tmp=False):
	if edited:
		remove_emojis(msg)
	
	if len(emojis+customs) == 0:
		return
	
	emojis_ready = {}
	
	for e in emojis:
		if e in emojis_ready:
			emojis_ready[e]["count"] += 1
		else:
			emojis_ready[e] = {}
			emojis_ready[e]["name"] = e
			emojis_ready[e]["custom"] = 0
			emojis_ready[e]["count"] = 1
			
	for e in customs:
		if e in emojis_ready:
			emojis_ready[e]["count"] += 1
		else:
			emojis_ready[e] = {}
			emojis_ready[e]["name"] = e
			emojis_ready[e]["custom"] = 1
			emojis_ready[e]["count"] = 1
	
	for e in emojis_ready.values():
		data = (e["name"], msg.guild.id if msg.guild is not None else 0, msg.channel.id if msg.channel is not None else None, msg.id, msg.author.id, msg.created_at, e["count"], 0, e["custom"], 1 if msg.author.bot else 0)
		cursor.execute("INSERT INTO emojis VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", data)
	
	if not tmp:
		db.commit()
	
	sh.debug("Added emoji from post: {}".format(msg.id))

def insert_emojis_reaction(msg, user, emoji, custom, db=stats, cursor=stats_c, tmp=False):
	data = (emoji if not custom else str(emoji), msg.guild.id if msg.guild is not None else 0, msg.channel.id if msg.channel is not None else None, msg.id, user.id, msg.created_at, 1, 1, 1 if custom else 0, 1 if user.bot else 0)
	
	cursor.execute("INSERT INTO emojis VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", data)
	
	if not tmp:
		db.commit()
	
	sh.debug("Added reaction to post: {}".format(msg.id))

def remove_reaction(msg, user, emoji, custom, db=stats, cursor=stats_c):
	data = (emoji if not custom else str(emoji), msg.guild.id if msg.guild is not None else 0, msg.channel.id if msg.channel is not None else None, msg.id, user.id, msg.created_at, 1, 1, 1 if custom else 0, 1 if user.bot else 0)
	
	cursor.execute("DELETE FROM emojis WHERE emoji = ? AND server = ? AND channel = ? AND message = ? AND user = ? AND time = ? AND count = ? AND reaction = ? AND custom = ? AND bot = ?", data)
	db.commit()
	
	sh.debug("Removed reaction to post: {}".format(msg.id))

def remove_emojis(msg, all=False, db=stats, cursor=stats_c):
	data = (msg.id, )
	
	if not all:
		query = "AND reaction = 0"
	else:
		query = ""
	
	cursor.execute("DELETE FROM emojis WHERE message = ? {}".format(query), data)
	db.commit()
	
	sh.debug("Removed emojis from post: {}".format(msg.id))

# Helper functions

def generate_date_format(date):
	return {
		1 : "%Y-%m",
		2 : "%Y-%m-%d"
	}.get(date.count("-"), "%Y")

def line_split(line):
	return re.findall(r'(\S+[=:](".+?"|\'.+?\'|\S+))', line)

def parse_stats_args(client, message, args):
	# Default values
	ret_array = {
		"server" : message.guild.id if (message and message.guild) else 0,
		"time" : None,
		"channel" : None,
		"user" : None,
		"bot" : False,
		"everyone" : False,
		"emoji" : False,
		"omit_users" : False
	}
	
	# Argument name replacements
	repl_args = {
		"server" : r"serwer",
		"time" : r"czas|kiedy|when|data|date",
		"channel" : r"kana(l|ł)|gdzie|where",
		"user" : r"kto|auth?or|u(ż|z)ytkownik",
		"bot" : r"boty?",
		"emoji" : r"(wszystkie_)?emoji",
		"omit_users" : r"omit_users"
	}
	
	# Value replacements
	repl_values = {
		"time" : {
			"today" : r"dzisiaj|dzi(s|ś)",
			"yesterday" : r"wczoraj",
			"last_month" : r"zesz(l|ł)y_?miesi(a|ą)c",
			"this_month" : r"ten_?miesi(a|ą)c",
			"month" : r"miesi(a|ą)c"
		},
		"channel" : {
			(message.channel.id if message else 0) : r"ten|tu(taj)?|this|here"
		},
		"user" : {
			(message.author.id if message else 0) : r"me|ja"
		},
		"bot" : {
			True : r"t|tak|y|yes|true|1",
			False : r"n|no|nie|f|false|0"
		},
		"everyone" : {
			True : r"t|tak|y|yes|true|1",
			False : r"n|no|nie|f|false|0"
		},
		"emoji" : {
			True : r"t|tak|y|yes|true|1",
			False : r"n|no|nie|f|false|0"
		},
		"omit_users" : {
			True : r"t|tak|y|yes|true|1",
			False : r"n|no|nie|f|false|0"
		}
	}
	
	# Parsing each possible argument
	for arg in line_split(args):
		e = re.split("=|:", arg[0])
		
		if len(e) != 2:
			continue
		else:
			argument = e[0]
			value = e[1].strip('\'"')
			
			# Replace argument
			for k, v in repl_args.items():
				argument = re.sub("^"+v+"$", k, argument, flags=re.I)
			
			# Replace value
			if argument in repl_values:
				for k, v in repl_values[argument].items():
					value = re.sub("^"+v+"$", str(k), value, flags=re.I)
			
			# Convert to bool
			if argument in ["bot", "everyone"]:
						value = (value == "True")
			
			if argument in ret_array.keys():
				ret_array[argument] = value
	
	# Check if server exists
	if ret_array["server"] and not str(ret_array["server"]).isdigit():
		e = find(lambda m: re.search(ret_array["server"], m.name, flags=re.I), client.guilds)
		if e:
			ret_array["server"] = e.id
		else:
			ret_array["server"] = -1
	
	# Check if channel exists
	if ret_array["channel"] and not str(ret_array["channel"]).isdigit():
		e = find(lambda m: re.search(ret_array["channel"], m.name, flags=re.I), client.get_all_channels())
		if e:
			ret_array["channel"] = e.id
		else:
			ret_array["channel"] = -1
	
	# Check if user exists
	if ret_array["user"] and not str(ret_array["user"]).isdigit():
		e = find(lambda m: re.search(ret_array["user"], m.name, flags=re.I), client.get_all_members())
		if not e:
			e = find(lambda m: re.search(ret_array["user"], m.display_name, flags=re.I), client.get_all_members())
		
		if e:
			ret_array["user"] = e.id
		else:
			ret_array["user"] = -1
	
	# Handle errors
	ret_err = ""
	if ret_array["server"] == -1:
		ret_err += "Nie znaleziono podanego serwera.\n"
	if ret_array["channel"] == -1:
		ret_err += "Nie znaleziono podanego kanału.\n"
	if ret_array["user"] == -1:
		ret_err += "Nie znaleziono podanego użytkownika.\n"
	
	if len(ret_err) > 0:
		return ret_err.strip()

	# Convert strings to int
	for key in ret_array:
		value = ret_array[key]
		sh.debug("{}, {}, {}".format(key, value, type(value)))
		if isinstance(value, str) and value.isdigit():
			ret_array[key] = int(value)

	return ret_array

# Prepare conditions for the database query
def prepare_conditions(time=None, server=None, channel=None, user=None, bot=False, everyone=None, deleted=None, custom_only=None, function=None, omit_users=False):
	conditions = ""
	today = datetime.now()
	
	# Server conditions
	
	if server:
		conditions += "AND server = {} ".format(server)
	
	# Channel conditions
	
	if channel:
		conditions += "AND channel = {} ".format(channel)
	
	# Channel conditions
	
	if user:
		conditions += "AND user = {} ".format(user)
	
	# Time conditions
	
	if time == "yesterday":
		target_date = today - timedelta(days=1)
		conditions += "AND date(time, 'localtime') = '{}' ".format(target_date.strftime('%Y-%m-%d'))
	elif time == "today":
		conditions += "AND date(time, 'localtime') = '{}' ".format(today.strftime('%Y-%m-%d'))
		
	elif time != None and re.match(r"^\d+d$", time):
		target_date = today - timedelta(days=int(re.match(r"^(\d+)d$", time)[1]))
		conditions += "AND datetime(time, 'localtime') BETWEEN '{}' AND '{}' ".format(target_date.strftime('%Y-%m-%d %H:%M:%S'), today.strftime('%Y-%m-%d %H:%M:%S'))
	elif time != None and re.match(r"^\d+h$", time):
		target_date = today - timedelta(hours=int(re.match(r"^(\d+)h$", time)[1]))
		conditions += "AND datetime(time, 'localtime') BETWEEN '{}' AND '{}' ".format(target_date.strftime('%Y-%m-%d %H:%M:%S'), today.strftime('%Y-%m-%d %H:%M:%S'))
	
	elif time == "month":
		target_date = today - timedelta(days=30)
		conditions += "AND date(time, 'localtime') BETWEEN '{}' AND '{}' ".format(target_date.strftime('%Y-%m-%d'), today.strftime('%Y-%m-%d'))
	elif time == "this_month":
		conditions += "AND date(time, 'localtime') BETWEEN '{}-01' AND '{}' ".format(today.strftime('%Y-%m'), today.strftime('%Y-%m-%d'))
	elif time == "last_month":
		conditions += "AND strftime('%Y-%m', time, 'localtime') = '{}' ".format((today.replace(day=1)-timedelta(days=1)).strftime('%Y-%m'))
	
	elif time != None and time.count(",") == 1:
		tmp = time.split(",")
		dates = {
			"start" : False,
			"end" : False
		}
		
		if re.match(r"^\d{4}(-\d{2})?(-\d{2})?$", tmp[0]):
			dates["start"] = tmp[0]
		if re.match(r"^\d{4}(-\d{2})?(-\d{2})?$", tmp[1]):
			dates["end"] = tmp[1]
		
		if dates["start"] and dates["end"]:
			conditions += "AND date(time, 'localtime') BETWEEN '{}' AND '{}' ".format(dates["start"], dates["end"])
		elif dates["start"]:
			conditions += "AND date(time, 'localtime') > '{}' ".format(dates["start"])
		elif dates["end"]:
			conditions += "AND date(time, 'localtime') < '{}' ".format(dates["end"])
	
	elif time != None and re.match(r"^\d{4}(-\d{2})?(-\d{2})?$", time):
		date_format = generate_date_format(time)
		conditions += "AND strftime('{}', time, 'localtime') = '{}' ".format(date_format, time)
	
	# Ignore bot entries
	if not bot:
		conditions += "AND bot = 0 "
	
	# Select @everyone mentions
	if everyone:
		conditions += "AND everyone = 1 "
	
	# Omit deleted entries
	if deleted is not None and not deleted:
		conditions += "AND deleted = 0 "
	elif deleted:
		conditions += "AND deleted = 1 "
	
	# Select only bot function invocations
	if function is not None and function:
		conditions += "AND function IS NOT NULL "
	
	# Select only custom emojis
	if custom_only is not None and custom_only:
		conditions += "AND custom = 1 "
	
	# Omit users from regular stats
	if omit_users is not None and omit_users:
		conditions += "AND user NOT IN {} ".format(USERS_TO_OMIT)
	
	if len(conditions) == 0:
		return "WHERE 1=1"
	else:
		return "WHERE " + conditions[4:].strip()

# Generating stats

def stats_count_messages(server, time=None, channel=None, user=None, bot=True, everyone=None, deleted=False, functions=None, db=stats, cursor=stats_c):
	conditions = prepare_conditions(time, server, channel, user, bot, everyone, deleted, None, functions)
	query = "SELECT count(*) AS result FROM messages {}".format(conditions)
	sh.debug("[stats_count_messages] " + query)
	cursor.execute(query)
	return cursor.fetchone()[0]

def stats_count_emojis(server, time=None, channel=None, user=None, bot=True, custom_only=None, db=stats, cursor=stats_c):
	conditions = prepare_conditions(time, server, channel, user, bot, None, None, custom_only)
	query = "SELECT count(*) AS result FROM emojis {}".format(conditions)
	sh.debug("[stats_count_emojis] " + query)
	cursor.execute(query)
	return cursor.fetchone()[0]

def stats_users(client, server, rows=5, time=None, channel=None, user=None, bot=True, everyone=None, deleted=False, functions=None, omit_users=False, db=stats, cursor=stats_c):
	params = (rows,)
	conditions = prepare_conditions(time, server, channel, user, bot, everyone, deleted, None, functions, omit_users)
	ret = ""
	
	i = 1
	query = "SELECT user, count(*) AS result FROM messages {} GROUP BY user ORDER BY result DESC, user ASC LIMIT 0,?".format(conditions)
	sh.debug("[stats_users] " + query)
	for row in cursor.execute(query, params):
		user = discord.utils.get(client.get_all_members(), id=row[0], guild__id=int(server)) or discord.utils.get(client.get_all_members(), id=row[0])
		ret += "#{}: {} ({})\n".format(i, re.sub(r"([~*_`>|])", r"\\\g<1>", user.display_name) if user is not None else NOT_FOUND, row[1])
		i += 1
	
	return ret.strip()

def stats_channels(client, server, rows=5, time=None, channel=None, user=None, bot=True, everyone=None, deleted=False, functions=None, db=stats, cursor=stats_c):
	params = (rows,)
	conditions = prepare_conditions(time, server, channel, user, bot, everyone, deleted, None, functions)
	ret = ""
	
	i = 1
	query = "SELECT channel, count(*) AS result FROM messages {} AND channel NOT IN {} GROUP BY channel ORDER BY result DESC, channel ASC LIMIT 0,?".format(conditions, CHANNELS_TO_OMIT)
	sh.debug("[stats_channels] " + query)
	for row in cursor.execute(query, params):
		channel = discord.utils.get(client.get_all_channels(), id=row[0])
		ret += "#{}: {} ({})\n".format(i, channel.name if channel is not None else NOT_FOUND, row[1])
		i += 1
	
	return ret.strip()

def stats_functions(client, server, rows=5, time=None, channel=None, user=None, bot=True, deleted=False, db=stats, cursor=stats_c):
	params = (rows,)
	conditions = prepare_conditions(time, server, channel, user, bot, None, deleted, None, True)
	ret = ""
	
	i = 1
	query = "SELECT function, count(*) AS result FROM messages {} GROUP BY function ORDER BY result DESC, channel ASC LIMIT 0,?".format(conditions)
	sh.debug("[stats_functions] " + query)
	for row in cursor.execute(query, params):
		ret += "#{}: {} ({})\n".format(i, row[0], row[1])
		i += 1
	
	return ret.strip()

def stats_emojis(client, server, rows=5, time=None, channel=None, user=None, bot=False, custom_only=False, db=stats, cursor=stats_c):
	params = (rows, )
	#server_obj = client.get_guild(server)
	conditions = prepare_conditions(time, server, channel, user, bot, None, None, custom_only)
	ret = ""
	
	#if not server:
	#	return "Coś skopałeś z ID serwera"
	
	i = 1
	query = "SELECT emoji, sum(count) AS result FROM emojis {} GROUP BY emoji ORDER BY result DESC, emoji ASC LIMIT 0,?".format(conditions)
	sh.debug("[stats_emojis] " + query)
	for row in cursor.execute(query, params):
		ret += "#{}: {} ({})\n".format(i, row[0], row[1])
		i += 1
	
	return ret.strip()

# Generate stats

def generate_stats(client, message, channel, arguments, stat_limit=5, bot_stats=False, hide_args=False, db=stats, cursor=stats_c):
	ret = ""
	
	query_args = parse_stats_args(client, message, arguments)
	
	# Some errors were found
	if isinstance(query_args, str):
		return query_args
	
	args_display = ""
	
	if not hide_args and (query_args["time"] is not None or query_args["channel"] is not None or query_args["user"] is not None or query_args["bot"] or query_args["everyone"]):
		args_display += "\n["
		
		if query_args["server"] is not None:
			args_display += "serwer: *{}*, ".format((client.get_guild(query_args["server"]).name if query_args["server"] != 0 else "prywatna wiadomość"))
		
		if query_args["channel"] is not None:
			ch = client.get_channel(query_args["channel"])
			if hasattr(ch, "name"):
				args_display += "kanał: *{}*, ".format(ch.name)
		
		if query_args["user"] is not None:
			args_display += "użytkownik: *{}*, ".format(discord.utils.get(client.get_all_members(), id=query_args["user"]).display_name)
		
		if query_args["time"] is not None:
			args_display += "czas: *{}*, ".format(query_args["time"])
		
		if (query_args["bot"] or query_args["user"]) is not None:
			args_display += "boty: *{}*, ".format((query_args["bot"] or not not query_args["user"]))
		
		if query_args["everyone"]:
			args_display += "everyone: *{}*, ".format(query_args["everyone"])
		
		if query_args["emoji"]:
			args_display += "wszystkie emoji: *{}*, ".format(query_args["emoji"])
			
		args_display = args_display[:-2] + "]"
	
	result_count = stats_count_messages(query_args["server"], time=query_args["time"], channel=query_args["channel"], user=query_args["user"], bot=(query_args["bot"] or query_args["user"]), everyone=query_args["everyone"], deleted=False, functions=bot_stats, db=db, cursor=cursor)
	
	# Message stats
	
	if result_count == 0:
		ret += "Brak wiadomości dla zadanych parametrów.{}".format(args_display)
	else:
		deleted_count = stats_count_messages(query_args["server"], time=query_args["time"], channel=query_args["channel"], user=query_args["user"], bot=(query_args["bot"] or query_args["user"]), everyone=query_args["everyone"], deleted=True, functions=bot_stats, db=db, cursor=cursor)
		ret += "Łącznie **{}** wiadomości (oraz {} usuniętych).{}".format(result_count, deleted_count, args_display)
		
		if not query_args["user"]:
			ret += ("\n\n*Najwięksi męczyciele bota:*\n\n" if bot_stats else "\n\n*Najwięksi spamerzy:*\n\n")
			
			ret += stats_users(client, query_args["server"], rows=stat_limit, time=query_args["time"], channel=query_args["channel"], user=query_args["user"], bot=(query_args["bot"] or query_args["user"]), everyone=query_args["everyone"], deleted=False, omit_users=query_args["omit_users"], functions=bot_stats, db=db, cursor=cursor)
		
		if not query_args["channel"] and query_args["server"] != 0:
			ret += "\n\n*Najbardziej zaspamowane kanały:*\n\n"
			
			ret += stats_channels(client, query_args["server"], rows=stat_limit, time=query_args["time"], channel=query_args["channel"], user=query_args["user"], bot=(query_args["bot"] or query_args["user"]), everyone=query_args["everyone"], deleted=False, functions=bot_stats, db=db, cursor=cursor)
		
		if bot_stats:
			ret += "\n\n*Najczęściej używane funkcje:*\n\n"
			
			ret += stats_functions(client, query_args["server"], rows=stat_limit, time=query_args["time"], channel=query_args["channel"], user=query_args["user"], bot=(query_args["bot"] or query_args["user"]), deleted=False, db=db, cursor=cursor)
	
	# Emoji stats
	
	if not bot_stats and not query_args["everyone"]:
		result_count = stats_count_emojis(query_args["server"], time=query_args["time"], channel=query_args["channel"], user=query_args["user"], bot=(query_args["bot"] or query_args["user"]), custom_only=(not query_args["emoji"]), db=db, cursor=cursor)
		
		if result_count == 0:
			ret += "\n\nBrak emotikon dla zadanych parametrów."
		else:
			ret += "\n\n*Najczęściej używane emoty:*\n\n"
			
			ret += stats_emojis(client, query_args["server"], rows=stat_limit, time=query_args["time"], channel=query_args["channel"], user=query_args["user"], bot=(query_args["bot"] or query_args["user"]), custom_only=(not query_args["emoji"]), db=db, cursor=cursor)
	
	return ret

# Commands

async def c_stats(client, message):
	stat_limit = STATS_CHANNELS_MORE_RESULTS_COUNT if (message.channel.id in STATS_CHANNELS_MORE_RESULTS) else STATS_RESULTS_COUNT
	bot_stats = True if "bot" in sh.get_command(message).lower() else None
	
	mmmsmsm = generate_stats(client, message, message.channel, sh.get_args(message), stat_limit, bot_stats)
	await message.reply(mmmsmsm)

c_stats.command = r"(bot|stat)(s|ystyki)"
c_stats.desc = "hidden"


async def c_stattest2(client, message):
	await t_daily_stats(client, [message.channel])

c_stattest2.command = r"stat_test"
c_stattest2.desc = "hidden"

# Daily stats

async def t_daily_stats(client, channels):
	yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
	ret = "Statystyki z dnia **{}**\n".format(yesterday)
	
	for ch in channels:
		await ch.send(ret + generate_stats(client, None, ch, "time=yesterday server=politbiuro omit_users=1", STATS_RESULTS_COUNT, hide_args=True))

t_daily_stats.channels = [174449535811190785]
t_daily_stats.time = "00:01"

# Weekly stats

async def t_weekly_stats(client, channels):
	if datetime.now().weekday() == 0:
		last_monday = (datetime.now()-timedelta(days=7)).strftime('%Y-%m-%d')
		yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
		ret = "Statystyki z zeszłego tygodnia (od **{}** do **{}**)\n".format(last_monday, yesterday)
		
		for ch in channels:
			await ch.send(ret + generate_stats(client, None, ch, "time={},{} server=politbiuro omit_users=1".format(last_monday, yesterday), STATS_CHANNELS_MORE_RESULTS_COUNT, hide_args=True))

t_weekly_stats.channels = [174449535811190785]
t_weekly_stats.time = "00:11"

# Monthly stats

async def t_monthly_stats(client, channels):
	if datetime.now().strftime('%d') == "01":
		last_month = (datetime.now() - timedelta(days=1)).strftime('%Y-%m')
		ret = "Statystyki z zeszłego miesiąca (**{}**)\n".format(last_month)
		
		for ch in channels:
			await ch.send(ret + generate_stats(client, None, ch, "time=last_month server=politbiuro omit_users=1", STATS_CHANNELS_MORE_RESULTS_COUNT, hide_args=True))

t_monthly_stats.channels = [174449535811190785]
t_monthly_stats.time = "00:21"

# Yearly stats

async def t_yearly_stats(client, channels):
	if datetime.now().strftime('%m-%d') == "01-01":
		last_year = (datetime.now() - timedelta(days=1)).strftime('%Y')
		ret = "Statystyki z zeszłego roku (**{}**)\n".format(last_year)
		
		for ch in channels:
			await ch.send(ret + generate_stats(client, None, ch, "time={}-01-01,{}-12-31 server=politbiuro omit_users=1".format(last_year, last_year), STATS_CHANNELS_MORE_RESULTS_COUNT, hide_args=True))

t_yearly_stats.channels = [174449535811190785]
t_yearly_stats.time = "00:31"