import asyncio
import random

import billy_shared as sh
import billy_rhymes as rhymes

# -------------------------------------
# rymy
# -------------------------------------

async def c_accounie(client, message):
	rhyme = rhymes.unie
	ret = "Accounie Accounie ty"
	custom = ["ślunski pierunie", "ajfonie", "żydomasonie"]
	await message.channel.send(ret + rhymes.compose(rhyme, custom))

c_accounie.command = r"accounie"
c_accounie.rhyme = True


async def c_aiden(client, message):
	rhyme = rhymes.en
	ret = "Aiden"
	custom = ["rudy aborygen"]
	await message.channel.send(ret + rhymes.compose(rhyme, custom))

c_aiden.command = r"aiden"
c_aiden.rhyme = True


async def c_behemort(client, message):
	rhyme = rhymes.ort
	ret = "Behemort"
	custom = ["zjada małe dzieci"]
	await message.channel.send(ret + rhymes.compose(rhyme, custom))

c_behemort.command = r"behemort"
c_behemort.rhyme = True


async def c_brylu(client, message):
	rhyme = rhymes.ylu
	ret = "Brylu Brylu ty"
	custom = ["debilu"]
	await message.channel.send(ret + rhymes.compose(rhyme, custom))

c_brylu.command = r"brylu"
c_brylu.rhyme = True


async def c_deffiku(client, message):
	rhyme = rhymes.iku
	ret = "deffiku deffiku ty"
	custom = ["mamuci siku"]
	await message.channel.send(ret + rhymes.compose(rhyme, custom))

c_deffiku.command = r"deffiku"
c_deffiku.rhyme = True


async def c_debilu(client, message):
	rhyme = rhymes.iru_ilu
	ret = "debiru debiru ty"
	custom = ["chory pojebie"]
	await message.channel.send(ret + rhymes.compose(rhyme, custom))

c_debilu.command = r"debilu"
c_debilu.rhyme = True


async def c_felu(client, message):
	rhyme = rhymes.elu
	ret = "felu felu ty"
	custom = ["taki fajniejszy podbielu", "niemiecki nieprzyjacielu"]
	await message.channel.send(ret + rhymes.compose(rhyme, custom))

c_felu.command = r"felu"
c_felu.rhyme = True


async def c_gen(client, message):
	rhyme = rhymes.en
	ret = "gen"
	custom = ["homoseksualny aborygen"]
	await message.channel.send(ret + rhymes.compose(rhyme, custom))

c_gen.command = r"gen"
c_gen.rhyme = True


async def c_goferze(client, message):
	rhyme = rhymes.erze
	ret = "Goferze Goferze ty"
	custom = ["krowi placku z bitą śmietaną i ekstra dużymi kawałkami owoców"]
	await message.channel.send(ret + rhymes.compose(rhyme, custom))

c_goferze.command = r"goferze"
c_goferze.rhyme = True


async def c_kathai(client, message):
	rhyme = rhymes.ai
	ret = "Kathai"
	custom = ["uahai dicki dwai", "s-senpai"]
	await message.channel.send(ret + rhymes.compose(rhyme, custom))

c_kathai.command = r"kath?a(i|j)"
c_kathai.rhyme = True


async def c_kathajec(client, message):
	rhyme = rhymes.jec
	ret = "Kathajec"
	custom = ["bez jajec"]
	await message.channel.send(ret + rhymes.compose(rhyme, custom))

c_kathajec.command = r"(kathajec|katajec)"
c_kathajec.rhyme = True


async def c_kicku(client, message):
	rhyme = rhymes.icku
	ret = "kicku kicku"
	custom = ["ty mały dicku", "thiccku"]
	await message.channel.send(ret + rhymes.compose(rhyme, custom))

c_kicku.command = r"kicku"
c_kicku.rhyme = True


async def c_komstuchu(client, message):
	rhyme = rhymes.uchu
	ret = "Komstuchu Komstuchu ty"
	custom = ["penisie w uchu", "tamburynie w ruchu"]
	await message.channel.send(ret + rhymes.compose(rhyme, custom))

c_komstuchu.command = r"komstuchu?"
c_komstuchu.rhyme = True


async def c_lghoscie(client, message):
	rhyme = rhymes.oscie
	ret = "LaserGhoście ty"
	custom = ["amigowca wal z gumowca"]
	await message.channel.send(ret + rhymes.compose(rhyme, custom))

c_lghoscie.command = r"lghoscie"
c_lghoscie.rhyme = True


