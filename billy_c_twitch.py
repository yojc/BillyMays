import discord
import random
import asyncio

import requests
import json
import time

import billy_shared as sh
from keys import TWITCH_KEY, TWITCH_SECRET


politbiuro_main_channel = 174449535811190785
politbiuro_ograch = 639853618568232982
politbiuro_retro = 305100969191014404
politbiuro_japabocie = 386148571529084929

twitch_check_frequency = 1 # minutes
twitch_bot_start_timeout = 5 # minutes
twitch_announcement_cooldown = 19.5 # minutes
twitch_start_time = time.time() - twitch_bot_start_timeout*60
oauth_token = ""

# to find out the oauth-token
# curl -X POST "https://id.twitch.tv/oauth2/token?client_id=[twitch-id]&client_secret=[client-secret]&grant_type=client_credentials"

# to find out the user ID
# curl -H "client-id: n39cbw7gz4kzblf6k4u1p2lxx87jib" -H "authorization: Bearer k8z2zdqm4v2952hs5o04t717tzp4mx" https://api.twitch.tv/helix/users?login=

twitch_streamers = {
	"44844181" : { 
		"nickname" : "yojc", 
		"url" : "https://www.twitch.tv/yojec", 
		"last_seen" : twitch_start_time,
		"discord_channels" : [politbiuro_retro],
		"mention_group" : "<@&672691296091111424>"
	},

	"237017365" : { 
		"nickname" : "Komstuch", 
		"url" : "https://www.twitch.tv/komstuch", 
		"last_seen" : twitch_start_time,
		"discord_channels" : [politbiuro_ograch],
		"mention_group" : "<@&674317267198279682>"
	},

	"191881998" : { 
		"nickname" : "Artius", 
		"url" : "https://www.twitch.tv/izdebeth", 
		"last_seen" : twitch_start_time,
		"discord_channels" : [politbiuro_ograch],
		"mention_group" : "<@&674317361066803210>"
	},

	"51708433" : { 
		"nickname" : "Abyss", 
		"url" : "https://www.twitch.tv/abyss121", 
		"last_seen" : twitch_start_time,
		"discord_channels" : [politbiuro_ograch],
		"mention_group" : "<@&674317320520466433>"
	},

	"48895107" : { 
		"nickname" : "kiceg", 
		"url" : "https://www.twitch.tv/kicegg", 
		"last_seen" : twitch_start_time,
		"discord_channels" : [politbiuro_ograch],
		"mention_group" : "<@&693760408615518209>"
	},

	"449776925" : { 
		"nickname" : "nevka", 
		"url" : "https://www.twitch.tv/nevka_", 
		"last_seen" : twitch_start_time,
		"discord_channels" : [politbiuro_ograch],
		"mention_group" : "<@&718134655945015346>"
	}

	#"40426372" : { 
	#	"nickname" : "Teb", 
	#	"url" : "https://www.twitch.tv/Tebeg", 
	#	"last_seen" : time.time(),
	#	"discord_channels" : [politbiuro_japabocie]
	#}
}

def refresh_oauth_token():
	global TWITCH_KEY
	global TWITCH_SECRET
	global oauth_token

	s = requests.Session()
	url="https://id.twitch.tv/oauth2/token?client_id=" + TWITCH_KEY + "&client_secret=" + TWITCH_SECRET + "&grant_type=client_credentials"
	
	try:
		r = s.post(url, timeout=12.05)
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

	#sh.warn("### TWITCH TEST ### ", date=True)

	if not oauth_token:
		refresh_oauth_token()

	#print(oauth_token)
	headers = {"client-id": TWITCH_KEY, "authorization": oauth_token}
	s = requests.Session()
	url = "https://api.twitch.tv/helix/streams?"

	for playa in twitch_streamers:
		url += "user_id=" + playa + "&"

	url = url[:-1]

	#print(url)

	try:
		r = s.get(url, headers=headers, timeout=12.05)
	except:
		sh.warn("### TWITCH REQUEST FAILED!!!", date=True)
		return
	
	#print("Poszło zapytanie - otrzymano " + str(r.status_code))
	response = json.loads(r.text)

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
				#print("Nie znaleziono gracza w db")
				continue
			else:
				tmp = twitch_streamers[playa["user_id"]]
				
				if time.time()-tmp["last_seen"] < twitch_announcement_cooldown*60:
				#print(tmp["nickname"] + " - nie powiadamiam")
					tmp["last_seen"] = time.time()
					continue
				else:
					#print(tmp["nickname"] + " - alleluja!")
					tmp["last_seen"] = time.time()

					for ch in tmp["discord_channels"]:
						await client.get_channel(ch).send("{} właśnie streamuje na Twitchu! {}\n{}".format(tmp["nickname"], tmp["mention_group"], tmp["url"]))
	else:
		sh.warn("### TWITCH Malformed data received?", date=True)
		sh.warn(json.dumps(response))

t_twitch_announcements.channels = [333]
t_twitch_announcements.interval = twitch_check_frequency*60