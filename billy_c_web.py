import requests 
import random
import asyncio
import json
import re
import wolframalpha
import ftfy
import datetime
from bs4 import BeautifulSoup
from cleverwrap import CleverWrap

import time

import billy_shared as sh
from billy_c_translate import translate
from billy_c_yojc import c_rimshot as rimshot
from keys import WOLFRAM_ALPHA_KEY, CLEVERBOT_KEY

# How many times should the bot retry the query in case an error occurs?
retry_count = 3

cw = CleverWrap(CLEVERBOT_KEY)

headers_Get = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	'Accept-Language': 'en-US,en;q=0.5',
	'Accept-Encoding': 'gzip, deflate',
	'DNT': '1',
	'Connection': 'keep-alive',
	'Upgrade-Insecure-Requests': '1'
}


def google(q, image=False):
	s = requests.Session()
	q = '+'.join(q.split())
	url = 'https://www.google.com/search?q=' + q + '&ie=utf-8&oe=utf-8'
	if image == "isch":
		url += "&tbm=isch"
	elif image:
		url += "&tbm=isch&tbs=" + image
	
	try:
		r = s.get(url, headers=headers_Get, timeout=12.05)
	except:
		return False
	 
	soup = BeautifulSoup(r.text, "html.parser")

	# For testing logs
	#f = open("log", "r", encoding="utf-8")
	#logtext = f.read()
	#soup = BeautifulSoup(logtext, "html.parser")
	
	if image:
		search_wrapper = None
		rules = [{'jsname':'ik8THc'}, {'class':'rg_meta notranslate'}]
		
		hack = False
		
		for rule in rules:
			sh.debug("Checking rule")
			search_wrapper = soup.find_all('div', rule)
			if len(search_wrapper) != 0:
				sh.debug("Found rule")
				break
		
		if len(search_wrapper) == 0:
			hack = True
			search_wrapper = soup.find_all('script')
			
			try:
				indexes = range(0, -len(search_wrapper), -1)

				for index in indexes:
					sh.debug("Checking index " + str(index))
					json_text = re.sub("AF_initDataCallback.*?data:(function\(\){return)?", "", search_wrapper[index].string).strip()
					json_text = re.sub("(, sideChannel.*?)?}.*?$", "", json_text).strip()

					if sh.is_json(json_text) and len(json.loads(json_text)) > 30:
						sh.debug("First match")
						if len(json.loads(json_text)[31]) > 0:
							sh.debug("Second match")
							search_wrapper = json.loads(json_text)[31][0][12][2]
							break
						else:
							sh.debug("Second match failed")
							return False
					else:
						if index == indexes[-1]:
							sh.debug("Last element reached")
							return r.text
						elif not sh.is_json(json_text):
							sh.debug("Not a valid JSON")
							continue
						else:
							sh.debug("Too short: " + len(json.loads(json_text)))
							continue
			except IndexError:
				sh.debug("IndexError")
				return r.text
		
		url = None
		
		for result_img in search_wrapper:
			tmp = ""
		
			if hack:
				if result_img[0] == 2:
					continue
				tmp = result_img[1][3][0]
			else:
				tmp = json.loads(result_img.string.strip())["ou"]
			
			banned_terms = ["x-raw-image", "lookaside.fbsbx.com", ".svg", "cdninstagram", "archiwum.allegro"]
			
			if any(term in tmp for term in banned_terms):
				sh.debug("This image comes from a blacklisted URL")
				continue
			else:
				url = tmp
				break
		
		if not url:
			return False
		
		if ("wikimedia" in url and "thumb" in url):
			url = re.sub(r"(.+?)(thumb/)(.+)(/.+)", r"\1\3", url)
		elif "wpimg" in url:
			url = re.sub(r"(.+\/\d+x\d+\/)(.+)", r"https://\2", url)
		
		result = {'url': url}
	else:
		search_wrapper_tag_defs = [
			{'class':'rc'},
			{'class':'tF2Cxc'}
		]

		for sw_tag_def in search_wrapper_tag_defs:
			search_wrapper = soup.find('div', sw_tag_def)

			if search_wrapper:
				sh.debug("Found search_wrapper")
				break

		if search_wrapper is None:
			sh.debug("search_wrapper is None - no results or an error occured")
			return False
		
		url = search_wrapper.find('a')["href"] 

		desc_tag_defs = [
			{'class':'st'},
			{'class':'aCOpRe'},
			{'class':'wuQ4Ob'},
			{'class':'WZ8Tjf'},
			{'class':'VwiC3b'},
			{'class':'yXK7lf'},
			{'class':'yDYNvb'},
			{'class':'lyLwlc'},
			{'class':'MUxGbd'}
		]

		try:
			text = re.sub(r"https?\S+", "", search_wrapper.find('a').text, flags=re.I).strip()
			debug_info_tag = {'class': 0, 'tag': '?'}

			sh.debug("Checking description tags")
			for desc_tag_def in desc_tag_defs:
				debug_info_tag["class"] = desc_tag_def["class"]
				desc_tag = search_wrapper.find('div', desc_tag_def)
				if desc_tag:
					debug_info_tag["tag"] = 'div'
					break
				else:
					desc_tag = search_wrapper.find('span', desc_tag_def)
					if desc_tag:
						debug_info_tag["tag"] = 'span'
						break

			if desc_tag:
				sh.debug("Desc tag found: {}.{}".format(debug_info_tag["tag"], debug_info_tag["class"]))
				desc = re.sub(r"https?\S+", "", desc_tag.text, flags=re.I).strip()
			else:
				sh.debug("Desc tag not found!")
				return r.text
		except:
			sh.debug("An unknown error occured")
			return r.text

		result = {'text': text, 'url': url, 'desc' : desc}
	
	return result

