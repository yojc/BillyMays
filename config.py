# ----------
# General
# ----------

BOT_PREFIX = r"^[;!\.,\/\\\\]"
BOT_OWNERS = [307949259658100736]

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

# Lots of crap gets written to the console, don't enable unless you need it.
# Work only in debug/dev mode.
ROLES_DEBUG = False