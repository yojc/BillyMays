import re

import billy_shared as sh
from billy_typer import generate_cup, output_cup, type_single_match

async def c_typer(client, message):
	spam_channel_id = 386148571529084929

	new_cup = generate_cup(sh.get_args(message))

	def split_msg(final, group):
		msg = "MECZ FINAŁOWY:\n{}\n\nKomplet wyników:\n\n{}".format(final, group)
		if len(msg) > 1999:
			delimiter = "Grupa"
			groups = msg.split(delimiter)
			return [delimiter.join(groups[:(len(groups)+1)//2]), delimiter + delimiter.join(groups[(len(groups)+1)//2:])]
		else:
			return [msg]

	if new_cup:
		await message.reply(new_cup)
		return
	else:
		new_cup = output_cup()
		
		if message.channel.id == spam_channel_id or str(message.channel.type) == "private":
			first_msg = True

			if (new_cup["group"]):
				for msg in split_msg(new_cup["final"], new_cup["group"]):
					if first_msg:
						await message.reply(msg)
						first_msg = False
					else:
						await message.channel.send(msg)

			
			if (new_cup["knockout"]):
				await message.channel.send(new_cup["knockout"])
		else:
			if (new_cup["final"]):
				await message.reply("Przeprowadziłem symulację, i w finale padł następujący wynik:\n{}\nAby sprawdzić komplet wyników wejdź do <#{}>".format(new_cup["final"], spam_channel_id))
			
			if (new_cup["group"]):
				for msg in split_msg(new_cup["final"], new_cup["group"]):
					await client.get_channel(spam_channel_id).send(msg)
			
			if (new_cup["knockout"]):
				await client.get_channel(spam_channel_id).send(new_cup["knockout"])

c_typer.command = r"(typer)"


async def c_typer_single(client, message):
	msg = sh.get_args(message)
	overtime = False

	if "-" in msg:
		delimiter = "-"
	elif "," in msg:
		delimiter = ","
	else:
		delimiter = " "
	
	if re.search(r"(overtime|dogrywka)", msg, re.IGNORECASE):
		msg = re.sub(r"(overtime|dogrywka)", "", msg, flags=re.IGNORECASE)
		overtime = True
	
	tmp = list(filter(None, map(str.strip, msg.split(delimiter, 1))))

	if len(tmp) > 1:
		ret = type_single_match(tmp[0], tmp[1], overtime)
	else: 
		ret = "Podaj drużyny bamboclu"
	
	await message.reply(ret)

c_typer_single.command = r"(typuj|mecz)"
