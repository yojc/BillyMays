import asyncio
from datetime import date

import billy_shared as sh
from billy_birthdays import return_birthdays_periodic, check_upcoming_birthdays

async def c_birthdays_summary(client, message):
	ret_msg = None
	checked_server = None
	checked_days = 30

	def is_valid_day_value(value):
		return value.isnumeric() and int(value) < 366

	def is_server_id(value):
		return value.isnumeric() and len(value) == 18
	
	def check_server_type(value):
		if is_server_id(value):
			value = int(value)
		
		sh.debug("Given server: {} ({})".format(value, type(value)))
		return value

	args = sh.get_args(message).rsplit(" ", 1)
	
	# Parsing arguments

	if len(args) == 2:
		if not is_valid_day_value(args[1].strip()):
			sh.debug("Invalid days delta: {}".format(args[1].strip()))
			ret_msg = "Niepoprawna liczba dni do sprawdzenia"
		else:
			checked_days = int(args[1].strip())
			sh.debug("Got days value: {}".format(checked_days))

			checked_server = check_server_type(args[0].strip())
	
	if len(args) == 1:
		arg = args[0].strip()

		if not message.guild and len(arg) == 0:
			sh.debug("No arguments given, server name/ID expected")
			ret_msg = "Proszę podać serwer do sprawdzenia (nazwa lub ID)"
		elif len(arg) == 0:
			checked_server = message.guild.id
		else:
			if not message.guild:
				if is_valid_day_value(arg):
					sh.debug("Days delta given instead of server name")
					ret_msg = "Proszę podać serwer do sprawdzenia (nazwa lub ID)"
				else:
					checked_server = check_server_type(arg)
			else:
				if is_valid_day_value(arg):
					checked_days = int(arg)
					sh.debug("Got days value: {}".format(checked_days))
				else:
					checked_server = check_server_type(arg)
	
	if ret_msg:
		sh.debug("Error(s) occured while parsing arguments")
		await message.reply(ret_msg)
		return

	sh.debug("checked_server: {}; checked_days: {}, checked_date: {}".format(checked_server, checked_days, date.today().strftime("%Y-%m-%d")))
	upcoming_birthdays = check_upcoming_birthdays(checked_server, checked_days, date.today())

	if upcoming_birthdays is None:
		await message.reply("Nie znaleziono podanego serwera.")
	elif len(upcoming_birthdays) == 0:
		await message.reply("Brak nadchodzących urodzin w ciągu najbliższych {} dni.".format(checked_days))
	else:
		ret_msg = "Nadchodzące urodziny w ciągu najbliższych **{}** dni:\n\n".format(checked_days)

		for birthday in upcoming_birthdays:
			ret_msg += "`{}` {} (pozostało **{}** dni)\n".format(birthday["date"].strftime("%Y-%m-%d"), birthday["name"], birthday["delta"])
		
		await message.reply(ret_msg)

c_birthdays_summary.command = r"urodziny|birthdays"
c_birthdays_summary.params = ["[serwer]", "[ile_dni_wprzód]"]
c_birthdays_summary.desc = "sprawdza nadchodzące urodziny w danym przedziale czasowym (domyślnie 30 dni)"

async def t_birthdays(client, channels):
	sh.debug("Processing birthdays reminder")

	upcoming_birthdays = return_birthdays_periodic(date.today())

	for server in upcoming_birthdays:
		ret_msg = "Przypomnienie o nadchodzących urodzinach:\n\n"

		for birthday in server["users"]:
			ret_msg += "`{}` {} (pozostało **{}** dni)\n".format(birthday["date"].strftime("%Y-%m-%d"), birthday["name"], birthday["delta"])
	
		for user in server["target_users"]:
			try:
				sh.debug("Calling get_user...")
				dest_user = client.get_user(user)
			except Exception:
				sh.warn("User not found (get_user failed)! {}".format(user), date=True)
				continue

			if not dest_user:
				sh.warn("User not found (dest_user is None)! {}".format(user), date=True)
				continue
			
			dest_channel = dest_user.dm_channel

			if not dest_channel:
				sh.debug("dm_channel is None! Creating DM...")
				dest_channel = await dest_user.create_dm()

				if not dest_channel:
					sh.warn("create_dm falied! This output was aborted")
			
			await dest_channel.send(ret_msg)
		
		#for channel in server["target_channels"]:

t_birthdays.channels = [0]
t_birthdays.time = "8:00"