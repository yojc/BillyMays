import discord
import random
import asyncio

import requests
import json
import time

import billy_shared as sh
from keys import TWITCH_KEY, TWITCH_SECRET
from config import REQUESTS_TIMEOUT, TWITCH_CHECK_FREQUENCY, TWITCH_ANNOUNCEMENT_COOLDOWN
from billy_twitch_data import twitch_streamers


politbiuro_main_channel = 174449535811190785
politbiuro_ograch = 639853618568232982
politbiuro_retro = 305100969191014404
politbiuro_japabocie = 386148571529084929

oauth_token = ""

# to find out the oauth-token
# curl -X POST "https://id.twitch.tv/oauth2/token?client_id=[twitch-id]&client_secret=[client-secret]&grant_type=client_credentials"

yojc_flag = False

def get_yojc_channel():
	global yojc_flag
	global politbiuro_ograch
	global politbiuro_retro

	if yojc_flag:
		yojc_flag = False
		sh.debug("Checking yojc flag, is set to o_grach")
		return politbiuro_ograch
	else:
		sh.debug("Checking yojc flag, is set to retro")
		return politbiuro_retro

def refresh_oauth_token():
	global TWITCH_KEY
	global TWITCH_SECRET
	global oauth_token

	sh.debug("Refreshing OAuth token...")

	s = requests.Session()
	url="https://id.twitch.tv/oauth2/token?client_id=" + TWITCH_KEY + "&client_secret=" + TWITCH_SECRET + "&grant_type=client_credentials"
	
	try:
		r = s.post(url, timeout=REQUESTS_TIMEOUT)
	except:
		sh.warn("### TWITCH OAUTH REQUEST FAILED!!!", date=True)
		return

	response = json.loads(r.text)

	if "access_token" in response:
		oauth_token = "Bearer " + response["access_token"]
		sh.warn("### TWITCH New OAuth token", date=True)
	else:
		sh.warn("### TWITCH Malformed OAuth token?", date=True)

	sh.warn(json.dumps(response))


async def t_twitch_announcements(client, channels):
	global TWITCH_KEY
	global twitch_streamers
	global oauth_token

	sh.debug("Checking Twitch stream status")

	if not oauth_token:
		refresh_oauth_token()

	headers = {"client-id": TWITCH_KEY, "authorization": oauth_token}
	s = requests.Session()
	url = "https://api.twitch.tv/helix/streams?"

	for playa in twitch_streamers:
		url += "user_id=" + playa + "&"

	url = url[:-1]

	#print(url)

	try:
		r = s.get(url, headers=headers, timeout=REQUESTS_TIMEOUT)
	except:
		sh.warn("### TWITCH REQUEST FAILED!!!", date=True)
		return
	
	sh.debug("Request sent, received code {}".format(r.status_code))
	try:
		response = json.loads(r.text)
	except:
		sh.warn("Twitch request failed! Status code: {}. Dumped request text to {}".format(r.status_code, sh.dump_errlog(r.text)))
		return

	if "status" in response and response["status"] != 200:
		if response["status"] == 401:
			sh.warn("### TWITCH Auth error (OAuth token expired?)", date=True)
			refresh_oauth_token()
			sh.warn(json.dumps(response))
		else:
			sh.warn("### TWITCH Unexpected error", date=True)
			sh.warn(json.dumps(response))
	elif "data" in response:
		for playa in response["data"]:
			if not playa["user_id"] in twitch_streamers:
				sh.debug("Streamer with ID {} not found in the database".format(playa["user_id"]))
				continue
			else:
				tmp = twitch_streamers[playa["user_id"]]
				
				if time.time()-tmp["last_seen"] < TWITCH_ANNOUNCEMENT_COOLDOWN*60:
					sh.debug("{} is streaming, but the notification is on cooldown".format(tmp["nickname"]))
					tmp["last_seen"] = time.time()
					continue
				else:
					sh.debug("{} is streaming - sending notification".format(tmp["nickname"]))
					tmp["last_seen"] = time.time()

					for ch in tmp["discord_channels"]:
						if ch == "yojc":
							dest_channel = get_yojc_channel()
						else:
							dest_channel = ch
						
						sh.debug("Destination channel: {}".format(dest_channel))
						
						await client.get_channel(dest_channel).send("{} właśnie streamuje na Twitchu! {}\n{}".format(tmp["nickname"], tmp["mention_group"], tmp["url"]))
	else:
		sh.warn("### TWITCH Malformed data received?", date=True)
		sh.warn(json.dumps(response))

t_twitch_announcements.channels = [333]
t_twitch_announcements.interval = TWITCH_CHECK_FREQUENCY*60

async def c_set_stream_dest(client, message):
	global yojc_flag

	if message.author.id != 307949259658100736:
		await message.reply("Spadaj pierdoło")

	old_flag = yojc_flag
	msg = sh.get_args(message)

	if msg == "ograch":
		yojc_flag = True
	elif msg == "retro":
		yojc_flag = False
	else:
		await message.reply("Nie rozpoznano flagi, jest {}".format(yojc_flag))
		return
	
	await message.reply("yojc_flag było {}, jest {}".format(old_flag, yojc_flag))

c_set_stream_dest.command = r"ustaw_stream"
c_set_stream_dest.desc = "hidden"