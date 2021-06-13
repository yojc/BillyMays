import random
import asyncio
import discord

import billy_shared as sh


# -------------------------------------
# obrazki
# -------------------------------------


async def c_pozdro(client, message):
	await message.channel.send(file=discord.File(sh.file_path("img/pzdr.jpg")))

c_pozdro.command = r"(pozdro|pzdr)"
c_pozdro.desc = "pzdr i z fartem"


async def c_several(client, message):
	await message.channel.send(file=discord.File(sh.file_path("img/politbiuro_intensifies.gif")))

c_several.command = r"(several|spat)"
c_several.desc = "Several people are typing..."


async def c_wiplerine(client, message):
	await message.channel.send(file=discord.File(sh.file_path("img/xavier-mikke.jpg")))

c_wiplerine.command = r"(w|v)iplerine"


async def c_cogif(client, message):
	await message.channel.send(file=discord.File(sh.file_path("img/comment_jblSpYCkKHo8hIGeGqLq0xWLjNjfM19j.gif")))

c_cogif.command = r"(co|czo|what)"


async def c_wypierdalaj(client, message):
	await message.channel.send(file=discord.File(sh.file_path("img/comment_yJaXUY8ayZxkMA8s0oLMjNkdj6ajeDLD.gif")))

c_wypierdalaj.desc = "hidden"
#c_wypierdalaj.command = r"wypierdalaj"


async def c_wincyj(client, message):
	await message.channel.send(file=discord.File(sh.file_path("img/comment_302bIOuE74Qs2AzCr7pjcFmMfGRZvdgn.gif")))

c_wincyj.command = r"wincyj"


async def c_bkc(client, message):
	await message.channel.send(file=discord.File(sh.file_path("img/bk z kg chb z cb.jpg")))

c_bkc.command = r"bkc"


async def c_zgadzam(client, message):
	if random.random() < 0.1:
		await message.channel.send(file=discord.File(sh.file_path("img/dracia_intensifies.gif")))
	else:
		await message.channel.send(file=discord.File(sh.file_path("img/nargogh wins.png")))

c_zgadzam.command = r"zgadzam"
c_zgadzam.desc = "Się zgadzam z Nargogiem"


async def c_wish(client, message):
	await message.channel.send(file=discord.File(sh.file_path("img/THATSME.jpg")))

c_wish.command = r"wish"
c_wish.desc = "god I wish it was me"


async def c_babe(client, message):
	await message.channel.send(file=discord.File(sh.file_path("img/marian_czy_ty_mnie_kochasz.jpg")))

c_babe.command = r"(chlopprzebranyza)?bab(a|e)"

async def c_smaglor(client, message):
	await message.channel.send(file=discord.File(sh.file_path("img/lanbajlan.png")))

c_smaglor.command = r"(komarcz|smaglor)"

async def c_zzz(client, message):
	await message.channel.send(file=discord.File(sh.file_path("img/zzz.gif")))

c_zzz.command = r"zzz"

async def c_dojce(client, message):
	await message.channel.send(file=discord.File(sh.file_path("img/parampampam.jpg")))

c_dojce.command = r"dojce"

async def c_cisza(client, message):
	await message.channel.send(file=discord.File(sh.file_path("img/SILENCE OR I WILL KILL YOU.jpg")))

c_cisza.command = r"(cisza|silence)"


async def c_afera(client, message):
	await message.channel.send(file=discord.File(sh.file_path("img/comment_5DTDRHYuWYyVyTXzQGs7SvHZtyDz2sF8.gif"), filename="dewjusz_nakreca_kserbiego.gif"))

c_afera.command = r"afera"


async def c_vnag(client, message):
	if random.random() < 0.1:
		await message.channel.send(file=discord.File(sh.file_path("img/bruk-teb mountain.png")))
	else:
		await message.channel.send(file=discord.File(sh.file_path("img/teb.png")))

c_vnag.command = r"(nice|very(nice(and(gay)?)?)?|vnag)"


async def c_okazja(client, message):
	await message.channel.send(file=discord.File(sh.file_path("img/to_sie_nazywa_antycypowanie_norek.png")))

c_okazja.command = r"okazja"


async def c_dupie(client, message):
	await message.channel.send(file=discord.File(sh.file_path("img/ASS.png")))

c_dupie.command = r"(dupa|dupie)"


async def c_dupe(client, message):
	await message.channel.send(file=discord.File(sh.file_path("img/your face your ass whats the difference.png")))

c_dupe.command = r"(dupe)"


async def c_ociehuj(client, message):
	await message.channel.send(file=discord.File(sh.file_path("img/nasralem.jpg")))

c_ociehuj.command = r"ociec?huj"


async def c_zrozumiale(client, message):
	await message.channel.send(file=discord.File(sh.file_path("img/zrozumiale.webm")))

c_zrozumiale.command = r"(zrozumialem?|understandable|understood)"


async def c_provocative(client, message):
	await message.channel.send(file=discord.File(sh.file_path("img/provo.mp4")))

c_provocative.command = r"(provo(cative)?|prowo)"