async def c_nargogu(client, message):
	rhyme = rhymes.ogu
	ret = "Nargogu Nargogu ty"
	custom = ["mentalny kucu", "niemyty pierogu"]
	await message.channel.send(ret + rhymes.compose(rhyme, custom))

c_nargogu.command = r"nargogh?u"
c_nargogu.rhyme = True


async def c_nevko(client, message):
	rhyme = rhymes.ewko
	ret = "nevko nevko ty"
	custom = ["kociaro"]
	await message.channel.send(ret + rhymes.compose(rhyme, custom))

c_nevko.command = r"ne(w|v)ko"
c_nevko.rhyme = True


async def c_orgu(client, message):
	rhyme = rhymes.rgu
	ret = "orgu orgu ty"
	custom = ["cybochuju", "ruski czołgu"]
	await message.channel.send(ret + rhymes.compose(rhyme, custom))

c_orgu.command = r"orgu"
c_orgu.rhyme = True


async def c_pewkerze(client, message):
	rhyme = rhymes.erze
	ret = "Pewkerze Pewkerze ty"
	custom = ["lamerze"]
	await message.channel.send(ret + rhymes.compose(rhyme, custom))

c_pewkerze.command = r"(pewkerze|palkerze|pałkerze)"
c_pewkerze.rhyme = True


async def c_podbielu(client, message):
	rhyme = rhymes.elu
	ret = "podbielu podbielu ty"
	custom = ["łysy cwelu", "analny skurwielu", "odbyta niszczycielu"]
	await message.channel.send(ret + rhymes.compose(rhyme, custom))

c_podbielu.command = r"podbielu"
c_podbielu.rhyme = True


async def c_polipie(client, message):
	rhyme = rhymes.ipie
	ret = "POLIPie POLIPie ty"
	custom = ["glucie z nosa", "najserdeczniejszy przyjacielu"]
	await message.channel.send(ret + rhymes.compose(rhyme, custom))

c_polipie.command = r"polipie"
c_polipie.rhyme = True


async def c_srane(client, message):
	rhyme = rhymes.rane
	ret = "rane rane"
	custom = ["pojebane", "witane witane", "w letspleju nagrane", "na jutubie obejrzane"]
	await message.channel.send(ret + rhymes.compose(rhyme, custom))

c_srane.command = r"srane"
c_srane.rhyme = True


async def c_rysiu(client, message):
	rhyme = rhymes.ysiu_isiu
	ret = "Rysiu Rysiu ty"
	custom = ["zwierzaku", "kiedyś miałaś lepszy brzuch", "bestio z Wadowic"]
	await message.channel.send(ret + rhymes.compose(rhyme, custom))

c_rysiu.command = r"rysiu"
c_rysiu.rhyme = True


async def c_seekerze(client, message):
	rhyme = rhymes.erze
	ret = "Seekerze Seekerze ty"
	custom = ["przestań mnie dotykać w nocy", "najlepszy przyjacielu R1Pa", "lubisz macierze", "białoruski drwalu"]
	await message.channel.send(ret + rhymes.compose(rhyme, custom))

c_seekerze.command = r"seekerze"
c_seekerze.rhyme = True


async def c_sermacieju(client, message):
	rhyme = rhymes.eju
	ret = "Sermacieju ty"
	custom = ["radości z życia złodzieju", "jebaku leśny"]
	await message.channel.send(ret + rhymes.compose(rhyme, custom))

c_sermacieju.command = r"sermacieju"
c_sermacieju.rhyme = True


async def c_tebie(client, message):
	rhyme = rhymes.ebie
	ret = "Tebie ty"
	custom = ["kurwo jerychońska", "特別"]
	await message.channel.send(ret + rhymes.compose(rhyme, custom))

c_tebie.command = r"tebie"
c_tebie.rhyme = True


async def c_tet(client, message):
	rhyme = rhymes.det_tet
	ret = "t3t"
	custom = ["naplet", "ty chuju"]
	await message.channel.send(ret + rhymes.compose(rhyme, custom))

c_tet.command = r"(tet|t3t)"
c_tet.rhyme = True


async def c_tetrisie(client, message):
	rhyme = rhymes.isie
	ret = "t3trisie ty"
	custom = ["afrożydowska kurwo"]
	await message.channel.send(ret + rhymes.compose(rhyme, custom))

c_tetrisie.command = r"(tet|t3t)risie"
c_tetrisie.rhyme = True


async def c_tetrzycie(client, message):
	rhyme = rhymes.ycie
	ret = "t3trzycie t3trzycie ty"
	custom = ["kapitanie mokrybąk"]
	await message.channel.send(ret + rhymes.compose(rhyme, custom))

