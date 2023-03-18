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
from billy_c_img import c_smieszne as smieszne
from billy_c_img import c_niesmieszne as niesmieszne

from keys import WOLFRAM_ALPHA_KEY, CLEVERBOT_KEY
from config import REQUESTS_RETRY_COUNT, REQUESTS_TIMEOUT, REQUESTS_DUMP_GOOGLE_TO_FILE, REQUESTS_DUMP_YOUTUBE_TO_FILE, REQUESTS_HEADERS

# Debug Google request with a file (passed as argument for bot command)
# Bot must be running in developer mode!
DEBUG_GOOGLE_FILE = False

# How many times should the bot retry the query in case an error occurs?
retry_count = REQUESTS_RETRY_COUNT if not sh.testing else 1

cw = CleverWrap(CLEVERBOT_KEY)

def google(q, image=False):
	if sh.testing and DEBUG_GOOGLE_FILE:
		# For testing logs
		f = open(q, "r", encoding="utf-8")
		webpage = f.read()
	else:
		s = requests.Session()
		s.cookies.set("CONSENT", "YES+cb.20220111-10-p0.en+FX+462", domain=".google.com")
		q = '+'.join(q.split())
		url = 'https://www.google.com/search?q=' + q + '&ie=utf-8&oe=utf-8'
		if image == "isch":
			url += "&tbm=isch"
		elif image:
			url += "&tbm=isch&tbs=" + image
		
		try:
			r = s.get(url, headers=REQUESTS_HEADERS, timeout=REQUESTS_TIMEOUT)
		except:
			return False
		
		webpage = r.text
		
		if sh.testing or REQUESTS_DUMP_GOOGLE_TO_FILE:
			sh.debug("Dumped server response to {}".format(sh.dump_errlog(webpage, "google")))
	
	soup = BeautifulSoup(webpage, "html.parser")
	
	if image:
		search_wrapper = None
		rules = [{'jsname':'ik8THc'}, {'class':'rg_meta notranslate'}]
		
		hack = False
		new_search_hack = False
		
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

					#if DEBUG_GOOGLE_FILE:
					#	sh.debug("----- ----- -----")
					#	sh.debug(search_wrapper[index])
					#	sh.debug("----- ----- -----")
					
					json_text = re.sub("AF_initDataCallback.*?data:(function\(\){return)?", "", search_wrapper[index].string or "").strip()
					json_text = re.sub("(, sideChannel.*?)}.*?$", "", json_text).strip()

					if not sh.is_json(json_text):
						sh.debug("Not a valid JSON")
						continue
					
					json_result = json.loads(json_text)

					if len(json_result) > 30:
						sh.debug("Trying old method")
						if json_result[31] and len(json_result[31]) > 0:
							sh.debug("Old method worked")

							for arr in json_result[31]:
								if len(arr) > 8 and arr[7] == "b-TOP_PLA":
									continue
								else:
									search_wrapper = arr[12][2]
									break
							
							break
						else:
							sh.debug("Old method failed, trying something else")
							new_search_hack = True

							if json_result[56] and len(json_result[56]) > 0:
								search_wrapper = []
								magic_number = "444383007"

								preprocessed_string = ""
								bracket_counter = 0

								inside_string_flag = False
								previous_char = None

								for char in json.dumps(json_result[56]):
									if char == "\"" and previous_char != "\\":
										#sh.debug("Changing string state")
										inside_string_flag = not inside_string_flag
										preprocessed_string += char
									elif inside_string_flag: 
										#sh.debug("Inside string")
										preprocessed_string += char
									elif char == "{":
										#sh.debug("Starting bracket")
										bracket_counter += 1
										if bracket_counter == 1:
											preprocessed_string += "!STARTING_BRACKET!{"
										else:
											preprocessed_string += "{"
									elif char == "}":
										#sh.debug("Closing bracket")
										bracket_counter -= 1
										if bracket_counter == 0:
											preprocessed_string += "}!ENDING_BRACKET!"
										else:
											preprocessed_string += "}"
									else:
										#sh.debug(char)
										preprocessed_string += char
									
									previous_char = char

								raw_dicts = re.findall("!STARTING_BRACKET!.+?!ENDING_BRACKET!", preprocessed_string)

								for result_dict in raw_dicts:
									sh.debug("----- ----- -----")
									sh.debug(re.sub("!(STARTING|ENDING)_BRACKET!", "", result_dict))
									sh.debug("----- ----- -----")

									dict_json = json.loads(re.sub("!(STARTING|ENDING)_BRACKET!", "", result_dict))

									if magic_number not in dict_json:
										sh.debug("Magic number not found")
									elif dict_json[magic_number] and dict_json[magic_number][1] and dict_json[magic_number][1][3] and dict_json[magic_number][1][3][0]:
										sh.debug("It's a result: {}".format(dict_json[magic_number][1][3][0]))
										search_wrapper.append(dict_json[magic_number][1][3][0])
									else:
										sh.debug("Magic number found, but something else is wrong")
								
							break
					else:
						if index == indexes[-1]:
							sh.debug("Last element reached")
							return webpage
						else:
							sh.debug("Too short: {}".format(len(json.loads(json_text))))
							continue
			except IndexError:
				sh.debug("An IndexError occurred!")
				return webpage
		
		url = None
		
		for result_img in search_wrapper:
			tmp = ""
		
			if new_search_hack:
				if result_img[0] != "h":
					continue
				
				if DEBUG_GOOGLE_FILE:
					sh.debug("result_img: {}".format(result_img))
				
				tmp = result_img
			elif hack:
				if DEBUG_GOOGLE_FILE:
					sh.debug("result_img[0]: {}".format(result_img[0]))

				if result_img[0] != 1:
					continue
				
				if DEBUG_GOOGLE_FILE:
					sh.debug("result_img: {}".format(result_img))
				
				try:
					tmp = result_img[1][3][0]
				except:
					sh.warn("Google image search failure, dumped server response to {}".format(sh.dump_errlog(webpage, "google")))
			else:
				tmp = json.loads(result_img.string.strip())["ou"]
			
			banned_terms = ["x-raw-image", "lookaside.fbsbx.com", ".svg", "cdninstagram", "archiwum.allegro", "lifesize.com", "tiktok.com"]
			
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
		r = s.get(url, headers=REQUESTS_HEADERS, timeout=REQUESTS_TIMEOUT)
	except:
		return False

	if sh.testing or REQUESTS_DUMP_YOUTUBE_TO_FILE:
		sh.debug("Dumped server response to {}".format(sh.dump_errlog(r.text, "youtube")))
	
	regex = r'\{\"videoRenderer\"\:\{\"videoId\"\:\"(\S+?)\"'
	ret = re.search(regex, r.text)

	if ret is None:
		sh.debug("First regex failed")
		regex = r'\\\{\\\"videoRenderer\\\"\\\:\\\{\\\"videoId\\\"\\\:\\\"(\S+?)\\\"'
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
	s.cookies.set("cf_clearance", "34235b3c0c6639f951778a335e3c39bdd6827580-1666707106-0-150", domain=".nhentai.net")
	s.cookies.set("csrftoken", "2DqJTamPd9HIWuqfqvKFAT28DWB6GC979aP1cK9PJFrBm22Ta0DstDssDGd7Scly", domain="nhentai.net")
	url = 'https://www.nhentai.net/g/' + q + '/'

	sh.debug("Fetching numerki from {}".format(url))
	
	try:
		r = s.get(url, timeout=REQUESTS_TIMEOUT)
	except:
		sh.debug("OBJECTION!")
		return False
	
	if sh.testing:
		sh.debug("Dumped server response to {}".format(sh.dump_errlog(r.text, "numerki")))
		
	parsed = BeautifulSoup(r.text, "html.parser")
	tagi = []
	
	for spa in parsed.find_all('span', {'class': 'tags'}):
		sh.debug("Found tag {}".format(spa.text.strip()))
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
		r = s.get(url, headers=REQUESTS_HEADERS, timeout=REQUESTS_TIMEOUT)
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
		r = s.get(url, headers=REQUESTS_HEADERS, timeout=REQUESTS_TIMEOUT)
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
		r = s.get(url, headers=REQUESTS_HEADERS, timeout=REQUESTS_TIMEOUT)
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
			r = s.get(url, headers = REQUESTS_HEADERS, timeout=REQUESTS_TIMEOUT)
		except:
			return None
		return r.text.strip()[1:-1]
	def basically():
		url = "http://itsthisforthat.com/api.php?text"
		try:
			r = s.get(url, headers = REQUESTS_HEADERS, timeout=REQUESTS_TIMEOUT)
		except:
			return None
		return r.text.strip()
	def business():
		url = "https://corporatebs-generator.sameerkumar.website/"
		try:
			r = s.get(url, headers = REQUESTS_HEADERS, timeout=REQUESTS_TIMEOUT)
		except:
			return None
		return json.loads(r.text)["phrase"]
	def advice():
		url = "https://api.adviceslip.com/advice"
		try:
			r = s.get(url, headers = REQUESTS_HEADERS, timeout=REQUESTS_TIMEOUT)
		except:
			return None
		return json.loads(r.text)["slip"]["advice"]
	result = random.choice([joke, basically, business, advice])()
	return translate(result, out_lang="pl")[0]

def bash():
	s = requests.Session()
	url = 'http://www.losowe.pl/'
	
	try:
		r = s.get(url, headers=REQUESTS_HEADERS, timeout=REQUESTS_TIMEOUT)
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
		await message.channel.send(sh.dump_errlog_msg(result, "c_google"))
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
		await message.channel.send(sh.dump_errlog_msg(result, "c_wyjasnij"))
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
		await message.channel.send(sh.dump_errlog_msg(result, "c_google_image"))
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
		await message.channel.send(sh.dump_errlog_msg(result, "c_google_image_clipart"))
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
		await message.channel.send(sh.dump_errlog_msg(result, "c_google_image_clipart"))
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
		await message.channel.send(sh.dump_errlog_msg(result, "c_google_image_gif"))
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
		if random.random() < 0.25:
			if random.random() < 0.33:
				await smieszne(client, message)
			elif random.random() < 0.5:
				await niesmieszne(client, message)
			else:
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
