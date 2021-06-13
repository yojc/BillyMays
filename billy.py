# Modules to import
python_modules = [
	"discord", 
	"asyncio",
	"platform",
	
	"sys",
	"argparse",
	"random",
	"re",
	"datetime",
	"emoji",
	"unidecode",
	"signal"
	]

for m in python_modules:
	globals()[m] = __import__(m)

# Bot dependencies
from discord.ext.commands import Bot
from discord.ext import commands

# Read command line arguments
parser = argparse.ArgumentParser(description="Just some Discord bot.")
parser.add_argument("-b", "--debug", help="enable simple debug messages", action="store_true")
parser.add_argument("-l", "--list", help="list all imported functions on startup", action="store_true")
parser.add_argument("-n", "--nostats", help="startup mode: disabled statistics module", action="store_true")
parser.add_argument("-s", "--stats", help="startup mode: statistics module ONLY", action="store_true")
parser.add_argument("-d", "--dev", help="startup mode: developer. Disables all modules (except billy_c_dev_*.py) and applies --list and --debug. Accepts commands only from bot owner(s). All functions use dev_ prefix! (eg. .dev_help)", action="store_true")

args = parser.parse_args()

NOSTATS_MODE = args.nostats
STATS_MODE = args.stats
DEBUG_MODE = args.debug
DEV_MODE = args.dev
LIST_FUNCTIONS = args.list

if DEV_MODE and (NOSTATS_MODE or STATS_MODE):
	print("Developer mode is meant to be used as a standalone parameter")
	sys.exit(2)
elif NOSTATS_MODE and STATS_MODE:
	print("--nostats and --stats are mutually exclusive")
	sys.exit(2)

# App keys
from keys import BILLY_KEY

from config import BOT_OWNERS, BOT_PREFIX

# Shared functions

import billy_antiflood as af
import billy_shared as sh
#import billy_roles as roles

if DEV_MODE or DEBUG_MODE:
	sh.set_debug_flag()

if STATS_MODE:
	sh.warn("Stats collection mode only enabled!")
elif NOSTATS_MODE:
	sh.warn("Stats module is completely disabled!")
elif DEV_MODE:
	# Import all modules starting with billy_c_dev
	for m in sh.list_modules(dev=True):
		globals()[m] = __import__(m)

	sh.warn("DEVELOPER MODE ENABLED!")

if DEBUG_MODE and not DEV_MODE:
	sh.warn("Debug info enabled!")

# Import all modules starting with billy_c

if not (DEV_MODE or STATS_MODE):
	for m in sh.list_modules():
		globals()[m] = __import__(m)

if not (DEV_MODE or NOSTATS_MODE):
	import billy_c_stats
else:
	# Ugly hack, don't look
	billy_c_stats = None


print("--------")

# Here you can modify the bot's prefix and description and wether it sends help in direct messages or not.
client = Bot(description="Hi, Billy Mays here", command_prefix=BOT_PREFIX, pm_help = True, intents=discord.Intents().all())

# Used to run timer-based function once a day
current_day = {}

# To prevent multiple reminder setup
sopel_reminder_setup = False

def compile_command(regex):
	return client.command_prefix + ("dev_" if DEV_MODE else "") + regex + r"\b"

# Filling in commands/triggers list

c_functions = [] # commands
f_functions = [] # fulltext
t_functions = [] # timer-based

modules = list(set(sys.modules) & set(globals()))

