import random
import asyncio

import billy_shared as sh
from billy_c_img import c_wypierdalaj as img_wypierd

# -------------------------------------
# gaywards
# -------------------------------------

async def f_ohshitimsorry(client, message):
	await message.channel.send("sorry for what? <:podbiel:326424787121602560>")

f_ohshitimsorry.command = r'^oh shit,? I(\')?m sorry'
f_ohshitimsorry.prob = 1.0

async def f_sorryforwhat(client, message):
	await message.channel.send("our dad told us not to be ashamed of our dicks <:podbiel:326424787121602560>")

f_sorryforwhat.command = r'^sorry for what'
f_sorryforwhat.prob = 1.0

async def f_nottobeashamed(client, message):
	await message.channel.send("especially since they're such good size and all <:podbiel:326424787121602560>")

f_nottobeashamed.command = r'our dad told us not to be ashamed of our dicks'
f_nottobeashamed.prob = 1.0

async def f_iseethat(client, message):
	await message.channel.send("yeah, I see that, daddy gave you good advice <:mhhhmm:256873687871913984>")

f_iseethat.command = r'specially since (it(\')?s|theyre|they\'re) such good size'
f_iseethat.prob = 1.0

async def f_goodadvice(client, message):
	await message.channel.send("daddy gave you good advice <:mhhhmm:256873687871913984>")
	
f_goodadvice.command = r'^yea(h)?(,)? i see that$'
f_goodadvice.prob = 1.0

async def f_itgetsbigger(client, message):
	await message.channel.send("it gets bigger when I pull on it <:podbiel:326424787121602560>")

f_itgetsbigger.command = r'daddy gave you good advice'
f_itgetsbigger.prob = 1.0

async def f_mmmm(client, message):
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
	await message.channel.send(ret + " <:mhhhmm:256873687871913984>")

f_mmmm.command = r'^it gets bigger when I pull'
f_mmmm.prob = 1.0

async def f_iriptheskin(client, message):
	await message.channel.send("sometimes I pull it on so hard, I rip the skin! <:podbiel:326424787121602560>")

f_iriptheskin.command = r'^m[mh]{9,}'
f_iriptheskin.prob = 1.0

async def f_mydaddytold(client, message):
	await message.channel.send("my daddy told me few things too <:mhhhmm:256873687871913984>")

f_mydaddytold.command = r'^sometimes I pull it on so hard(,)? I rip the skin'
f_mydaddytold.prob = 1.0

async def f_nottorip(client, message):
	await message.channel.send("like, uh, how not to rip the skin by using someone else's mouth <:mhhhmm:256873687871913984>")

f_nottorip.command = r'my daddy (told|taught) me few things too'
f_nottorip.prob = 1.0

async def f_willyoushowme(client, message):
	await message.channel.send("will you show me? <:podbiel:326424787121602560>")

f_willyoushowme.command = r'how not to rip the skin by using someone else(\')?s mouth'
f_willyoushowme.prob = 1.0

async def f_idberighthappy(client, message):
	await message.channel.send("I'd be right happy to! <:mhhhmm:256873687871913984>")

f_idberighthappy.command = r'^will you show me'
f_idberighthappy.prob = 1.0

# -------------------------------------
# funkcje sprawdzające całą wypowiedź
# -------------------------------------

async def f_cogowno(client, message):
	await message.channel.send(random.choice(["gówno 1:0", "chujów sto 1:0"]))

f_cogowno.command = r'^(co|czo)\b'
f_cogowno.prob = 0.00675

async def f_czyzby(client, message):
	await message.channel.send("chyba ty")

f_czyzby.command = r'(czyzby|czyżby)'
f_czyzby.prob = 0.05

async def f_guten(client, message):
	await message.channel.send("Schwuchtel Arsch in der Nähe!!!")

f_guten.command = r'^guten tag$'
f_guten.prob = 0.5

async def f_maciek(client, message):
	await message.channel.send("Maćku")

f_maciek.command = r'^maciek$'
f_maciek.prob = 1.0

async def f_rucha(client, message):
	await message.channel.send("Ruchasz psa jak sra")

