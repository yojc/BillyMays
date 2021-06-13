import random
import asyncio
import itertools
import re
import unidecode
import time

import json
import os

import billy_shared as sh
from billy_antiflood import check_uptime
from billy_nicknames import get_random_nickname

boruc = "Artur Boruc"

async def c_nickrand(client, message):
	phrase = sh.replace_all(sh.get_args(message), {u'Ą':'A', u'Ę':'E', u'Ó':'O', u'Ś':'S', u'Ł':'L', u'Ż':'Z', u'Ź':'Z', u'Ć':'C', u'Ń':'N', u'ą':'a', u'ę':'e', u'ó':'o', u'ś':'s', u'ł':'l', u'ż':'z', u'ź':'z', u'ć':'c', u'ń':'n'})
	uniq = ''.join(ch for ch, _ in itertools.groupby(''.join(sorted(re.sub("[^a-z]", "", phrase.lower())))))
	uniqV = ''
	uniqC = ''
	uniqN = '0123456789'

	for letter in uniq:
		if letter in "eyuioa":
			uniqV += letter
		else:
			uniqC += letter

	uniqVS = ''.join(random.sample(uniqV,len(uniqV)))
	uniqCS = ''.join(random.sample(uniqC,len(uniqC)))
	uniqNS = ''.join(random.sample(uniqN,len(uniqN)))

	mask = ''
	for letter in phrase:
		if letter.islower():
			mask += 'a'
		elif letter.isupper():
			mask += 'A'
		else:
			mask += '#'

	ret = ''
	for letter in phrase.lower():
		if uniqV.find(letter) > -1:
			ret += uniqVS[uniqV.find(letter)]
		elif uniqC.find(letter) > -1:
			ret += uniqCS[uniqC.find(letter)]
		elif uniqN.find(letter) > -1:
			ret += uniqNS[uniqN.find(letter)]
		else:
			ret += letter

	ret = list(ret)
	for i in range(0, len(ret)):
		if mask[i].islower():
			ret[i] = ret[i].lower()
		elif mask[i].isupper():
			ret[i] = ret[i].upper()

	await message.channel.send(''.join(ret))

c_nickrand.command = r"rn"
c_nickrand.params = ["zdanie"]
c_nickrand.desc = "Miesza litery w zdaniu"

async def c_slap(client, message):
	verb = random.choice(['slaps', 'hits', 'smashes', 'beats', 'bashes', 'smacks', 'blasts', 'punches', 'stabs', 'kills', 'decapitates', 'crushes', 'devastates', 'massacres', 'assaults', 'tackles', 'abuses', 'slams', 'slaughters', 'obliderates', 'wipes out', 'pulverizes', 'granulates', 'stuns', 'knocks out', 'strikes', 'bitchslaps', 'scratches', 'pounds', 'bangs', 'whacks', 'rapes', 'eats', 'destroys', 'does nothing to', 'dooms', 'evaporates', 'does something to', 'taunts', 'disrespects', 'disarms', 'mauls', 'dismembers', 'defuses', 'butchers', 'annihilates', 'tortures', 'shatters', 'wrecks', 'toasts', 'dominates', 'suffocates', 'oxidises', 'erases', 'stomps', 'zaps', 'whomps', 'swipes', 'pats', 'nails', 'thumps', '*PAC*'])
	area = random.choice(['around the head', 'viciously', 'repeatedly', 'in the face', 'to death', 'in the balls', 'in the ass', 'savagely', 'brutally', 'infinitely', 'deeply', 'mercilessly', 'randomly', 'homosexually', 'keenly', 'accurately', 'ironically', 'gayly', 'outrageously', 'straight through the heart', 'immediately', 'unavoidably', 'from the inside', 'around a bit', 'from outer space', 'gently', 'silently', 'for real', 'for no apparent reason', 'specifically', 'maybe', 'allegedly', 'once and for all', 'for life', 'stealthly', 'energetically', 'frightfully', 'in the groin', 'in the dignity', 'in the heels', 'in the nostrils', 'in the ears', 'in the eyes', 'in the snout', 'fearfully', 'appallingly', 'vigorously', 'hrabully'])
	size = random.choice(['large', 'huge', 'small', 'tiny', 'enormous', 'massive', 'rusty', 'gay', 'pink', 'sharpened', 'lethal', 'poisoned', 'toxic', 'incredible', 'powerful', 'wonderful', 'priceless', 'explosive', 'rotten', 'smelly', 'puny', 'toy', 'deadly', 'mortal', 'second-rate', 'second-hand', 'otherwise useless', 'magical', 'pneumatic', 'manly', 'sissy', 'iron', 'steel', 'golden', 'filthy', 'semi-automatic', 'invisible', 'infected', 'spongy', 'sharp-pointed', 'undead', 'horrible', 'intimidating', 'murderous', 'intergalactic', 'serious', 'nuclear', 'cosmic', 'mad', 'insane', 'rocket-propelled', 'holy', 'super', 'homosexual', 'imaginary', 'airborne', 'atomic', 'huge', 'lazy', 'stupid', 'communist', 'creepy', 'slimy', 'nazi', 'heavyweight', 'lightweight', 'thin', 'thick'])
	tool = random.choice(['trout', 'fork', 'mouse', 'bear', 'piano', 'cello', 'vacuum', 'mosquito', 'sewing needle', 'nail', 'fingernail', 'opti', 'penis', 'whale', 'cookie', 'straight-arm punch', 'roundhouse kick', 'training shoe', 'dynamite stick', 'Justin Bieber CD', 'fart cloud', 'dildo', 'lightsaber', 'rock', 'stick', 'nigger', 'dinosaur', 'soap', 'foreskin', 'sock', 'underwear', 'herring', 'spider', 'snake', 'ming vase', 'cow', 'jackhammer', 'hammer and sickle', 'razorblade', 'daemon', 'trident', 'gofer', 'alligator', 'bag of piss', 'lobster', 'beer pad', 'toaster', 'printer', 'nailgun', 'banana bomb', 'fetus', 'unicorn statue', 'blood vial', 'electron', 'spell', 'tin of spam', 'behemoth', 'hand grenade', 'hand of God', 'fist of fury', 'erection', 'Pudzian\'s egg kick', 'pimp hand', 'darth fallus', 'dog turd', 'canoe', 'Atari 5200', 'booby trap', 'Gaben', 'fishbot', 'syntax error', 'blue screen of death'])
	
	if sh.get_args(message) == "":
		who = message.author.display_name
	else:
		who = sh.get_args(message)
	
	if who.lower() in ["billy mays", "himself", "self", "billy", "<@312862727385251842>"]:
		who = message.author.display_name
	
	if size[0].lower() in ["a", "e", "i", "o", "u"]:
		witha = "with an";
	else:
		witha = "with a";
	
	action = "*Billy Mays %s %s %s %s %s %s!*" % (verb, who, area, witha, size, tool)
	await message.channel.send(action)