for module_name in modules:
	if module_name.startswith("billy_c_"):
		i = 0
		module = sys.modules[module_name]
		
		for name, val in module.__dict__.items():
			if callable(val) and name.startswith(("c_", "f_", "t_")):
				if name.startswith("t_"):
					if hasattr(val, "time") and not re.match(r"([0-9]|[0-1][0-9]|2[0-3])\:[0-5][0-9]", getattr(val, "time")):
						sh.warn("Invalid specified time: " + name)
						continue
					elif not hasattr(val, "channels"):
						sh.warn("No channels specified: " + name)
						continue
					else:
						# Timer functions functions
						if (DEV_MODE or LIST_FUNCTIONS):
							sh.debug("Imported timer: " + name)
						t_functions.append(val)
						i += 1
				
				elif not hasattr(val, "command"):
					# Omit functions without specified .command
					sh.warn("Missing command regex: " + name)
					continue
				
				elif name.startswith("f_") and not hasattr(val, "prob"):
					# Omit fulltext without specified .prob
					sh.warn("Missing fulltext probability: " + name)
					continue
				
				elif name.startswith("c_"):
					# Called functions
					if (DEV_MODE or LIST_FUNCTIONS):
						sh.debug("Imported command: " + name)
					c_functions.append(val)
					i += 1
				
				elif name.startswith("f_"):
					# Fulltext search
					if (DEV_MODE or LIST_FUNCTIONS):
						sh.debug("Imported fulltext: " + name)
					f_functions.append(val)
					i += 1
			
		print("Loaded " + str(i) + " functions from module " + module_name)
	else:
		if module_name not in python_modules:
			sh.debug("Probably not a module: " + module_name)

# Start timer tasks

for e in t_functions:
	async def f(fun):
		global client
		global current_day
		await client.wait_until_ready()
		
		if hasattr(fun, "time"):
			t = list(map(int, getattr(fun, "time").split(":")))
		else:
			t = False
		
		channels = []
		tmp = getattr(fun, "channels")
		for e in tmp:
			channels.append(client.get_channel(e))
		
		interval = getattr(fun, "interval", 30)
		
		while not client.is_closed():
			now = datetime.datetime.now()
			
			if (not t and interval != 30):
				await fun(client, channels)
			elif (not fun.__name__ in current_day or current_day[fun.__name__] != now.day) and (not t or (t[0] == now.hour and t[1] == now.minute)):
				current_day[fun.__name__] = now.day
				await fun(client, channels)
			
			await asyncio.sleep(interval)
	
	client.loop.create_task(f(e))

# Parse message and execute functions