c_tetrzycie.command = r"(tet|t3t)rzycie"
c_tetrzycie.rhyme = True


async def c_trepli(client, message):
	rhyme = rhymes.pli
	ret = "Trepli"
	custom = ["jest gorsza od Kath bo ma tylko jednego dicka"]
	await message.channel.send(ret + rhymes.compose(rhyme, custom))

c_trepli.command = r"trepli"
c_trepli.rhyme = True


async def c_turq(client, message):
	rhyme = rhymes.urku
	ret = "Turq Turq ty"
	custom = ["robotny fiucie"]
	await message.channel.send(ret + rhymes.compose(rhyme, custom))

c_turq.command = r"turq"
c_turq.rhyme = True


async def c_xysiu(client, message):
	rhyme = rhymes.ysiu_isiu
	ret = "Xysiu Xysiu ty"
	custom = ["żydowski rabinie"]
	await message.channel.send(ret + rhymes.compose(rhyme, custom))

c_xysiu.command = r"xysiu"
c_xysiu.rhyme = True


async def c_yojec(client, message):
	rhyme = rhymes.jec
	ret = "yojec"
	custom = ["srojec", "cyklotron"]
	await message.channel.send(ret + rhymes.compose(rhyme, custom))

c_yojec.command = r"yojec"
c_yojec.rhyme = True


# -------------------------------------
# jakies inne bzdety
# -------------------------------------


async def c_behe(client, message):
	ret = 'Be'
	for x in range(0, random.randint(1, 15)):
		ret += 'he'
	await message.channel.send(ret+'mort')

c_behe.command = r"behe"
c_behe.desc = "Behehemort"
c_behe.rhyme = True

async def c_hakken(client, message):
	ret = 'Ha'
	for x in range(0, random.randint(0, 14)):
		ret += 'ha'
	await message.channel.send(ret+'kken')

c_hakken.command = r"hakken"
c_hakken.desc = "Hahahakken"
c_hakken.rhyme = True


async def c_kath(client, message):
	ret = 'Ka'
	for x in range(0, random.randint(0, 14)):
		ret += 'ka'
	ret += "thai_Na"
	for x in range(0, random.randint(0, 14)):
		ret += 'na'
	await message.channel.send(ret+'njika')

c_kath.command = r"kath"
c_kath.desc = "Kakakathai"
c_kath.rhyme = True


async def c_kicek(client, message):
	await message.channel.send(random.choice(["kicek", "kiceg"]) + " mały " + random.choice(["bicek", "dicek", "cycek"]))

c_kicek.command = r"kice(k|g)"
c_kicek.desc = "kicek mały..."
c_kicek.rhyme = True


async def c_nargog(client, message):
	ret = 'Na'
	for x in range(0, random.randint(0, 14)):
		ret += 'na'
	await message.channel.send(ret+'rgogh')

c_nargog.command = r"nargog(h)?"
c_nargog.desc = "Nananargogh"
c_nargog.rhyme = True


async def c_polip(client, message):
	ret = 'POLI'
	for x in range(0, random.randint(0, 14)):
		ret += 'POLI'
	await message.channel.send(ret + random.choice(["P", "POLIK"]))

c_polip.command = r"polip"
c_polip.desc = "POLIPOLIPOLIK"
c_polip.rhyme = True


async def c_rane(client, message):
	ret = "Ra"
	for x in range(0, 14):
		if random.randint(0, 1) == 1:
			ret += 'ra'
		else:
			ret += "ne"
	await message.channel.send(ret)

c_rane.command = r"rane"
c_rane.desc = "raranene"
c_rane.rhyme = True


async def c_teb(client, message):
	ret = 'Teb'
	for x in range(0, random.randint(0, 14)):
		ret += 'eb'
	await message.channel.send(ret + "eg")

c_teb.command = r"teb"
c_teb.desc = "Tebebeg"
c_teb.rhyme = True


async def c_tebeg(client, message):
	await message.channel.send("T E B E G\nE\nB\nE\nG")

c_tebeg.command = r"tebeg"
c_tebeg.desc = "T E B E G"
c_tebeg.rhyme = True


async def c_yojc(client, message):
	count = random.randint(0, 14)
	flag = random.randint(0, 1)
	
	if count < 2:
		where = 0
	else:
		where = random.randint(1, count-1)
	
	ret = "yo"
	
	for x in range(0, count):
		ret += 'yo'
		if flag == 1 and x == where:
			ret += "motherfucker"
	
	await message.channel.send(ret+'jc')

c_yojc.command = r"yojc"
c_yojc.desc = "yoyoyojc"
c_yojc.rhyme = True