def yt(q):
	s = requests.Session()
	s.cookies.set("CONSENT", "YES+cb.20210328-17-p0.en+FX+836", domain=".youtube.com")
	q = '+'.join(q.split())
	url = 'https://www.youtube.com/results?search_query=' + q + '&sp=EgIQAQ%253D%253D'
	
	try:
		r = s.get(url, headers=headers_Get, timeout=12.05)
	except:
		return False

	sh.dump_errlog(r.text)
	
	regex = r'\\\"videoId\\\"\:\\\"(\S+?)\\\"'
	ret = re.search(regex, r.text)

	if ret is None:
		sh.debug("First regex failed")
		regex = r'\"videoId\"\:\"(\S+?)\"'
		ret = re.search(regex, r.text)
	
	if ret is not None:
		sh.debug("Found vid")
		result = {'url': 'https://www.youtube.com/watch?v=' + ret.groups()[0]}
	else:
		sh.debug("Second regex failed")
		return False
	
	
	return result

def numerki(q):
	s = requests.Session()
	url = 'https://www.nhentai.net/g/' + q + '/'
	
	try:
		r = s.get(url, timeout=12.05)
	except:
		return False
		
	parsed = BeautifulSoup(r.text, "html.parser")
	tagi = []
	
	for spa in parsed.find_all('span', {'class': 'tags'}):
		tagi.append(spa.text.strip())
	
	while("" in tagi): 
		sh.debug("Numerki - rem")
		tagi.remove("")
	
	#prepare msg
	result = ''
	
	for tag in tagi :
		result += '[' + tag + ']\n'
		
	return result

def tumblr_random(q):
	s = requests.Session()
	url = 'http://'+q+'.tumblr.com/random'
	
	try:
		r = s.get(url, headers=headers_Get, timeout=12.05)
		if r.url == url:
			return False
		else:
			return r.url
	except:
		return False

def suchar():
	if random.random() < 0.01:
		return "jogurt"
	
	s = requests.Session()
	url = 'http://piszsuchary.pl/losuj'
	
	try:
		r = s.get(url, headers=headers_Get, timeout=12.05)
	except:
		return False
	
	soup = BeautifulSoup(r.text, "html.parser")
	
	search_wrapper = soup.find('pre', {'class':'tekst-pokaz'})
	if search_wrapper is None:
		return False
	result = search_wrapper.string.strip()[:-17]
	
	return result

def cytat():
	s = requests.Session()
	url = 'http://www.losowe.pl/'
	
	try:
		r = s.get(url, headers=headers_Get, timeout=12.05)
	except:
		return False
	
	soup = BeautifulSoup(r.text, "html.parser")
	
	search_wrapper_c = soup.find('blockquote')
	search_wrapper_a = soup.find('div', {'id':'autor'})
	if search_wrapper_c is None or search_wrapper_a is None:
		return False
	result = {'content' : search_wrapper_c.string.strip(), 'author' : search_wrapper_a.string.strip()[:-22]}
	
	return result