c_slap.command = r"slap"
c_slap.params = ["nick"]


async def c_pazdzioch(client, message):
	if sh.get_args(message) == "":
		who = message.author.display_name
	else:
		who = sh.get_args(message)
	
	if who.lower() in ["billy mays", "himself", "self", "billy", "<@312862727385251842>"]:
		who = message.author.display_name
	
	what = random.choice(["alkoholik", "analfabeta", "arbuz", "baran", "bambocel", "bezczelny człowiek", "burak", "bydlak nie człowiek", "cham bezczelny", "cham ze wsi spod Elbląga", "chuderlak", "ciemniak", "cymbał", "człowiek kiełbasa", "człowiek niedorozwinięty", "darmozjad", "defekt", "donosiciel", "dupa z uszami", "dureń jeden", "dziad", "dziad kalwaryjski", "dzieciorób", "dzikus", "Einstein zasrany", "erosoman", "frajer", "gagatek", "Gigi Amoroso zasrany", "gnida", "gnój", "głupi psychopata", "głowonóg", "grubas przebrzydły bez czci i wiary", "grubas erosomański", "grubasz pieprzony", "grubas pogański", "grubas pornograficzny", "horror erotyczny", "idiota", "ignorant", "judasz zasrany", "ludożerca", "łobuz", "kanibal", "kapucyn jeden", "kretyn", "krwiożerczy grubas", "menda", "menel", "nędzna karykatura", "nienormalny", "niedorozwój", "nikt", "niewyselekcjonowany burak", "odpad atomowy", "oszust", "pajac", "pasożyt", "parobas", "parówa", "pederasta", "pierdzimąka", "pijak", "pierdoła", "pokraka", "przygłup", "plackarz charytatywny, zasrany", "regularne bydle", "regularny debil i złodziej", "sadysta", "snowboardzista zasrany", "sprośna świnia", "szmaciarz", "świniak", "świnia przebrzydła", "świnia pornograficzna", "świnia zakamuflowana", "świnia żarłoczna", "świnia erosomańska", "śmieć", "taran opasły", "tuman", "ukryty erosoman", "wsza ludzka", "wieprz", "wypierdek", "zagrożenie dla kościoła", "zboczek pieprzony", "zbrodniarz", "zdrajca", "zdewociały faszysta", "znachor zasrany", "żarłoczny, pasożytniczy wrzód na dupie społeczeństwa ludu pracującego miast i wsi"])

	await message.channel.send("%s to %s!" % (who, what))

c_pazdzioch.command = r"(pazdzioch|boczek)"


async def c_balls(client, message):
	await message.channel.send("I've got balls of steel")

c_balls.command = r"balls"
c_balls.desc = "I've got balls of steel"

async def c_boruc(client, message):
	await message.channel.send("brawo " + boruc)

c_boruc.command = r"(brawo|boruc)"
c_boruc.desc = "BRAWO ARTUR BORUC"

async def c_setboruc(client, message):
	global boruc
	
	if sh.get_args(message) == "":
		boruc = "Artur Boruc"
	else:
		boruc = sh.get_args(message)

c_setboruc.command = r"set"
c_setboruc.desc = "hidden"

async def c_ohgod(client, message):
	await message.channel.send("oh god oh man")

c_ohgod.command = r"ohgod"
c_ohgod.desc = "Oh god oh man"

async def c_patch(client, message):
	await message.channel.send("exec Patch.txt")

c_patch.command = r"patch"
c_patch.desc = "hidden"

