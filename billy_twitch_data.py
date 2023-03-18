import time
from config import TWITCH_BOT_START_TIMEOUT

politbiuro_main_channel = 174449535811190785
politbiuro_ograch = 639853618568232982
politbiuro_retro = 305100969191014404
politbiuro_japabocie = 386148571529084929
politbiuro_gryonline = 548207953455480832

twitch_start_time = time.time() - TWITCH_BOT_START_TIMEOUT*60

# to find out the user ID
# curl -H "client-id: [twitch-id]" -H "authorization: Bearer [token]" https://api.twitch.tv/helix/users?login=

twitch_streamers = {
	"44844181" : { 
		"nickname" : "yojc", 
		"url" : "https://www.twitch.tv/yojec", 
		"last_seen" : twitch_start_time,
		"discord_channels" : ["yojc"],
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
	},
	"47541578" : { 
		"nickname" : "accoun", 
		"url" : "https://www.twitch.tv/accoun_", 
		"last_seen" : twitch_start_time,
		"discord_channels" : [politbiuro_ograch],
		"mention_group" : "<@&872510146335629361>"
	},
	"40426372" : { 
		"nickname" : "Teb", 
		"url" : "https://www.twitch.tv/Tebeg", 
		"last_seen" : twitch_start_time,
		"discord_channels" : [politbiuro_gryonline],
		"mention_group" : "<@&1027822999681896539>"
	},
	"26544756" : { 
		"nickname" : "Shaker", 
		"url" : "https://www.twitch.tv/shakecaine", 
		"last_seen" : twitch_start_time,
		"discord_channels" : [politbiuro_ograch],
		"mention_group" : "<@&1086512961356578816>"
	}
}