def bzdur():
	s = requests.Session()
	def joke():
		url = "https://geek-jokes.sameerkumar.website/api"
		try:
			r = s.get(url, headers = headers_Get, timeout=12.05)
		except:
			return None
		return r.text.strip()[1:-1]
	def basically():
		url = "http://itsthisforthat.com/api.php?text"
		try:
			r = s.get(url, headers = headers_Get, timeout=12.05)
		except:
			return None
		return r.text.strip()
	def business():
		url = "https://corporatebs-generator.sameerkumar.website/"
		try:
			r = s.get(url, headers = headers_Get, timeout=12.05)
		except:
			return None
		return json.loads(r.text)["phrase"]
	def advice():
		url = "https://api.adviceslip.com/advice"
		try:
			r = s.get(url, headers = headers_Get, timeout=12.05)
		except:
			return None
		return json.loads(r.text)["slip"]["advice"]
	result = random.choice([joke, basically, business, advice])()
	return translate(result, out_lang="pl")[0]

def bash():
	s = requests.Session()
	url = 'http://www.losowe.pl/'
	
	try:
		r = s.get(url, headers=headers_Get, timeout=12.05)
	except:
		return False
	
	soup = BeautifulSoup(r.text, "html.parser")
	
	search_wrapper_c = soup.find('blockquote')
	search_wrapper_a = soup.find('div', {'id':'autor'})
	if search_wrapper_c is None or search_wrapper_a is None:
		return False
	result = {'content' : search_wrapper_c.string.strip(), 'author' : search_wrapper_a.string.strip()[:-22]}
	
	return result

# ---------

async def c_google(client, message):
	for i in range(retry_count):
		result = google(sh.get_args(message, True))
		
		if not result:
			continue
		else:
			break
	
	if isinstance(result, str):
		await message.channel.send(sh.dump_errlog_msg(result))
	elif not result:
		await message.reply("Brak wyników, albo Google się zesrało.")
	else:
		await message.reply(result["text"] + "\n" + result["url"])

c_google.command = r"(g|google)"
c_google.params = ["zapytanie"]
c_google.desc = "szukaj w Google"

async def c_wyjasnij(client, message):
	for i in range(retry_count):
		result = google(sh.get_args(message, True))
		
		if not result:
			continue
		else:
			break
	
	if isinstance(result, str):
		await message.channel.send(sh.dump_errlog_msg(result))
	elif not result:
		await message.reply("Brak wyników, albo Google się zesrało.")
	else:
		await message.reply(result["desc"] + "\n" + result["url"])

c_wyjasnij.command = r"(wyjasnij|explain)"
c_wyjasnij.params = ["zapytanie"]
c_wyjasnij.desc = "szukaj w Google, podaje treść"

async def c_google_image(client, message):
	for i in range(retry_count):
		result = google(sh.get_args(message, True), "isch")
		
		if not result or isinstance(result, str):
			continue
		else:
			break
	
	if isinstance(result, str):
		await message.channel.send(sh.dump_errlog_msg(result))
	elif not result:
		await message.reply("Brak wyników, albo Google się zesrało.")
	else:
		await message.reply(result["url"])

c_google_image.command = r"(i|img)"
c_google_image.params = ["zapytanie"]
c_google_image.desc = "szukaj obrazków w Google"


async def c_google_image_clipart(client, message):
	for i in range(retry_count):
		result = google(sh.get_args(message, True), "itp:clipart")
		
		if not result or isinstance(result, str):
			continue
		else:
			break
	
	if isinstance(result, str):
		await message.channel.send(sh.dump_errlog_msg(result))
	elif not result:
		await message.reply("Brak wyników, albo Google się zesrało.")
	else:
		await message.reply(result["url"])

c_google_image_clipart.command = r"clipart"
c_google_image_clipart.params = ["zapytanie"]
c_google_image_clipart.desc = "szukaj clipartów"


async def c_google_image_face(client, message):
	for i in range(retry_count):
		result = google(sh.get_args(message, True), "itp:face")
		
		if not result or isinstance(result, str):
			continue
		else:
			break
	
	if isinstance(result, str):
		await message.channel.send(sh.dump_errlog_msg(result))
	elif not result:
		await message.reply("Brzydal")
	else:
		await message.reply(result["url"])

c_google_image_face.command = r"(face|twarz)"
c_google_image_face.params = ["zapytanie"]
c_google_image_face.desc = "szukaj obrazków zawierających twarz"


async def c_google_image_gif(client, message):
	for i in range(retry_count):
		result = google(sh.get_args(message, True), "itp:animated")
		
		if not result or isinstance(result, str):
			continue
		else:
			break
	
	if isinstance(result, str):
		await message.channel.send(sh.dump_errlog_msg(result))
	elif not result:
		await message.reply("Brak wyników, albo Google się zesrało.")
	else:
		await message.reply(result["url"])

c_google_image_gif.command = r"gif"
c_google_image_gif.params = ["zapytanie"]
c_google_image_gif.desc = "szukaj animowanych obrazków"