async def c_rimshot(client, message):
	await message.channel.send("Ba-dum-pish!")

c_rimshot.command = r"rimshot"
c_rimshot.desc = "Ba-dum-pish!"


async def c_cwiercz(client, message):
	if random.random() < 0.8:
		await message.channel.send("https://www.youtube.com/watch?v=K8E_zMLCRNg")
	else:
		await message.channel.send(random.choice(["https://www.youtube.com/watch?v=IP5e7jrYBtY", "https://www.youtube.com/watch?v=gmS5yyBrWZU"]))

c_cwiercz.command = r"(cricket(s)?|swierszcz(e)?)"
c_cwiercz.desc = "Używać razem z funkcją .martius"


async def c_nh(client, message):
	if random.random() < 0.15:
		await message.channel.send(random.choice(["(much homo wow)", "(extra homo)", "(kiceg tier homo)", "(no hetero)", "(yes homo)", "(ecce homo)"]))
	else:
		await message.channel.send("(no homo)")

c_nh.command = r"(nh|nohomo)"


async def c_mmmm(client, message):
	ret = ""
	for x in range(0, random.randint(4, 13)):
		ret += 'm'
	for x in range(0, random.randint(1, 4)):
		ret += 'M'
	for x in range(0, random.randint(2, 5)):
		ret += 'H'
	for x in range(0, random.randint(1, 4)):
		ret += 'M'
	for x in range(0, random.randint(4, 13)):
		ret += 'm'
	await message.channel.send(ret)

c_mmmm.command = r"m[mh]{2,}"

async def c_twss(client, message):
	await message.channel.send("That's what she said!")

c_twss.command = r"twss"
c_twss.desc = "That's what she said!"


async def c_wybierz(client, message):
	msg = sh.get_args(message)
	if "," in msg:
		delimiter = ","
	else:
		delimiter = " "
	
	tmp = list(filter(None, map(str.strip, msg.split(delimiter))))
	
	if len(tmp) > 0:
		ret = random.choice(tmp)
	else: 
		ret = "Nie mam nic do wyboru tłumoku"
	
	await message.reply(ret)

c_wybierz.command = r"wybierz"
c_wybierz.params = ["opcja, opcja, opcja..."]


async def c_ym(client, message):
	await message.channel.send("Your mom")

c_ym.command = r"ym"
c_ym.desc = "Your mom"


async def c_esad(client, message):
	await message.channel.send("Eat shit and die")

c_esad.command = r"esad"
c_esad.desc = "Eat shit and die"


async def c_kurwa(client, message):
	c = sh.get_command(message).lower()
	await message.reply(sh.insert_word(c, sh.get_args(message)))

c_kurwa.command = r"(kurwa|fucking)"
c_kurwa.params = ["zdanie"]
c_kurwa.desc = "Okrasz wypowiedź wyrafinowanym słownictwem!"


async def c_wstaw(client, message):
	tmp = sh.get_args(message).split(" ", 1)
	ret = sh.insert_word(tmp[0], tmp[1])
	
	await message.reply(ret)

c_wstaw.command = r"(wstaw|insert)"
c_wstaw.params = ["słowo", "zdanie"]
c_wstaw.desc = "Wstaw słowo w dowolne miejsca zdania"


async def c_uptime(client, message):
	await message.channel.send(check_uptime())

c_uptime.command = r"uptime"
c_uptime.desc = "hidden"


async def c_pair(client, message):
	if message.guild:
		nicks = []
		forbidden = ["Fursik"]
		
		for n in message.guild.members:
			if n.display_name not in forbidden:
				nicks.append(n.display_name)
		
		first = random.choice(nicks)
		second = random.choice(nicks)
		
		if len(nicks) > 1:
			while first == second:
				second = random.choice(nicks)
		
		await message.channel.send(first + " × " + second)

c_pair.command = r"(pair|ship)"


async def c_losu(client, message):
	if message.guild:
		nicks = []
		nick = ""

		channel_nev = 697179498558259393
		forbidden_all = [205985469081714698]
		forbidden_per_channel = {
			channel_nev : [295551521884733440, 316150521989824513, 108688393860308992, 316261530859470849, 307949259658100736, 401821271371022355]
		}
		
		for n in message.guild.members:
			# and n.id is not message.author.id
			if n.bot is not True and n.id not in forbidden_all and message.channel.permissions_for(n).read_messages and (message.channel.id not in forbidden_per_channel or n.id not in forbidden_per_channel[message.channel.id]):
				if n.nick:
					nicks.append([n.id, n.display_name + " (" + n.name + ")"])
				else:
					nicks.append([n.id, n.name])
		
		if message.channel.id in forbidden_per_channel:
			db_path = sh.file_path("billy_db_losu.db")
			data = None

			if os.path.exists(db_path):
				with open(db_path, "r") as db:
					try:
						data = json.load(db)
					except:
						data = {}
			else:
				data = {}

			with open(db_path, "w") as db:
				channel = str(message.channel.id)
				key = sh.get_args(message) or "all" #message.author.id
				
				if channel not in data:
					data[channel] = {}
				
				if key not in data[channel]:
					data[channel][key] = []
				
				nicks_working_copy = [x for x in nicks if not (x[0] in data[str(channel_nev)][key])]

				if len(nicks_working_copy) == 0:
					data[channel][key] = []
					nick = "Wylosowano już wszystkie osoby. Resetuję listę."
				else:
					person = random.choice(nicks_working_copy)
					data[channel][key].append(person[0])
					nick = person[1]

				json.dump(data, db)
		else: 
			nick = random.choice(nicks)[1]
		
		await message.reply(nick)

