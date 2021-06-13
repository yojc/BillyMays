
import billy_shared as sh
from billy_typer import generate_cup, output_cup

async def c_typer(client, message):
	spam_channel_id = 386148571529084929

	new_cup = generate_cup(sh.get_args(message))

	if new_cup:
		await message.reply(new_cup)
		return
	else:
		new_cup = output_cup()
		
		if message.channel.id == spam_channel_id or str(message.channel.type) == "private":
			if (new_cup["group"]):
				await message.reply("MECZ FINAŁOWY:\n{}\n\nKomplet wyników:\n\n{}".format(new_cup["final"], new_cup["group"]))
			
			if (new_cup["knockout"]):
				await message.channel.send(new_cup["knockout"])
		else:
			if (new_cup["final"]):
				await message.reply("Przeprowadziłem symulację, i w finale padł następujący wynik:\n{}\nAby sprawdzić komplet wyników wejdź do <#{}>".format(new_cup["final"], spam_channel_id))
			
			if (new_cup["group"]):
				await client.get_channel(spam_channel_id).send("MECZ FINAŁOWY:\n{}\n\nKomplet wyników:\n\n{}".format(new_cup["final"], new_cup["group"]))
			
			if (new_cup["knockout"]):
				await client.get_channel(spam_channel_id).send(new_cup["knockout"])

c_typer.command = r"(typer)"
