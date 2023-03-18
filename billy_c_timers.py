import random
import asyncio
import os

import billy_shared as sh
from config import BOT_OWNERS, OUTPUTTER_FILENAMES, MESSAGE_LENGTH_LIMIT

# -------------------------------------
# To execute on specified times/interval
# -------------------------------------


#@asyncio.coroutine
#def t_pope_time(client, channels):
#	choices = ["zapraszam wszystkich na kremówki", "wybiła godzina papieska", "Jan Paweł 2, w moim sercu zawsze 1", "Jan Paweł II był wielkim człowiekiem", "Jan Paweł 2 Gloria Matki Dziewicy"]
#	barka = [("Pan kiedyś stanął nad brzegiem,\n" +
#		"Szukał ludzi gotowych pójść za Nim;\n" +
#		"By łowić serca\n" +
#		"Słów Bożych prawdą.\n\n" +
#		"Ref.: \n" +
#		"O Panie, to Ty na mnie spojrzałeś,\n" +
#		"Twoje usta dziś wyrzekły me imię.\n" +
#		"Swoją barkę pozostawiam na brzegu,\n" +
#		"Razem z Tobą nowy zacznę dziś łów."), (("O"*random.randint(3, 10)) + " P" + ("A"*random.randint(5,15)) + "NI" + ("E"*random.randint(5,15)))]
#	
#	reply = random.choice([random.choice(choices), random.choice(barka)])
#	
#	for ch in channels:
#		#await ch.send(reply)
#		await ch.send("Jebać PiS")
#
#t_pope_time.channels = [174449535811190785]
#t_pope_time.time = "21:37"

def random_a():
	return "A"*random.randint(3,7)

async def t_trzytrzytrzy(client, channels):
	
	choices = ["https://www.youtube.com/watch?v=20GkBnhQqY0", "https://www.youtube.com/watch?v=WX8ZeZJqOE0", "https://www.youtube.com/watch?v=rRctiUI8pmE", "https://www.youtube.com/watch?v=IJKWUTgrE2g", "https://www.youtube.com/watch?v=UskQs90Y2TE", "pac"]
	
	reply = random.choice(choices)
	for ch in channels:
		if random.random() < 0.075:
			if reply == "pac":
				await ch.send("O K{}T{}J\nTO TY MNIE POPAC{}Ł{}Ś".format(random_a(), random_a(), random_a(), random_a()))
			else:
				await ch.send(reply)

t_trzytrzytrzy.channels = [174449535811190785]
t_trzytrzytrzy.time = "3:33"


# Sends file contents from disk

outputter_file_db = {}

def resolve_filename(name):
	if name.startswith(".") or name.startswith("/"):
		return name
	else:
		return sh.file_path(name)

async def t_outputter(client, channels):
	for name in OUTPUTTER_FILENAMES:
		#sh.debug("Trying to output file {}".format("name"))
		filename = resolve_filename(name)
		#sh.debug("Filename resolved to {}".format(filename))

		if os.path.isfile(filename):
			user_id = BOT_OWNERS[0]

			try:
				sh.debug("Calling get_user...")
				dest_user = client.get_user(user_id)
			except Exception:
				sh.warn("Output destination user not found (get_user failed)! {}".format(user_id), date=True)
				continue

			if not dest_user:
				sh.warn("Output destination user not found (dest_user is None)! {}, {}".format(user_id), date=True)
				continue
			
			dest_channel = dest_user.dm_channel

			if not dest_channel:
				sh.debug("dm_channel is None! Creating DM...")
				dest_channel = await dest_user.create_dm()

				if not dest_channel:
					sh.warn("create_dm falied! This output was aborted")

			output_messages = ["**{}**\n".format(name)]
			current_output_message = 0

			sh.debug("Iterating over lines...")

			with open(filename, "r", encoding="utf-8") as source_file:
				for line in source_file:
					if len(output_messages[current_output_message] + line) > MESSAGE_LENGTH_LIMIT:
						sh.debug("Message limit exceeded - creating a new one")
						output_messages.append("")
						current_output_message += 1
					
					if len(line) > MESSAGE_LENGTH_LIMIT:
						sh.debug("Line exceeds message limit - trimmed")
						line = line[:MESSAGE_LENGTH_LIMIT]
					
					output_messages[current_output_message] += line
			
			for message in output_messages:
				sh.debug("Sending message(s)...")
				await dest_channel.send(message)
			
			os.remove(filename) 
			sh.debug("File removed")
		else:
			#sh.debug("File not found")
			continue

t_outputter.channels = [0]
t_outputter.interval = 60