c_losu.command = r"losu"


async def c_klocuch(client, message):
	vids = ["https://www.youtube.com/watch?v=YidQZnQSB4I", "https://www.youtube.com/watch?v=Auot04TYZp4", "https://www.youtube.com/watch?v=YJakurmhT-E", "https://www.youtube.com/watch?v=v20aYFWu8f4", "https://www.youtube.com/watch?v=ABhdqD7hGtw", "https://www.youtube.com/watch?v=xhpamcFwRBs", "https://www.youtube.com/watch?v=5itoVUzXHIg", "https://www.youtube.com/watch?v=xLaHAjENWb0", "https://www.youtube.com/watch?v=V77ktdbGmbI", "https://www.youtube.com/watch?v=Q8N_dgvm_28", "https://www.youtube.com/watch?v=CQvBAPMOw1E", "https://www.youtube.com/watch?v=medTXwgrx4U", "https://www.youtube.com/watch?v=BYPR9ebbLFY", "https://www.youtube.com/watch?v=YZI-_MVGRM4", "https://www.youtube.com/watch?v=xq-mD3TCkfc", "https://www.youtube.com/watch?v=E7gCQ6FA3BQ", "https://www.youtube.com/watch?v=09F-waIZG2E", "https://www.youtube.com/watch?v=w1iVTOdllUo", "https://www.youtube.com/watch?v=jn54hyJH1W8", "https://www.youtube.com/watch?v=hN7NZCG63Sk", "https://www.youtube.com/watch?v=gMEWuMmOf-A", "https://www.youtube.com/watch?v=8WFjoBCnzGY", "https://www.youtube.com/watch?v=zii15LcTSLw", "https://www.youtube.com/watch?v=kykPWhAdJZA", "https://www.youtube.com/watch?v=8NV9zyhaQaY", "https://www.youtube.com/watch?v=UrG5mioVZe0", "https://www.youtube.com/watch?v=cJRrqAPyywk", "https://www.youtube.com/watch?v=sccYn-rfq4Q", "https://www.youtube.com/watch?v=EzMkI_FBje0", "https://www.youtube.com/watch?v=YHm60KS0EMc", "https://www.youtube.com/watch?v=s9izhCLWPZs", "https://www.youtube.com/watch?v=qis339gCCSg", "https://www.youtube.com/watch?v=4-wWAtSGSaE", "https://www.youtube.com/watch?v=Ldp0X3SpbnE", "https://www.youtube.com/watch?v=Io3f5bKFlFs", "https://www.youtube.com/watch?v=Ofm-ZU-WbLM", "https://www.youtube.com/watch?v=665_HyoNxU8", "https://www.youtube.com/watch?v=cbm_CikNeEk", "https://www.youtube.com/watch?v=dID0aHDKATU", "https://www.youtube.com/watch?v=Si-L0arYVoE", "https://www.youtube.com/watch?v=xxwJuE215SM", "https://www.youtube.com/watch?v=NG_W3L_iy9w", "https://www.youtube.com/watch?v=AUtNIXO8pcU", "https://www.youtube.com/watch?v=8DDx5r6lwpM", "https://www.youtube.com/watch?v=9QXu7MRCs30", "https://www.youtube.com/watch?v=KUva_V-NWs8", "https://www.youtube.com/watch?v=5Ff1__OBYXc", "https://www.youtube.com/watch?v=TSQnM33CGII", "https://www.youtube.com/watch?v=2k-y5N_vFZA", "https://www.youtube.com/watch?v=NFdhFJ0RzHA", "https://www.youtube.com/watch?v=s0S-Jamzi_c", "https://www.youtube.com/watch?v=fDtCStfL1Y8", "https://www.youtube.com/watch?v=hqt3u3c5QiI", "https://www.youtube.com/watch?v=q1a5TUDISdM", "https://www.youtube.com/watch?v=uZx83buJNA8", "https://www.youtube.com/watch?v=sZg6XSaMAwM", "https://www.youtube.com/watch?v=VurnIaithdo", "https://www.youtube.com/watch?v=acMskgoCacY", "https://www.youtube.com/watch?v=zzRjCjo2SFQ", "https://www.youtube.com/watch?v=LW8YS8jnZxA", "https://www.youtube.com/watch?v=AiPLWSXgGgU", "https://www.youtube.com/watch?v=ZIYnRWfM9sk", "https://www.youtube.com/watch?v=WFgnlaLMbcc", "https://www.youtube.com/watch?v=lfQr68XXCXo", "https://www.youtube.com/watch?v=nwXiFgawbdA", "https://www.youtube.com/watch?v=azvm8A_BIkE", "https://www.youtube.com/watch?v=A_AuB8dXmP4", "https://www.youtube.com/watch?v=XFgMBBwi8lI", "https://www.youtube.com/watch?v=GBSfqEV1cxo", "https://www.youtube.com/watch?v=OoB_clQZJyk", "https://www.youtube.com/watch?v=g0K64KeYyl4", "https://www.youtube.com/watch?v=4UDC3ZpNjlI", "https://www.youtube.com/watch?v=heAtTMF7lzU", "https://www.youtube.com/watch?v=1dsSM1C0f-o", "https://www.youtube.com/watch?v=Ucam4s2rxC4", "https://www.youtube.com/watch?v=HHraFdmGOKQ", "https://www.youtube.com/watch?v=SzBWXg9ns44", "https://www.youtube.com/watch?v=9gzq988ANfg", "https://www.youtube.com/watch?v=_J7zDdQyzPw", "https://www.youtube.com/watch?v=gdLsTCQ3d0s", "https://www.youtube.com/watch?v=sRcHVGTphWY", "https://www.youtube.com/watch?v=UzFj_PrBDDs", "https://www.youtube.com/watch?v=ZL-3-t8hedg", "https://www.youtube.com/watch?v=W_Ro0zlD7x8", "https://www.youtube.com/watch?v=5RGa4lBgEk0", "https://www.youtube.com/watch?v=EChdbKFy5qk", "https://www.youtube.com/watch?v=QdasWOuiB_E", "https://www.youtube.com/watch?v=D_Lyp0jMJS8", "https://www.youtube.com/watch?v=AVHepIx3HXQ"]
	
	await message.channel.send(random.choice(vids))