async def c_wikipedia(client, message):
	for i in range(retry_count):
		result = google(sh.get_args(message, True) + " site:wikipedia.org")
		
		if not result:
			continue
		else:
			break
	
	if not result:
		await message.reply("Brak wyników, albo Wiki się zesrało.")
	else:
		await message.reply(result["text"] + "\n" + result["desc"] + "\n" + result["url"])

c_wikipedia.command = r"(wiki?|wikipedia)"
c_wikipedia.params = ["zapytanie"]
c_wikipedia.desc = "szukaj w Wikipedii"


async def c_youtube(client, message):
	for i in range(retry_count):
		result = yt(sh.get_args(message, True))
		
		if not result:
			continue
		else:
			break
	
	if not result:
		await message.reply("Brak wyników, albo jutub się zesrał.")
	else:
		await message.reply(result["url"])

c_youtube.command = r"(yt|youtube)"
c_youtube.params = ["zapytanie"]
c_youtube.desc = "szukaj filmików na YT"


async def c_numerki(client, message):
	for i in range(retry_count):
		result = numerki(sh.get_args(message, True))
		
		if not result:
			continue
		else:
			break
	
	if not result:
		await message.reply("Brak hentajca, złe numerki?")
	else:
		await message.reply(result)

c_numerki.command = r"(numerki)"
c_numerki.params = ["zapytanie"]
c_numerki.desc = "wyświetl tagi hentajca po numerkach"

async def c_tumblr_r(client, message):
	for i in range(retry_count):
		result = tumblr_random(sh.get_args(message))
		
		if not result:
			continue
		else:
			break
	
	if not result:
		await message.reply("Wszystko tylko nie to")
	else:
		await message.reply(result)

c_tumblr_r.command = r"tumblrr(andom)?"
c_tumblr_r.params = ["tumblr"]
c_tumblr_r.desc = "losowy post z danego Tumblra"


async def c_zwierzaki(client, message):
	tumblr = random.choice(["fluffy-kittens", "cuteanimals", "cutest-critters"])
	result = tumblr_random(tumblr)
	
	if not result:
		await message.reply("ZJADŁEM WSZYSTKIE KOTY")
	else:
		await message.reply(result)

c_zwierzaki.command = r"zwierzaki"
c_zwierzaki.desc = "losowy Tumblr ze zwierzakami"


async def c_shitpostbot(client, message):
	result = tumblr_random("shitpostbot5k")
	
	if not result:
		await message.reply("I have a crippling depression")
	else:
		await message.reply(result)

c_shitpostbot.command = r"shitpost(bot)?"


async def c_wolfram(client, message):
	cw = wolframalpha.Client(WOLFRAM_ALPHA_KEY)
	res = cw.query(sh.get_args(message, True))
	
	if not hasattr(res, "results"):
		await message.reply("Nie ma takich rzeczy")
	else:
		await message.reply(next(res.results).text)

c_wolfram.command = r"(wa|wolfram)"
c_wolfram.params = ["zapytanie"]
c_wolfram.desc = "Wolfram Alpha"


async def c_suchar(client, message):
	result = suchar()
	
	if not result:
		await message.channel.send("jogurt")
	else:
		await message.channel.send(result)
		if random.random() < 0.4:
			await rimshot(client, message)

c_suchar.command = r"(suchar|martius)"
c_suchar.desc = "śmiej się razem z nami!"

async def c_bzdur(client, message):
    result = bzdur()
    if not result:
        await message.channel.send("Reasumując wszystkie aspekty kwintesencji tematu dochodzę do fundamentalnej konkluzji")
    else:
        await message.channel.send(result)
c_bzdur.command = r"(jacek|jaca|duptysta)"
c_bzdur.desc = "Głębokie teksty głębokiego kolegi"


async def c_cytat(client, message):
	result = cytat()
	
	if not result:
		await message.channel.send("Chamsko!\n*~Kathai_Nanjika*")
	else:
		await message.channel.send(result["content"] + "\n*~" + result["author"] + "*")

c_cytat.command = r"cytat"
c_cytat.desc = "życiowe maksymy"


async def c_cleverbot(client, message):
	await message.reply(ftfy.ftfy(cw.say(sh.get_args(message, True))))

c_cleverbot.command = r"(cb|cleverbot|(od)?powiedz|why|(dla)?czego|(dla)?czemu)"
c_cleverbot.params = ["zapytanie"]
c_cleverbot.desc = "spytaj bota o sens życia"


async def c_cleverbot_reset(client, message):
	cw.reset()

c_cleverbot_reset.command = r"(cb|cleverbot)r(eset)?"
c_cleverbot_reset.desc = "hidden"
