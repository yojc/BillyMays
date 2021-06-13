import billy_shared as sh
from config import ROLES_DB_FILENAME, ROLES_DEBUG

roles_db = {}

def roles_debug(msg):
	if ROLES_DEBUG:
		sh.debug(msg)

def init_roles(client):
	for server in client.guilds:
		roles_debug("Checking roles for server {} (ID: {})".format(server.name, server.id))

		for member in server.members:
			roles_debug("Checking roles for member {} (ID: {})".format(member.name, member.id))

			if len(member.roles) == 0 or (len(member.roles) == 1 and member.roles[0].name == "@everyone"):
				roles_debug("No roles found")
				continue

			for role in member.roles:
				if role.name == "@everyone":
					continue
				roles_debug("{} ({})".format(role.name, role.id))