c_klocuch.command = r"klocuch(12)?"


async def c_skryba(client, message):
	await message.channel.send("Moim zdaniem to nie ma tak, że dobrze albo że nie dobrze. Gdybym miał powiedzieć, co cenię w życiu najbardziej, powiedziałbym, że ludzi. Ekhm... Ludzi, którzy podali mi pomocną dłoń, kiedy sobie nie radziłem, kiedy byłem sam. I co ciekawe, to właśnie przypadkowe spotkania wpływają na nasze życie. Chodzi o to, że kiedy wyznaje się pewne wartości, nawet pozornie uniwersalne, bywa, że nie znajduje się zrozumienia, które by tak rzec, które pomaga się nam rozwijać. Ja miałem szczęście, by tak rzec, ponieważ je znalazłem. I dziękuję życiu. Dziękuję mu, życie to śpiew, życie to taniec, życie to miłość. Wielu ludzi pyta mnie o to samo, ale jak ty to robisz?, skąd czerpiesz tę radość? A ja odpowiadam, że to proste, to umiłowanie życia, to właśnie ono sprawia, że dzisiaj na przykład buduję maszyny, a jutro... kto wie, dlaczego by nie, oddam się pracy społecznej i będę ot, choćby sadzić... znaczy... marchew.")

c_skryba.command = r"skryba"