f_rucha.command = r'\.\.\.'
f_rucha.prob = 0.000675

async def f_wulg(client, message):
	responses = [
		"Może byś tak kurwa nie przeklinał", 
		"Co?", "Bez wulgaryzmów proszę", 
		"Na ten kanał zaglądają dzieci", 
		"Ostrożniej z językiem", 
		"To kanał PG13", 
		"Czy mam ci język uciąć?", 
		"Przestań przeklinać gejasie bo cię stąd wypierdolę dyscyplinarnie", 
		"Pambuk płacze jak przeklinasz", 
		"Mów do mnie brzydko", 
		"Kath bączy jak przeklinasz", 
		"Proszę tu nie przeklinać, to porządna knajpa", 
		"Nie ma takiego przeklinania chuju", 
		"блять))))))))))", 
		"Zamknij pizdę"
		]
	await message.channel.send(random.choice(responses))

f_wulg.command = r'(kurw|chuj|pierdol|pierdal|jeb)'
f_wulg.prob = 0.000675

async def f_witam(client, message):
	responses = [
		"Witam na kanale i życzę miłej zabawy", 
		"Cześć, kopę lat", 
		"Siemanko witam na moim kanale", 
		"Witam witam również", 
		"No elo", 
		"Salam alejkum", 
		"привет", 
		"Dzińdybry", 
		"Siemaszki", 
		"Serwus", 
		"Gitara siema", 
		"Dobrý den", 
		"Pozdrawiam, " + random.choice(["Piotr Gambal", "Mateusz Handzlik"]), 
		"Feedlysiemka " + str(message.author).split("#")[0].lower() + "ox"
		]
	await message.channel.send(random.choice(responses))

f_witam.command = r'(\bwitam|\bcześć\b|\bczesc\b|siema|szalom|\bjoł|shalom|dzi(n|ń)dybry|dzie(n|ń) dobry|siemka)'
f_witam.prob = 0.125

async def f_opti(client, message):
	await message.reply("Uprasza się o nieużywanie słowa \"opti\" na terenie politbiura. Dziękuję.")

f_opti.command = r"opti"
f_opti.prob = 0.05


async def f_tbh(client, message):
	await message.channel.send("smh")

f_tbh.command = r"^tbh$"
f_tbh.prob = 1.0


async def f_smh(client, message):
	await message.channel.send("tbh")

f_smh.command = r"^smh$"
f_smh.prob = 1.0


async def f_jakisgolas(client, message):
	replies = ["USUŃ TO", "A bana to byś nie chciał?", "<rzygi>", "Ty bamboclu"]
	
	if random.random() < 1/(len(replies)+1):
		await img_wypierd(client, message)
	else:
		await message.channel.send( random.choice(replies))

f_jakisgolas.command = r"vkPCjJM.jpg"
f_jakisgolas.prob = 1.0


async def f_jakisnervo(client, message):
	replies = ["nie", "no chyba nie"]
	
	await message.channel.send( random.choice(replies))

f_jakisnervo.command = r"(3tsmuxa|We8ms5m).jpg"
f_jakisnervo.prob = 1.0


async def f_takiezycie(client, message):
	await message.channel.send("Takie życie")

f_takiezycie.command = r"^chamsko"
f_takiezycie.prob = 0.05


async def f_wogole(client, message):
	await message.channel.send("Centralnie\nKamieniem go bez kitu")

f_wogole.command = r"^w og(o|ó)le$"
f_wogole.prob = 0.1


async def f_zabenya(client, message):
	await message.channel.send("ZABENY" + "A"*random.randrange(5, 16))

f_zabenya.command = r"^a{3,}$"
f_zabenya.prob = 0.1

async def f_marek(client, message):
	await message.channel.send("MAREK")

f_marek.command = r'^e{3,}$'
f_marek.prob = 1.0


#@asyncio.coroutine
#def f_nawzajem(client, message):
#	await message.channel.send("nawzajem")

#f_nawzajem.command = r"weso(l|ł)"
#f_nawzajem.prob = 1.0