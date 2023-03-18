# ----------
# General
# ----------

BOT_PREFIX = r"^[;!\.,\/\\\\]"
BOT_OWNERS = [307949259658100736]

MESSAGE_LENGTH_LIMIT = 2000

# ----------
# Antiflood
# ----------

ANTIFLOOD_MSG_LIMIT = 5
ANTIFLOOD_TIME_LIMIT = 5

# Channels where billy will not react to any command.
ANTIFLOOD_CHANNELS_DENY_ALL = []

# Channels with billy_f_* function activated.
# pecetgej, politbiuro, luzna_jazda, japabocie, japa_bocie
ANTIFLOOD_CHANNELS_FULLTEXT = [318733700160290826, 174449535811190785, 316323075622961152, 319056762814595076, 386148571529084929]

# Channels that have antiflood control deactivated.
# japabocie, japa_bocie, sesje_rpg, sun_world, kanau_fela
ANTIFLOOD_CHANNELS_UNLIMITED = [316323075622961152, 319056762814595076, 386148571529084929, 174541542923436032, 539154754631106584, 232881423604776960]

# ----------
# Web requests
# ----------

REQUESTS_RETRY_COUNT = 3
REQUESTS_TIMEOUT = 12.05
REQUESTS_TRANSLATE_TIMEOUT = 24.05

REQUESTS_HEADERS = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	'Accept-Language': 'en-US,en;q=0.5',
	'Accept-Encoding': 'gzip, deflate',
	'DNT': '1',
	'Connection': 'keep-alive',
	'Upgrade-Insecure-Requests': '1'
}

# Will always dump Google request reply to file.
# Always on in developer mode, regardless of this setting
REQUESTS_DUMP_GOOGLE_TO_FILE = False

# Will always dump YouTube request reply to file.
# Always on in developer mode, regardless of this setting
REQUESTS_DUMP_YOUTUBE_TO_FILE = False

# ----------
# Reminders
# ----------

REMINDERS_DB_FILENAME = "billy_db_reminders.db"

# ----------
# Stats
# ----------

STATS_DB_FILENAME = "billy_db_stats.db"

STATS_RESULTS_COUNT = 10

# These channels will not be shown in stats results, unless forced.
STATS_CHANNELS_TO_OMIT = [326696245684862987, 425724173906870284, 471373220545691661, 697179498558259393, 730299221659484191]

# These users will not be shown in daily/weekly/monthly stats.
STATS_USERS_TO_OMIT = [122048388844748802]

# These channels will show more stat results.
STATS_CHANNELS_MORE_RESULTS = [319056762814595076, 386148571529084929]
STATS_CHANNELS_MORE_RESULTS_COUNT = 15

# ----------
# Roles
# ----------

ROLES_DB_FILENAME = "billy_db_roles.db"

# ----------
# Twitch
# ----------

# How many minutes between stream checks?
TWITCH_CHECK_FREQUENCY = 1

# No notification will be sent right after restarting the bot, for this amount of minutes.
# This should prevent another notification if the bot happens to restart when the channel is live.
TWITCH_BOT_START_TIMEOUT = 5

# The channel must be offline for at least this amount of minutes for the notification to be sent again.
TWITCH_ANNOUNCEMENT_COOLDOWN = 19.5

# ----------
# File outputter
# ----------

OUTPUTTER_FILENAMES = ["billy_output.txt", "/home/pi/steamgifts/output.txt"]

# ----------
# Misc debug stuff
# Enabling these will increase the amount of crap written to the console.
# ----------

# Prints all attributes that changed when on_member_update event occurs.
DEBUG_MEMBER_UPDATE = False

# Prints extra message info when on_message_delete event occurs.
DEBUG_MESSAGE_DELETION = False

# Lists all roles for all users on all available servers.
DEBUG_ROLES = False