async def c_korwin(client, message):
	title = "pani" if sh.is_female(message) else "pan"
	components = [
		["Proszę zwrócić uwagę, że", "I tak mam trzy razy mniej czasu, więc proszę pozwolić mi powiedzieć:", "Państwo się śmieją, ale", "Ja nie potrzebowałem edukacji seksualnej, żeby wiedzieć, że", "No niestety:", "Gdzie leży przyczyna problemu? Ja państwu powiem:", "Państwo chyba nie wiedzą, że", "Oświadczam kategorycznie:", "Powtarzam:", "Powiedzmy to z całą mocą:", "W polsce dzisiaj", "Państwo sobie nie zdają sprawy, że", "To ja przepraszam bardzo:", "Otóż nie wiem, czy " + title + " wie, że", "Yyyyy...", "Ja chcę powiedzieć jedną rzecz:", "Trzeba powiedzieć jasno:", "Jak powiedział wybitny krakowianin Stanisław Lem,", "Proszę mnie dobrze zrozumieć:", "Ja chciałem państwu przypomnieć, że", "Niech państwo nie mają złudzeń:", "Powiedzmy to wyraźnie:"],
		["właściciele niewolników", "związkowcy", "trockiści", "tak zwane dzieci kwiaty", "rozmaici urzędnicy", "federaści", "etatyści", "ci durnie i złodzieje", "ludzie wybrani głosami meneli spod budki z piwem", "socjaliści pobożni", "socjaliści bezbożni", "komuniści z krzyżem w zębach", "agenci obcych służb", "członkowie Bandy Czworga", "pseudo-masoni z Wielkiego Wschodu Francji", "przedstawiciele czerwonej hołoty", "ci wszyscy (tfu!) geje", "funkcjonariusze reżymowej telewizji", "tak zwani ekolodzy", "ci wszyscy (tfu!) demokraci", "agenci bezpieki", "feminazistki"],
		["po przeczytaniu *Manifestu komunistycznego*", "którymi się brzydzę", "których nienawidzę", "z okolic \"Gazety Wyborczej\"", "- czyli taka żydokomuna -", "odkąd zniesiono karę śmierci", "którymi pogardzam", "których miejsce w normalnym kraju jest w więzieniu", "na polecenie Brukseli", "posłusznie", "bezmyślnie", "z nieprawdopodobną pogardą dla człowieka", "za pieniądze podatników", "zgodnie z ideologią LGBTQZ", "za wszelką cenę", "zupełnie bezkarnie", "całkowicie bezczelnie", "o poglądach na lewo od komunizmu", "celowo i świadomie", "z premedytacją", "od czasów Okrągłego Stołu", "w ramach postępu"],
		["udają homoseksualistów", "niszczą rodzinę", "idą do polityki", "zakazują góralom robienia oscypków", "organizują paraolimpiady", "wprowadzają ustrój, w którym raz na cztery lata można wybrać sobie pana", "ustawiają fotoradary", "wprowadzają dotacje", "wydzielają buspasy", "podnoszą wiek emerytalny", "rżną głupa", "odbierają dzieci rodzicom", "wprowadzają absurdalne przepisy", "umieszczają dzieci w szkołach koedukacyjnych", "wprowadzają parytety", "nawołują do podniesienia podatków", "próbują skłócić Polskę z Rosją", "głoszą brednie o globalnym ociepleniu", "zakazują posiadania broni", "nie dopuszczają prawicy do władzy", "uczą dzieci homoseksualizmu"],
		["żeby poddawać wszystkich tresurze", "bo taka jest ich natura", "bo chcą wszystko kontrolować", "bo nie rozumieją, że socjalizm nie działa", "żeby wreszcie zapanował socjalizm", "dokładnie tak jak towarzysz Janosik", "zamiast pozwolić ludziom zarabiać", "żeby wyrwać kobiety z domu", "bo to jest w interesie tak zwanych ludzi pracy", "zamiast pozwolić decydować konsumentowi", "żeby nie opłacało się mieć dzieci", "zamiast obniżyć podatki", "bo nie rozumieją, że selekcja naturalna jest czymś dobrym", "żeby mężczyźni przestali być agresywni", "bo dzięki temu mogą brać łapówki", "bo dzięki temu mogą kraść", "bo dostają za to pieniądze", "bo tak się uczy w państwowej szkole", "bo bez tego (tfu!) demokracja nie może istnieć", "bo głupich jest więcej niż mądrych", "bo chcą tworzyć raj na ziemi", "bo chcą niszczyć cywilizację białego człowieka"],
		["co ma zresztą tyle samo sensu, co zawody w szachach dla debili", "co zostało dokładnie zaplanowane w Magdalence przez śp. generała Kiszcaka", "i trzeba być idiotą, żeby ten system popierać", "- ale nawet ja jeszcze dożyję normalnych czasów", "co dowodzi, że wyskrobano nie tych co trzeba", "a zwykłym ludziom wmawiają, że im coś \"dadzą\"", "- cóż - chcieliście (tfu!) demokracji, to macie", "- dlatego trzeba zlikwidować koryto, a nie zmieniać świnie", "a wystarczyłoby przestać wypłacać zasiłki", "podczas gdy normalni ludzie są uważani za dziwaków", "co w wieku XIX po prostu by wyśmiano", "- dlatego w społeczeństwie jest równość, a powinno być rozwarstwienie", "co prowadzi Polskę do katastrofy", "- dlatego trzeba przywrócić normalność", "ale w wolnej Polsce pójdą siedzieć", "przez kolejne kadencje", "o czym się nie mówi", "- i właśnie dlatego Europa umiera", "- ale przyjdą muzułmanie i zrobią porządek", "- tak samo zresztą jak za Hitlera", "- proszę zobaczyć, co się dzieje na Zachodzie, jeśli państwo mi nie wierzą", "co sto lat temu nikomu nie przyszłoby nawet do głowy"]
	]
	reply = ""

	for c in components:
		reply += " " + random.choice(c)

	reply += random.choice([".", "!"])

	await message.channel.send(reply)

c_korwin.command = r"korwin"


async def c_fullwidth(client, message):
	HALFWIDTH_TO_FULLWIDTH = str.maketrans(
		'0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&()*+,-./:;<=>?@[]^_`{|}~ ',
		'０１２３４５６７８９ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ！゛＃＄％＆（）＊＋、ー。／：；〈＝〉？＠［］＾＿‘｛｜｝～　')
	
	await message.channel.send(unidecode.unidecode(sh.get_args(message, True)).translate(HALFWIDTH_TO_FULLWIDTH))

c_fullwidth.command = r"(fullwidth|fw)"


