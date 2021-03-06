import requests 
import asyncio
import json
import re
import random

import billy_shared as sh

# How many times should the bot retry the query in case an error occurs?
retry_count = 3

def parse_args(msg):
	in_lang = "auto"
	out_lang = "en"
	
	r = re.findall(r"(\:\S+ )", msg)
	
	if len(r) == 2:
		in_lang = r[0][1:-1]
		out_lang = r[1][1:-1]
	elif len(r) == 1:
		out_lang = r[0][1:-1]
	
	return {"msg" : msg[len("".join(re.findall(r"(\:\S+ )", msg))):], "in_lang" : in_lang, "out_lang" : out_lang}


def translate(text, in_lang='auto', out_lang='en', verify_ssl=True):
	raw = False
	if str(out_lang).endswith('-raw'):
		out_lang = out_lang[:-4]
		raw = True

	headers = {
		'User-Agent': 'Mozilla/5.0' +
		'(X11; U; Linux i686)' +
		'Gecko/20071127 Firefox/2.0.0.11'
	}

	query = {
		"client": "gtx",
		"sl": in_lang,
		"source": in_lang,
		"tl": out_lang,
		"dt": "t",
		"q": text,
	}
	url = "http://translate.googleapis.com/translate_a/single"

	for i in range(retry_count):
		#print(str(i) + ", " + in_lang + " => " + out_lang)
		result = requests.get(url, params=query, timeout=9.05, headers=headers,
							verify=verify_ssl).text

		if result == '[,,""]':
			return None, in_lang

		while ',,' in result:
			result = result.replace(',,', ',null,')
			result = result.replace('[,', '[null,')

		try:
			data = json.loads(result)
		except:
			if i == retry_count-1:
				sh.warn("\"" + text + "\", " + in_lang + " => " + out_lang, date=True)
				#return -1, result
				return text, False
			else:
				continue

		if raw:
			return str(data), 'en-raw'

		try:
			language = data[2]  # -2][0][0]
		except:
			language = '?'

		return ''.join(x[0] for x in data[0]), language


async def mangle(client, channel, text, dest="en", randomize=False, original=False):
	langs = ['auto']
	
	if randomize:
		lang_list = "af sq am ar hy az eu bn bs bg ca zh co hr cs da nl eo et fi fr fy gl ka de el gu ht ha iw hi hu is ig id ga it ja jw kn kk km ko ku lo lv lt lb mk mg ms ml mt mi mr mn ne no ny ps fa pt pa ro ru sm gd sr st sn sd si sk sl so es sw sv tl tg ta te th tr uk ur uz vi cy xh yi yo zu".split(" ")
		langs.extend(random.sample(lang_list, 8))
	elif original:
		langs.extend(['en', 'fr', 'de', 'es', 'it'])
	else:
		langs.extend(['fr', 'de', 'es', 'it', 'no', 'he', 'la', 'ja'])
	
	langs.append(dest)
	
	i = 1
	last_lang = langs[0]
	
	while i < len(langs):
		text = translate(text, last_lang, langs[i])

		if text and text[0] != -1:
			if text[1]:
				last_lang = langs[i]
			text = text[0]
		else:
			await channel.send(sh.dump_errlog_msg(text[1]))
			text = "dupa cycki"
			break
		
		i += 1
	
	return text


# ---------

async def c_tr(client, message):
	args = parse_args(sh.get_args(message))
	result = translate(args["msg"], args["in_lang"], args["out_lang"])
	
	if result[0] is None:
		await message.reply("Brak wynik??w, albo Google si?? zesra??o.")
	else:
		await message.reply("[" + result[1] + " => " + args["out_lang"] + "] " + result[0])

c_tr.command = r"tr"
c_tr.params = [":j??z_wej", ":j??z_wyj", "tekst"]
c_tr.desc = "t??umaczenie (parametry opcjonalne, domy??lnie auto => en)"

async def c_trp(client, message):
	result = translate(sh.get_args(message), "auto", "pl")
	
	if result[0] is None:
		await message.reply("Google nie zna j??zyka ??l??skiego, prosz?? tu takich rzeczy nie wkleja??.")
	else:
		await message.reply("[" + result[1] + " => pl] " + result[0])

c_trp.command = r"trp"
c_trp.params = ["tekst"]
c_trp.desc = "t??umaczenie na j. polski"

async def c_mangle(client, message):
	await message.reply((await mangle(client, message.channel, sh.get_args(message), "en")))

c_mangle.command = r"mangle"
c_mangle.params = [":j??z_wej", ":j??z_wyj", "tekst"]
c_mangle.desc = "najlepsze t??umaczenie (domy??lnie auto => en)"

async def c_manglep(client, message):
	await message.reply((await mangle(client, message.channel, sh.get_args(message), "pl")))

c_manglep.command = r"manglep"
c_manglep.params = ["tekst"]
c_manglep.desc = "najlepsze t??umaczenie na polski"

async def c_mangler(client, message):
	await message.reply((await mangle(client, message.channel, sh.get_args(message), "pl", True)))

c_mangler.command = r"mangler"
c_mangler.params = ["tekst"]
c_mangler.desc = "najlepsze t??umaczenie na polski (losowo dobierana kolejno???? t??umacze??)"

async def c_mangleo(client, message):
	await message.reply((await mangle(client, message.channel, sh.get_args(message), "pl", False, True)))

c_mangleo.command = r"mangleo"
c_mangleo.params = ["tekst"]
c_mangleo.desc = "najlepsze t??umaczenie na polski (stary algorytm)"

async def c_manglew(client, message):
	tmp = sh.get_args(message).split(" ", 1)
	ret = sh.insert_word(tmp[0], tmp[1])
	await message.reply((await mangle(client, message.channel, ret, "pl")))

c_manglew.command = r"(manglew|wstaglep)"
c_manglew.params = ["s??owo", "zdanie"]
c_manglew.desc = "wstaw + manglep"

async def c_manglekn(client, message):
	result = translate(sh.get_args(message), "auto", "pl")

	if result[0] is None:
		await message.reply("Google nie zna j??zyka ??l??skiego, prosz?? tu takich rzeczy nie wkleja??.")
	else:
		text = sh.insert_word("kurwa", result[0]).replace("\n", " ")
		await message.reply((await mangle(client, message.channel, text, "pl")))

c_manglekn.command = r"manglekn"
c_manglekn.params = ["zdanie"]
c_manglekn.desc = "manglep z ekstra du??ymi kawa??kami wulgaryzm??w i bez enter??w"

async def c_manglek(client, message):
	result = translate(sh.get_args(message), "auto", "pl")

	if result[0] is None:
		await message.reply("Google nie zna j??zyka ??l??skiego, prosz?? tu takich rzeczy nie wkleja??.")
	else:
		text = sh.insert_word("kurwa", result[0])
		await message.reply((await mangle(client, message.channel, text, "pl")))

c_manglek.command = r"manglek"
c_manglek.params = ["zdanie"]
c_manglek.desc = "manglep z ekstra du??ymi kawa??kami wulgaryzm??w"

async def c_hakan(client, message):
	result = translate(sh.get_args(message), "auto", "pl")

	if result[0] is None:
		await message.reply("Google nie zna j??zyka ??l??skiego, prosz?? tu takich rzeczy nie wkleja??.")
	else:
		text = sh.insert_word("hakan", result[0])
		await message.reply((await mangle(client, message.channel, text, "pl")))

c_hakan.command = r"(al)?haka(n|m)"
c_hakan.params = ["zdanie"]
c_hakan.desc = "manglep z podw??jnym Hakkenem na cienkim cie??cie"