async def parse_message(message, edited=False):
	if DEV_MODE and message.author.id not in BOT_OWNERS:
		#sh.debug("Received and ignored a message")
		return

	if not (DEV_MODE or NOSTATS_MODE):
		if not edited:
			billy_c_stats.insert_msg(message)
		
		# Track used emojis
		
		emoji_list = list(c for c in message.clean_content if c in emoji.UNICODE_EMOJI) or []
		custom_emoji_list = re.findall(r"<:\S+?:\d+>", message.clean_content, re.IGNORECASE) or []
		billy_c_stats.insert_emojis_post(message, emoji_list, custom_emoji_list, edited)
	
	# Ignore bot messages
	
	if message.author == client.user:
		return
	
	perm = af.check_channel_whitelist(client, message)
	
	# Channel blacklisted
	
	if perm["disallow"]:
		return
	
	# Strip quotes
	content = unidecode.unidecode(sh.rm_leading_quotes(message))
	
	
	if not edited:
		# Fulltext search
		for f in f_functions:
			c = getattr(f, "command", False)
			p = getattr(f, "prob", False)
			
			if c and p and re.search(c, content, re.IGNORECASE) and (p >= 1.0 or (perm["fulltext"] and random.random() < p)):
				sh.debug("Triggered " + f.__name__ + "...")
				try:
					await f(client, message)
				except Exception:
					sh.warn("An error occured in " + f.__name__ + "!!! (" + content + ")")
					raise
					
	# Commands
	
	if re.match(client.command_prefix, content) and sh.get_command(message):
		sh.debug("This seems to be a command: ." + sh.get_command(message))
		
		# Check antiflood
		
		if not (STATS_MODE or DEV_MODE) and perm["flood"] and ((await af.check_flood_channel(client, message)) or (await af.check_flood(client, message))):
			sh.debug("Anti-flood kicked in yo")
			return
		
		# Help
		
		if not STATS_MODE and re.match(compile_command(r"(help|pomoc)"), content, re.IGNORECASE):
			ret = "Witam witam, z tej strony Billy Mays z kolejnym fantastycznym produktem!\nDozwolone przedrostki funkcji: . , \ / ! ;\n\n"
			
			for f in c_functions:
				desc = getattr(f, "desc", False)
				
				if hasattr(f, "rhyme") or desc == "hidden":
					continue
					
				command = getattr(f, "command", False)
				
				ret += "." + getattr(f, "command")
				
				params = getattr(f, "params", False)
				
				if params:
					for p in params:
						ret += " [" + p + "]"
				
				if desc:
					ret += " - " + desc
				
				ret += "\n"
			
			ret += "\nRymy i inne bzdety: .rymy"
			ret += "\nZadzwoń teraz, a podwoimy ofertę!"
			
			if len(ret) > 2000:
				n = 40
				groups = ret.split("\n")
				help = ["\n".join(groups[:n]), "\n".join(groups[n:n*2]), "\n".join(groups[n*2:])]
			else:
				help = [ret]
			
			for m in help:
				await message.channel.send(m)
		
		elif not STATS_MODE and re.match(compile_command(r"(rymy|rhymes)"), content, re.IGNORECASE):
			ret = "Rymy i inne bzdety:\n"
			
			for f in c_functions:
				if not hasattr(f, "rhyme"):
					continue
				command = getattr(f, "command", False)
				ret += "." + getattr(f, "command") + "\n"
			
			await message.channel.send(ret[:-1])
		
		else:
			# Iterate over functions
			for f in c_functions:
				c = getattr(f, "command", False)
				r = re.match(compile_command(c), content, re.IGNORECASE)
				if c and r:
					sh.debug("Executing " + f.__name__ + "...")
					async with message.channel.typing():
						pass

					try:
						await f(client, message)

						if not (NOSTATS_MODE or DEV_MODE):
							billy_c_stats.update_msg_function(message, f.__name__)
					except Exception as e:
						reply_msg = "Oho, chyba coś się zepsuło."

						if BOT_OWNERS and BOT_OWNERS[0] and message.guild and message.guild.get_member(BOT_OWNERS[0]):
							yojec_action = ["się skończy bawić pociągami", "wyłączy w końcu Bordery", "skończy magisterkę", "wróci z rowerowej wycieczki", "mu się zachce albo i nie"]
							reply_msg += " <@{}> to kiedyś naprawi, jak {}.".format(BOT_OWNERS[0], random.choice(yojec_action))

						await message.reply(reply_msg + "\n```{}```".format(str(e)))
						sh.warn("An error occured in " + f.__name__ + "!!! (" + content + ")")
						raise
						continue
					break
			
			# If stats mode only: import function names from database
			if STATS_MODE:
				for f in sh.get_function_names():
					c = sh.function_list[f]
					r = re.match(compile_command(c), content, re.IGNORECASE)
					if c and r:
						sh.debug("Adding " + f + " to stat database...")
						try:
							billy_c_stats.update_msg_function(message, f)
						except Exception:
							sh.warn("Stat database msg update error " + f + "!!! (" + content + ")")
							raise
							continue
						break


# Sort functions alphabetically (for .help)
c_functions.sort(key=lambda x: x.__name__)

# Dump function names to file
if not (STATS_MODE or DEV_MODE):
	sh.dump_function_names(c_functions)

print("--------")

# Start the bot and display startup info
@client.event
async def on_ready():
	global sopel_reminder_setup
	
	print('Logged in as '+client.user.name+' (ID:'+str(client.user.id)+') | Connected to '+str(len(client.guilds))+' servers | Connected to '+str(len(set(client.get_all_members())))+' users')
	print('Connection datetime: ' + str(datetime.datetime.now()))
	print('--------')
	sh.debug('Current Discord.py Version: {} | Current Python Version: {}'.format(discord.__version__, platform.python_version()))
	sh.debug('--------')
	#print('Use this link to invite {}:'.format(client.user.name))
	#print('https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=8'.format(client.user.id))
	#print('--------')
	
	if not (DEV_MODE or STATS_MODE) and not sopel_reminder_setup:
		sh.debug("### CREATED REMINDER TASKS " + str(datetime.datetime.now()))
		sopel_reminder_setup = True
		await billy_c_sopel_remind.setup(client)
	elif DEV_MODE:
		sh.debug("### REMINDERS DISABLED IN DEVELOPER MODE")
	else:
		sh.debug("### REMINDERS ALREADY ACTIVE")
	
#	# Update user role database
#	if not (STATS_MODE):
#		from billy_roles import dump_roles
#		dump_roles(client)
		


# Execute on every reaction

