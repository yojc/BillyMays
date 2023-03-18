import random
import asyncio
from discord.utils import get

import billy_shared as sh

async def c_add_emoji(client, message):
	args = sh.get_args(message).split(" ")

	if len(args) != 2:
		await message.reply("Za mało argumentów")
		return

	target_msg_id = int(args[0])
	target_reaction = args[1]

	target_msg = get(client.cached_messages, id=target_msg_id)

	if not target_msg:
		await message.reply("Nie znaleziono wiadomości {}".format(target_msg_id))
		return
	
	if target_reaction.isnumeric():
		target_emoji = get(client.emojis, id=int(target_reaction))
	else:
		target_emoji = get(client.emojis, name=target_reaction)
	
	if not target_emoji:
		await message.reply("Nie znaleziono emoji {}".format(target_reaction))
		return
	
	await target_msg.add_reaction(target_emoji)
	await message.reply("Chyba OK?")


c_add_emoji.command = r"(reakcja|reaction)"
c_add_emoji.desc = "Dodaje reakcję do wiadomości (można użyć do dodawania animowanych!)"