async def c_nasralem(client, message):
	await message.channel.send(file=discord.File(sh.file_path("img/magiczny_napoj_metalusa.jpg")))

c_nasralem.command = r"(nasra(l|ł)em)"


async def c_uwal(client, message):
	await message.channel.send(file=discord.File(sh.file_path("img/hej kup se klej.jpg")))

c_uwal.command = r"(uwal|pizde|pizdę)"


async def c_silversurfer(client, message):
	await message.channel.send(file=discord.File(sh.file_path("img/zal.pl.png")))

c_silversurfer.command = r"(silversurfer|ss|rzal|zal)"


async def c_nawzajem(client, message):
	await message.channel.send(file=discord.File(sh.file_path("img/nawzajem.jpg")))

c_nawzajem.command = r"nawzajem"


async def c_stop(client, message):
	await message.channel.send(file=discord.File(sh.file_path("img/ELMO.mp4")))

c_stop.command = r"stop"


async def c_gofapota(client, message):
	await message.channel.send(file=discord.File(sh.file_path("img/gofa_pota.png")))

c_gofapota.command = r"(gofa|pota|gofapota|hari|haripota)"


async def c_pierdolisz(client, message):
	await message.channel.send(file=discord.File(sh.file_path("img/parmezany.jpg")))

c_pierdolisz.command = r"pierdolisz"


async def c_dzonka(client, message):
	await message.channel.send(file=discord.File(sh.file_path("img/still a better love story than meblosciankalight.JPG")))

c_dzonka.command = r"(dt|dzonka|tur)"


async def c_epic(client, message):
	await message.channel.send(file=discord.File(sh.file_path("img/oatw10sekund.webm")))

c_epic.command = r"(oat|epic)"


async def c_rabin(client, message):
	await message.channel.send(file=discord.File(sh.file_path("img/xysiu.webm")))

c_rabin.command = r"(rabin|rabbi)"


async def c_spierdalaj(client, message):
	await message.channel.send(file=discord.File(sh.file_path("img/wuppertal.png")))

c_spierdalaj.command = r"spierdalaj"


async def c_klasnij(client, message):
	await message.channel.send(file=discord.File(sh.file_path("img/rubik.png")))

c_klasnij.command = r"klasnij"


async def c_lyj(client, message):
	await message.channel.send(file=discord.File(sh.file_path("img/rudy_szubert.png")))

c_lyj.command = r"l(e|y)j"


async def c_mydli(client, message):
	await message.channel.send(file=discord.File(sh.file_path("img/mydli.jpg")))

c_mydli.command = r"mydli"


async def c_dobrze(client, message):
	await message.channel.send(file=discord.File(sh.file_path("img/dobrze.webm")))

c_dobrze.command = r"(dobrze|prawda|tak)"


async def c_zle(client, message):
	await message.channel.send(file=discord.File(sh.file_path("img/zle.webm")))

c_zle.command = r"(zle|falsz|nie)"


async def c_zapraszam_wypierdalac(client, message):
	await message.channel.send(file=discord.File(sh.file_path("img/wybamboclaj.jpg")))

c_zapraszam_wypierdalac.command = r"(zapraszam|wypierdalac)"


async def c_debbie(client, message):
	if random.random() < (1/15):
		await message.channel.send(file=discord.File(sh.file_path("img/senkyu.png")))
	else:
		await message.channel.send(file=discord.File(sh.file_path("img/debbie.jpg")))
	

c_debbie.command = r"(debiru|pierdole)"


async def c_uszanowanko(client, message):
	await message.channel.send(file=discord.File(sh.file_path("img/uszanowanko.png")))

c_uszanowanko.command = r"szanuje"


async def c_hammertime(client, message):
	await message.channel.send(file=discord.File(sh.file_path("img/hammerhead.webm")))

c_hammertime.command = r"hammer(time)?"


async def c_cicho(client, message):
	await message.channel.send(file=discord.File(sh.file_path("img/bulkowski.webm")))

c_cicho.command = r"cicho"


async def c_memeapproved(client, message):
	if random.random() < 0.05:
		if random.random() < 0.5:
			await message.channel.send(file=discord.File(sh.file_path("img/o8y7bAcVvBixP1Nb.webm"), filename="and_not_knuckles.webm"))
		else:
			await message.channel.send(file=discord.File(sh.file_path("img/Fgg4rkk5njffqzPA.webm"), filename="or_knuckles.webm"))
	else:
		await message.channel.send(file=discord.File(sh.file_path("img/_zL1eQZ5VldbBss2.webm"), filename="and_knuckles.webm"))

c_memeapproved.command = r"(approved|knuckles)"


async def c_gamer(client, message):
	await message.channel.send(file=discord.File(sh.file_path("img/So_Heres_Your_Problem.webm")))

c_gamer.command = r"gamer"


async def c_respects(client, message):
	await message.channel.send(file=discord.File(sh.file_path("img/showmethemoney.gif")))

c_respects.command = r"f"


async def c_good(client, message):
	await message.channel.send(file=discord.File(sh.file_path("img/johnny_b_goode.webm")))

c_good.command = r"good"
