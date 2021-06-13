import asyncio
import datetime
import time

import os
import glob

import billy_shared as sh

from config import ANTIFLOOD_MSG_LIMIT, ANTIFLOOD_TIME_LIMIT, ANTIFLOOD_CHANNELS_DENY_ALL, ANTIFLOOD_CHANNELS_FULLTEXT, ANTIFLOOD_CHANNELS_UNLIMITED

start_time = time.time()
check = {}

async def check_flood(client, message):
	sh.debug("Checking for flood...")
	if sh.april_fools():
		msg_limit = 1
		time_limit = 1
	else:
		msg_limit = ANTIFLOOD_MSG_LIMIT	# messages per channel
		time_limit = ANTIFLOOD_TIME_LIMIT	# minutes
	
	if message.channel not in check:
		# channel not tracked yet
		check[message.channel] = {}
	
	if message.author not in check[message.channel]:
		# author on channel not tracked yet:
		check[message.channel][message.author] = {}
		check[message.channel][message.author]["timestamps"] = []
		check[message.channel][message.author]["warning_issued"] = False
	
	if len(check[message.channel][message.author]["timestamps"]) < msg_limit:
		# less than limit messages sent
		sh.debug("Message number " + str(len(check[message.channel][message.author]["timestamps"])+1))
		check[message.channel][message.author]["timestamps"].append(time.time())
		return False
	
	else:
		time_diff = time.time() - check[message.channel][message.author]["timestamps"][0]
		if time_diff > (time_limit*60):
			# message older than time limit
			sh.debug("Message number " + str(msg_limit) + "; deleted timestamp " + str(check[message.channel][message.author]["timestamps"][0]), message)
			check[message.channel][message.author]["timestamps"].pop(0)
			check[message.channel][message.author]["timestamps"].append(time.time())
			check[message.channel][message.author]["warning_issued"] = False
			return False
		else:
			if check[message.channel][message.author]["warning_issued"] == False:
				# scold user for spamming
				sh.debug("This user is spamming!")
				if sh.april_fools():
					await message.reply("Wykorzystał{}ś już wszystkie BillyMays(TM) Token. Aby korzystać dalej z bota, doładuj swoje konto lub wykup usługę BillyMays(TM) Premium.".format("a" if sh.is_female(message.author) else "e"))
				else:
					await message.reply("Zamknij pizdę przez " + datetime.datetime.utcfromtimestamp((time_limit*60)-time_diff).strftime("%Mmin %Ss") + ". Spamuj w <#386148571529084929>")
				check[message.channel][message.author]["warning_issued"] = True
				return True
			else:
				# ...but just once
				sh.debug("This user is still spamming!")
				return False

# This function doesn't seem to work, not like it's needed anyway
async def check_flood_channel(client, message):
	sh.debug("Checking for channel flood...")
	msg_limit = 5    # messages per channel
	time_limit = 1    # minutes
	
	if message.channel not in check:
		# channel not tracked yet
		check[message.channel] = {}
		check[message.channel]["timestamps"] = []
		check[message.channel]["warning_issued"] = False
	
	if len(check[message.channel]["timestamps"]) < msg_limit:
		# less than limit messages sent
		sh.debug("Channel message number " + str(len(check[message.channel]["timestamps"])+1))
		check[message.channel]["timestamps"].append(time.time())
		return False
	
	else:
		time_diff = time.time() - check[message.channel]["timestamps"][0]
		if time_diff > (time_limit*60):
			# message older than time limit
			sh.debug("Channel message number " + str(msg_limit) + "; deleted timestamp " + str(check[message.channel]["timestamps"][0]), message)
			check[message.channel]["timestamps"].pop(0)
			check[message.channel]["timestamps"].append(time.time())
			check[message.channel]["warning_issued"] = False
			return False
		else:
			if check[message.channel]["warning_issued"] == False:
				# scold these idiots for spamming
				sh.debug("This channel is being flooded!")
				message.channel.send("Weźcie wszyscy sklejcie pizdy przez " + datetime.datetime.utcfromtimestamp((time_limit*60)-time_diff).strftime("%Mmin %Ss") + ". Od spamowania jest <#386148571529084929>")
				check[message.channel]["warning_issued"] = True
				return True
			else:
				# ...but just once
				sh.debug("This channel is still being flooded!")
				return False

def check_channel_whitelist(client, message):
	deny_all = ANTIFLOOD_CHANNELS_DENY_ALL
	allow_fulltext = ANTIFLOOD_CHANNELS_FULLTEXT
	unlimited = ANTIFLOOD_CHANNELS_UNLIMITED
	
	# default: disallow fulltext, enable flood control, enable bot
	permissions = {"fulltext" : False, "flood" : True, "disallow" : False}

	msg_details = ""
	
	if str(message.channel).startswith("Direct Message"):
		msg_details += "private, "
		permissions["flood"] = False
		permissions["fulltext"] = True
		
	else:
		if message.channel.id in deny_all:
			msg_details += "blacklisted, "
			permissions["disallow"] = True
			
		if message.channel.id in allow_fulltext:
			msg_details += "whitelisted, "
			permissions["fulltext"] = True
			
		if message.channel.id in unlimited:
			msg_details += "unlimited, "
			permissions["flood"] = False
	
	if msg_details:
		sh.debug("Message: ({})".format(msg_details[:-2]), message)
	else:
		sh.debug("Message:", message)
	
	return permissions


def check_uptime():
	list_of_files = glob.glob(sh.file_path("billy*.py"))
	latest_file = max(list_of_files, key=os.path.getmtime)
	
	ret = "Żyję już od " + str((datetime.datetime.today()-datetime.datetime.utcfromtimestamp(start_time)).days).zfill(2) + datetime.datetime.utcfromtimestamp(time.time()-start_time).strftime("d %Hh %Mmin %Ss") + "!\n"
	ret += "Ostatnia aktualizacja: " + datetime.datetime.fromtimestamp(int(os.path.getmtime(latest_file))).strftime('%Y-%m-%d %H:%M:%S') + " (" + latest_file + ")"
	return ret