async def c_letter_emoji(client, message):
	replacements = [
		(" ", "   "),
		("\(c\)", "©️"),
		("\(r\)", "®️"),
		("\(tm\)", "™️"),
		("cool", "🆒"),
		("free", "🆓"),
		("new", "🆕"),
		("ok", "🆗"),
		("sos", "🆘"),
		("zzz", "💤"),
		("ng", "🆖"),
		("cl", "🆑"),
		("up!", "🆙"),
		("vs", "🆚"),
		("id", "🆔"),
		("ab", "🆎"),
		("<3", "❤"),
		("100", "💯"),
		("a", "🇦"),
		("b", ":b:"),
		("c", "🇨"),
		("d", "🇩"),
		("e", "🇪"),
		("f", "🇫"),
		("g", "🇬"),
		("h", "🇭"),
		("i", "🇮"),
		("j", "🇯"),
		("k", "🇰"),
		("l", "🇱"),
		("m", "🇲"),
		("n", "🇳"),
		("o", "🇴"),
		("p", "🇵"),
		("q", "🇶"),
		("r", "🇷"),
		("s", "🇸"),
		("t", "🇹"),
		("u", "🇺"),
		("v", "🇻"),
		("w", "🇼"),
		("x", "🇽"),
		("y", "🇾"),
		("z", "🇿"),
		("0", ":zero:"),
		("1", ":one:"),
		("2", ":two:"),
		("3", ":three:"),
		("4", ":four:"),
		("5", ":five:"),
		("6", ":six:"),
		("7", ":seven:"),
		("8", ":eight:"),
		("9", ":nine:"),
		("\+", "➕"),
		("-", "➖"),
		("!\?", "⁉"),
		("!!", "‼"),
		("\?", "❓"),
		("!", "❗"),
		("#", ":hash:"),
		("\*", ":asterisk:"),
		("\$", "💲")
	]
	
	ret = unidecode.unidecode(sh.get_args(message, True))
	
	for e in replacements:
		ret = re.sub(e[0], " {} ".format(e[1]), ret, flags=re.I)
	
	await message.channel.send(ret)

c_letter_emoji.command = r"b"


async def c_memberlist(client, message):
	ret = ""

	x = message.guild.members
	for member in x:
		ret += member.name + "\n"
	
	await message.channel.send(ret)

c_memberlist.command = r"members"


# -------------------------------------
# funkcje używające seed
# -------------------------------------


async def c_czy(client, message):
	response = ""
	responses_yes = ["Tak", "Tak", "Na pewno", "Jeszcze się pytasz?", "Tak (no homo)", "Zaiste", "Teraz już tak", "A czy papież sra w lesie?", "Jak najbardziej", "Jeszcze jak", "Jest możliwe", "Owszem", "Czemu nie", "No w sumie...", "Nom", "W rzeczy samej", "Na bank", "Skoro tak mówisz, to nie będę zaprzeczał"]
	responses_no = ["Nie", "Nie", "To mało prawdopodobne", "Nie sądzę", "Tak (żartuję, hehe)", "No chyba cię pambuk opuścił", "Raczej nie", "Jeszcze nie", "Gówno prawda", "Otóż nie", "Niep", "Akurat", "Nawet o tym nie myśl", "Bynajmniej", "Co ty gadasz", "Chyba ty"]
	responses_dunno = ["Nie wiem", "Być może", "Hehe))))))))))))))))))", "Może kiedyś", "Jeszcze nie wiem", "Daj mi chwilę to się zastanowię", "Nie wiem, spytaj {}".format(get_random_nickname(message, "genitive")), "Tego nawet najstarsi górale nie wiedzą", "A jebnąć ci ciupaską?", "A co ja jestem, informacja turystyczna?"]

	if sh.is_female(message):
		responses_yes = responses_yes + ["Tak jest pani kapitan", "Trafiłaś w sedno"]
		responses_no = responses_no + ["Pani grażynko NIE"]
		responses_dunno = responses_dunno + ["Nie wiem zarobiony jestem przyjdź Pani jutro", "Co za debilka wymyśla te pytania", "Nie jesteś za młoda żeby pytać o takie rzeczy?", "Sama sobie odpowiedz"]
	else:
		responses_yes = responses_yes + ["Tak jest panie kapitanie", "Trafiłeś w sedno"]
		responses_no = responses_no + ["Panie januszu NIE"]
		responses_dunno = responses_dunno + ["Nie wiem zarobiony jestem przyjdź Pan jutro", "Co za debil wymyśla te pytania", "Nie jesteś za młody żeby pytać o takie rzeczy?", "Sam sobie odpowiedz"]
	
	if random.random() < 0.45:
		response = random.choice(responses_yes)
	elif random.random() < (9/11):
		response = random.choice(responses_no)
	else:
		response = random.choice(responses_dunno)
	
	await message.reply(response)

c_czy.command = r"czy"
c_czy.params = ["zapytanie"]

async def c_ile(client, message):
	if random.randint(0,50) < 1:
		replies = ["Fafnaście", "Szyberdzieści brlndpięć", "Czypiendziesiont", "Pisiont", "Mniej niz zero", "Tyle ile Pudzian bierze na klatę jak ma dobry dzień", "Sto tysięcy milionów"]
		await message.reply(random.choice(replies))
	else:
		zeros = random.randint(1,4)
		await message.reply(str(random.randint(pow(10, zeros-1), pow(10, zeros))))

c_ile.command = r"(ile|ilu)"
c_ile.params = ["zapytanie"]

async def c_ocen(client, message):
	ocena = random.randint(1, 10)
	doda = ""
	znak = ""
	if ocena < 10 and ocena > 0:
		doda = random.choice(["", ",5", "-", "+"])
	if ocena > 7:
		znak = random.choice(["", "+ <:znak:391940544458391565>", "- Berlin poleca", ""])
	
	await message.reply(str(ocena) + doda + "/10 " + znak)

c_ocen.command = r"ocen"
c_ocen.params = ["zapytanie"]


async def c_taknie(client, message):
	await message.reply(random.choice(["Tak", "Nie"]))

c_taknie.command = r"(taknie|tn)"
c_taknie.params = ["zapytanie"]