@client.event
async def on_reaction_add(reaction, user):
	if reaction.me:
		return
	elif not (NOSTATS_MODE or DEV_MODE):
		# Track used emojis
		billy_c_stats.insert_emojis_reaction(reaction.message, user, reaction.emoji, reaction.custom_emoji)
	
	#if random.random() < 0.001:
	#	await asyncio.sleep(4)
	#	await client.add_reaction(reaction.message, reaction.emoji)

@client.event
async def on_reaction_remove(reaction, user):
	if not (NOSTATS_MODE or DEV_MODE):
		# Track used emojis
		billy_c_stats.remove_reaction(reaction.message, user, reaction.emoji, reaction.custom_emoji)


# Execute on every msg edit

@client.event
async def on_message_edit(before, after):
	if before.content == after.content:
		return
	
	if re.match(client.command_prefix, before.content):
		await handle_bot_response_deletion(before)

	await parse_message(after, True)

# Execute on every msg

@client.event
async def on_message(message):
	await parse_message(message)

# Handle reponse deletion

@client.event
async def on_message_delete(message):
	if not (NOSTATS_MODE or DEV_MODE):
		billy_c_stats.update_msg_deletion(message)
	
	content = sh.rm_leading_quotes(message)
	
	if message.author == client.user:
		sh.debug("Deleted bot message: " + message.content, message)
		return
	elif not message.guild:
		sh.debug("Deleted private message: " + message.content, message)
		return
	elif not re.match(client.command_prefix, content):
		sh.debug("Deleted regular message: " + message.content, message)
		return
	
	sh.debug("User command deleted: " + message.content, message)
	#sh.debug("message.id : {}".format(message.id))
	#sh.debug("client.user : {}".format(client.user))

	await handle_bot_response_deletion(message)
	
async def handle_bot_response_deletion(message):
	async for log in message.channel.history(limit=50, after=message):
		#sh.debug("log.author : {}".format(log.author))
		#sh.debug("log.reference : {}".format(log.reference))
		#sh.debug("log.reference.message_id : {}".format(log.reference.message_id))
		if log.author != client.user:
			sh.debug("Not a bot message - skipped")
			continue
		elif not log.reference:
			sh.debug("Bot message without reference - skipped")
			continue
		if log.reference.message_id != message.id:
			sh.debug("Different message referenced - skipped")
			continue
		
		sh.debug("Found a message to delete: " + log.content, log)
		
		await log.delete()
		return
	
	sh.warn("Bot command deleted, no matching response found? " + message.content)

# Handle member profile change

@client.event
async def on_member_update(before, after):
	attribute_list = ["status", "activity", "display_name", "roles", "pending"]
	changed_attributes = ""

	for attr in attribute_list:
		if getattr(before, attr) != getattr(after, attr):
			changed_attributes += attr + ", "

	if changed_attributes:
		changed_attributes = changed_attributes[:-2]
	else:
		changed_attributes = "[UNKNOWN?]"

	sh.debug("{} ({}) changed their profile, specifically: {}".format(after, after.guild.name, changed_attributes))

# Handle member join/leave

@client.event
async def on_member_join(member):
	if not (STATS_MODE or DEV_MODE) and member.guild.system_channel:
		invitation_msg = "Witam witam {} na naszym magicznym serwerze!".format(member.mention)
		
		if member.guild.id == 174449535811190785:
			await member.guild.system_channel.send(content=invitation_msg, file=discord.File(sh.file_path("img/w mcdonalds spotkajmy sie.jpg")))
			await member.guild.system_channel.send("(lepiej nie pytaj kto to jest)")
		else:
			await member.guild.system_channel.send(invitation_msg)

@client.event
async def on_member_remove(member):
	if not (STATS_MODE or DEV_MODE) and member.guild.system_channel:
		word = "polazła" if sh.is_female(member) else "polazł"

		leave_msg = "{} ({}) właśnie se stąd gdzieś {}".format(member.mention, str(member), word)

		if member.guild.id == 174449535811190785:
			leave_msg += " <:smaglor:328947669676457984>"
		
		await member.guild.system_channel.send(leave_msg)

# Start the bot

client.run(BILLY_KEY)

# Catch SIGINT

def signal_handler(sig, frame):
	print("SIGINT CAUGHT")
	sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)