async def c_moneta(client, message):
	await message.reply(random.choice(["Orzeł", "Reszka"]))

c_moneta.command = r"moneta"


async def c_abcd(client, message):
	await message.reply(random.choice(["A", "B", "C", "D"]))

c_abcd.command = r"abcd"

# -------------------------------------
# kto / kim / komu / kogo
# -------------------------------------

async def c_gdzie(client, message):
	prefix = ["Pod mostem", "W dupie", "Na głowie", "Na kompie", "W parafii", "W koszu", "W fapfolderze", "Na rowerze", "Na penisie", "W Hondzie", "W portfelu", "W czipsach", "W brodzie Gofra"]
	suffix = [get_random_nickname(message, "genitive"), "na wydziale elektrycznym", "w Kathowicach", "w Sosnowcu", "u Kath w piwnicy", "we Wrocławiu", "w Szczecinie", "w Brwinowie", "w Warszawie", "w Bogatyni", "w Golubiu-Dobrzynie", "w Rzeszowie", "w Krakowie", "w Bydgoszczy", "w Magdalence przy stole z pozostałymi zdrajcami", "tam gdzie stało ZOMO", "na serwerze Interii", "w Gołodupczynie", "w kinie w Berlinie", "w redakcji CD-Action", "naprawdę mnie kusi żeby napisać \"w dupie\"", "w bagażniku Hondy nevki", "w Pendolino", "za górami, za lasami, za siedmioma dolinami...", "w bagnie Shreka", "w telezakupach Mango"]
	await message.reply(random.choice(prefix) + " " + random.choice(suffix))

c_gdzie.command = r"gdzie"
c_gdzie.params = ["zapytanie"]

async def c_kiedy(client, message):
	random_date = time.strftime("%Y-%m-%d %H:%M", time.localtime(time.time() + random.randint(3600, 31622400)))
	replies = ["O wpół do dziesiątej rano w Polsce", "Wczoraj", "Jutro", "Jak przyjdą szwedy", "W trzy dni po premierze Duke Nukem Forever 2", "Dzień przed końcem świata", "Nigdy", "Jak dojdą pieniądze", "Za godzinkę", "Kiedy tylko sobie życzysz", "Gdy przestaniesz zadawać debilne pytania", "Jak wybiorą czarnego papieża", "Już za cztery lata, już za cztery lata", "Na sylwestrze u P_aula", "O 3:33", "O 21:37", "Jak Kath napisze magisterkę", "Jak Dracia zrobi wszystko co musi kiedyś zrobić", "Jak KatajNapsika wróci na Discorda", "Jak Paul wejdzie do platyny", "Jak Fel znowu zgrubnie", "Gdy Aiden zgoli rude kudły", "Dzień po wybuchowym debiucie Brylanta", "Za 12 lat", "Gdy Martius przestanie pierdolić o ptakach", "Jak podbiel zje mi dupę", "A co ja jestem, informacja turystyczna?", "Jak wreszcie wyjebiemy stąd Nargoga", "Jak Debiru awansuje do seniora", "Jak kanau_fela zamknie FBI", "Już tej nocy w twoim łóżku", "Jak Strejlau umrze bo jest stary", "Nie", "Jak się skończy pandemia", "Jak Kataj skończy 12 lat", random_date]
	
	if sh.is_female(message):
		replies = replies + ["Gdy wreszcie znajdziesz chłopaka"]
	else:
		replies = replies + ["Gdy wreszcie znajdziesz dziewczynę"]
	
	await message.reply(random.choice(replies))

c_kiedy.command = r"kiedy"
c_kiedy.params = ["zapytanie"]

async def c_kto(client, message):
	await message.reply(get_random_nickname(message, "nominative"))

c_kto.command = r"kto"
c_kto.params = ["zapytanie"]

async def c_czyj(client, message):
	await message.reply(get_random_nickname(message, "genitive", sh.get_command(message)))

c_czyj.command = r"(z\s|u\s|o\s|na\s|za\s|od\s|do\s|w\s)?(czyi(m|mi|ch)|czyj(a|e|ego|ej)?)"
c_czyj.params = ["zapytanie"]

async def c_komu(client, message):
	await message.reply(get_random_nickname(message, "dative"))

c_komu.command = r"komu"
c_komu.params = ["zapytanie"]

async def c_kogo(client, message):
	await message.reply(get_random_nickname(message, "genitive", sh.get_command(message)))

c_kogo.command = r"(z\s|u\s|od\s|do\s)kogo"
c_kogo.params = ["zapytanie"]

async def c_kogo_bier(client, message):
	await message.reply(get_random_nickname(message, "accusative", sh.get_command(message)))

c_kogo_bier.command = r"(o\s|na\s|za\s|w\s)?kogo"
c_kogo_bier.params = ["zapytanie"]

async def c_kim(client, message):
	await message.reply(get_random_nickname(message, "instrumental", sh.get_command(message)))

c_kim.command = r"(z\s|za\s)?kim"
c_kim.params = ["zapytanie"]

async def c_kim_msc(client, message):
	await message.reply(get_random_nickname(message, "locative", sh.get_command(message)))

c_kim_msc.command = r"(o\s|na\s|w\s)kim"
c_kim_msc.params = ["zapytanie"]
