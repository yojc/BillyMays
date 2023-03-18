cups = {
########################################
# EURO 2016
########################################
	"euro2016": {
		"regex": r"euro ?(20)?16",
		"win_pts": 3,
		"draw_pts": 1,
		"playoffs": False,
		"third_place_qual": True,
		"third_place_match": False,
		"teams": {
			"fra": {
				"name": "Francja",
				"group": "A",
				"extra_coeff": [8]
			},
			"rom": {
				"name": "Rumunia",
				"group": "A",
				"extra_coeff": [18]
			},
			"alb": {
				"name": "Albania",
				"group": "A",
				"extra_coeff": [31]
			},
			"sui": {
				"name": "Szwajcaria",
				"group": "A",
				"extra_coeff": [10]
			},
			"eng": {
				"name": "Anglia",
				"group": "B",
				"extra_coeff": [3]
			},
			"rus": {
				"name": "Rosja",
				"group": "B",
				"extra_coeff": [9]
			},
			"wal": {
				"name": "Walia",
				"group": "B",
				"extra_coeff": [28]
			},
			"svk": {
				"name": "Słowacja",
				"group": "B",
				"extra_coeff": [19]
			},
			"ger": {
				"name": "Niemcy",
				"group": "C",
				"extra_coeff": [1]
			},
			"ukr": {
				"name": "Ukraina",
				"group": "C",
				"extra_coeff": [14]
			},
			"pol": {
				"name": "Polska",
				"group": "C",
				"extra_coeff": [17]
			},
			"nir": {
				"name": "Irlandia Północna",
				"group": "C",
				"extra_coeff": [33]
			},
			"esp": {
				"name": "Hiszpania",
				"group": "D",
				"extra_coeff": [2]
			},
			"cze": {
				"name": "Czechy",
				"group": "D",
				"extra_coeff": [15]
			},
			"tur": {
				"name": "Turcja",
				"group": "D",
				"extra_coeff": [22]
			},
			"cro": {
				"name": "Chorwacja",
				"group": "D",
				"extra_coeff": [12]
			},
			"bel": {
				"name": "Belgia",
				"group": "E",
				"extra_coeff": [5]
			},
			"ita": {
				"name": "Włochy",
				"group": "E",
				"extra_coeff": [6]
			},
			"irl": {
				"name": "Irlandia",
				"group": "E",
				"extra_coeff": [23]
			},
			"swe": {
				"name": "Szwecja",
				"group": "E",
				"extra_coeff": [16]
			},
			"por": {
				"name": "Portugalia",
				"group": "F",
				"extra_coeff": [4]
			},
			"isl": {
				"name": "Islandia",
				"group": "F",
				"extra_coeff": [27]
			},
			"aus": {
				"name": "Austria",
				"group": "F",
				"extra_coeff": [11]
			},
			"hun": {
				"name": "Węgry",
				"group": "F",
				"extra_coeff": [20]
			}
		},
		"group_algorithm": [
			{
				"host": 1,
				"guest": 2
			},
			{
				"host": 3,
				"guest": 4
			},
			{
				"host": 1,
				"guest": 3
			},
			{
				"host": 2,
				"guest": 4
			},
			{
				"host": 4,
				"guest": 1
			},
			{
				"host": 2,
				"guest": 3
			}
		],
		"bracket_algorithm": [
			{
				"host": "A2",
				"guest": "C2"
			},
			{
				"host": "D1",
				"guest": "3"
			},
			{
				"host": "B1",
				"guest": "3"
			},
			{
				"host": "F1",
				"guest": "E2"
			},
			{
				"host": "C1",
				"guest": "3"
			},
			{
				"host": "E1",
				"guest": "D2"
			},
			{
				"host": "A1",
				"guest": "3"
			},
			{
				"host": "B2",
				"guest": "F2"
			}
		]
	},
########################################
# EURO 2020/2021
########################################
	"euro2021": {
		"regex": r"euro ?202[01]",
		"win_pts": 3,
		"draw_pts": 1,
		"playoffs": False,
		"third_place_qual": True,
		"third_place_match": False,
		"teams": {
			"tur": {
				"name": "Turcja",
				"group": "A",
				"extra_coeff": [14]
			},
			"ita": {
				"name": "Włochy",
				"group": "A",
				"extra_coeff": [2]
			},
			"wal": {
				"name": "Walia",
				"group": "A",
				"extra_coeff": [19]
			},
			"sui": {
				"name": "Szwajcaria",
				"group": "A",
				"extra_coeff": [9]
			},
			"den": {
				"name": "Dania",
				"group": "B",
				"extra_coeff": [15]
			},
			"fin": {
				"name": "Finlandia",
				"group": "B",
				"extra_coeff": [20]
			},
			"bel": {
				"name": "Belgia",
				"group": "B",
				"extra_coeff": [1]
			},
			"rus": {
				"name": "Rosja",
				"group": "B",
				"extra_coeff": [12]
			},
			"ned": {
				"name": "Holandia",
				"group": "C",
				"extra_coeff": [11]
			},
			"ukr": {
				"name": "Ukraina",
				"group": "C",
				"extra_coeff": [6]
			},
			"aus": {
				"name": "Austria",
				"group": "C",
				"extra_coeff": [16]
			},
			"mad": {
				"name": "Macedonia Północna",
				"group": "C",
				"extra_coeff": [30]
			},
			"eng": {
				"name": "Anglia",
				"group": "D",
				"extra_coeff": [3]
			},
			"cro": {
				"name": "Chorwacja",
				"group": "D",
				"extra_coeff": [10]
			},
			"sco": {
				"name": "Szkocja",
				"group": "D",
				"extra_coeff": [29]
			},
			"cze": {
				"name": "Czechy",
				"group": "D",
				"extra_coeff": [18]
			},
			"spa": {
				"name": "Hiszpania",
				"group": "E",
				"extra_coeff": [5]
			},
			"swe": {
				"name": "Szwecja",
				"group": "E",
				"extra_coeff": [17]
			},
			"pol": {
				"name": "Polska",
				"group": "E",
				"extra_coeff": [8]
			},
			"svk": {
				"name": "Słowacja",
				"group": "E",
				"extra_coeff": [22]
			},
			"hun": {
				"name": "Węgry",
				"group": "F",
				"extra_coeff": [31]
			},
			"por": {
				"name": "Portugalia",
				"group": "F",
				"extra_coeff": [13]
			},
			"fra": {
				"name": "Francja",
				"group": "F",
				"extra_coeff": [7]
			},
			"ger": {
				"name": "Niemcy",
				"group": "F",
				"extra_coeff": [4]
			}
		},
		"group_algorithm": [
			{
				"host": 1,
				"guest": 2
			},
			{
				"host": 3,
				"guest": 4
			},
			{
				"host": 1,
				"guest": 3
			},
			{
				"host": 2,
				"guest": 4
			},
			{
				"host": 4,
				"guest": 1
			},
			{
				"host": 2,
				"guest": 3
			}
		],
		"bracket_algorithm": [
			{
				"host": "B1",
				"guest": "3"
			},
			{
				"host": "A1",
				"guest": "C2"
			},
			{
				"host": "F1",
				"guest": "3"
			},
			{
				"host": "D2",
				"guest": "E2"
			},
			{
				"host": "E1",
				"guest": "3"
			},
			{
				"host": "D1",
				"guest": "F2"
			},
			{
				"host": "C1",
				"guest": "3"
			},
			{
				"host": "A2",
				"guest": "B2"
			}
		]
	},
########################################
# Mundial Rosja 2018
########################################
	"mundial2018": {
		"regex": r"mundial ?(20)?18",
		"win_pts": 3,
		"draw_pts": 1,
		"playoffs": False,
		"third_place_qual": False,
		"third_place_match": True,
		"teams": {
			"rus": {
				"name": "Rosja",
				"group": "A",
				"extra_coeff": [70]
			},
			"ksa": {
				"name": "Arabia Saudyjska",
				"group": "A",
				"extra_coeff": [67]
			},
			"egy": {
				"name": "Egipt",
				"group": "A",
				"extra_coeff": [45]
			},
			"uru": {
				"name": "Urugwaj",
				"group": "A",
				"extra_coeff": [14]
			},
			"por": {
				"name": "Portugalia",
				"group": "B",
				"extra_coeff": [4]
			},
			"esp": {
				"name": "Hiszpania",
				"group": "B",
				"extra_coeff": [10]
			},
			"mar": {
				"name": "Maroko",
				"group": "B",
				"extra_coeff": [41]
			},
			"irn": {
				"name": "Iran",
				"group": "B",
				"extra_coeff": [37]
			},
			"fra": {
				"name": "Francja",
				"group": "C",
				"extra_coeff": [7]
			},
			"aus": {
				"name": "Australia",
				"group": "C",
				"extra_coeff": [36]
			},
			"per": {
				"name": "Peru",
				"group": "C",
				"extra_coeff": [11]
			},
			"den": {
				"name": "Dania",
				"group": "C",
				"extra_coeff": [12]
			},
			"arg": {
				"name": "Argentyna",
				"group": "D",
				"extra_coeff": [5]
			},
			"isl": {
				"name": "Islandia",
				"group": "D",
				"extra_coeff": [22]
			},
			"cro": {
				"name": "Chorwacja",
				"group": "D",
				"extra_coeff": [20]
			},
			"nig": {
				"name": "Nigeria",
				"group": "D",
				"extra_coeff": [48]
			},
			"bra": {
				"name": "Brazylia",
				"group": "E",
				"extra_coeff": [2]
			},
			"sui": {
				"name": "Szwajcaria",
				"group": "E",
				"extra_coeff": [6]
			},
			"crc": {
				"name": "Kostaryka",
				"group": "E",
				"extra_coeff": [23]
			},
			"srb": {
				"name": "Serbia",
				"group": "E",
				"extra_coeff": [34]
			},
			"ger": {
				"name": "Niemcy",
				"group": "F",
				"extra_coeff": [1]
			},
			"mex": {
				"name": "Meksyk",
				"group": "F",
				"extra_coeff": [15]
			},
			"swe": {
				"name": "Szwecja",
				"group": "F",
				"extra_coeff": [24]
			},
			"kor": {
				"name": "Korea Południowa",
				"group": "F",
				"extra_coeff": [57]
			},
			"bel": {
				"name": "Belgia",
				"group": "G",
				"extra_coeff": [3]
			},
			"pan": {
				"name": "Panama",
				"group": "G",
				"extra_coeff": [55]
			},
			"tun": {
				"name": "Tunezja",
				"group": "G",
				"extra_coeff": [21]
			},
			"eng": {
				"name": "Anglia",
				"group": "G",
				"extra_coeff": [12]
			},
			"pol": {
				"name": "Polska",
				"group": "H",
				"extra_coeff": [8]
			},
			"sen": {
				"name": "Senegal",
				"group": "H",
				"extra_coeff": [27]
			},
			"col": {
				"name": "Kolumbia",
				"group": "H",
				"extra_coeff": [16]
			},
			"jap": {
				"name": "Japonia",
				"group": "H",
				"extra_coeff": [61]
			}
		},
		"group_algorithm": [
			{
				"host": 1,
				"guest": 2
			},
			{
				"host": 3,
				"guest": 4
			},
			{
				"host": 1,
				"guest": 3
			},
			{
				"host": 4,
				"guest": 2
			},
			{
				"host": 4,
				"guest": 1
			},
			{
				"host": 2,
				"guest": 3
			}
		],
		"bracket_algorithm": [
			{
				"host": "A1",
				"guest": "B2"
			},
			{
				"host": "C1",
				"guest": "D2"
			},
			{
				"host": "E1",
				"guest": "F2"
			},
			{
				"host": "G1",
				"guest": "H2"
			},
			{
				"host": "B1",
				"guest": "A2"
			},
			{
				"host": "D1",
				"guest": "C2"
			},
			{
				"host": "F1",
				"guest": "E2"
			},
			{
				"host": "H1",
				"guest": "G2"
			}
		]
	},
########################################
# Mundial Katar 2022
########################################
	"mundial2022": {
		"regex": r"(mundial ?(20)?22|katar)",
		"win_pts": 3,
		"draw_pts": 1,
		"playoffs": False,
		"third_place_qual": False,
		"third_place_match": True,
		"teams": {
			"QAT": {
				"name": "Katar",
				"group": "A",
				"extra_coeff": [51]
			},
			"ECU": {
				"name": "Ekwador",
				"group": "A",
				"extra_coeff": [46]
			},
			"SEN": {
				"name": "Senegal",
				"group": "A",
				"extra_coeff": [20]
			},
			"NED": {
				"name": "Holandia",
				"group": "A",
				"extra_coeff": [10]
			},
			"ENG": {
				"name": "Anglia",
				"group": "B",
				"extra_coeff": [5]
			},
			"IRN": {
				"name": "Iran",
				"group": "B",
				"extra_coeff": [21]
			},
			"USA": {
				"name": "Stany Zjednoczone",
				"group": "B",
				"extra_coeff": [16]
			},
			"WAL": {
				"name": "Walia",
				"group": "B",
				"extra_coeff": [18]
			},
			"ARG": {
				"name": "Argentyna",
				"group": "C",
				"extra_coeff": [4]
			},
			"KSA": {
				"name": "Arabia Saudyjska",
				"group": "C",
				"extra_coeff": [49]
			},
			"MEX": {
				"name": "Meksyk",
				"group": "C",
				"extra_coeff": [9]
			},
			"POL": {
				"name": "Polska",
				"group": "C",
				"extra_coeff": [26]
			},
			"FRA": {
				"name": "Francja",
				"group": "D",
				"extra_coeff": [3]
			},
			"AUS": {
				"name": "Australia",
				"group": "D",
				"extra_coeff": [42]
			},
			"DEN": {
				"name": "Dania",
				"group": "D",
				"extra_coeff": [11]
			},
			"TUN": {
				"name": "Tunezja",
				"group": "D",
				"extra_coeff": [35]
			},
			"ESP": {
				"name": "Hiszpania",
				"group": "E",
				"extra_coeff": [7]
			},
			"CRC": {
				"name": "Kostaryka",
				"group": "E",
				"extra_coeff": [31]
			},
			"GER": {
				"name": "Niemcy",
				"group": "E",
				"extra_coeff": [12]
			},
			"JPN": {
				"name": "Japonia",
				"group": "E",
				"extra_coeff": [23]
			},
			"BEL": {
				"name": "Belgia",
				"group": "F",
				"extra_coeff": [2]
			},
			"CAN": {
				"name": "Kanada",
				"group": "F",
				"extra_coeff": [38]
			},
			"MAR": {
				"name": "Maroko",
				"group": "F",
				"extra_coeff": [24]
			},
			"CRO": {
				"name": "Chorwacja",
				"group": "F",
				"extra_coeff": [16]
			},
			"BRA": {
				"name": "Brazylia",
				"group": "G",
				"extra_coeff": [1]
			},
			"SRB": {
				"name": "Serbia",
				"group": "G",
				"extra_coeff": [25]
			},
			"SUI": {
				"name": "Szwajcaria",
				"group": "G",
				"extra_coeff": [14]
			},
			"CMR": {
				"name": "Kamerun",
				"group": "G",
				"extra_coeff": [37]
			},
			"POR": {
				"name": "Portugalia",
				"group": "H",
				"extra_coeff": [8]
			},
			"GHA": {
				"name": "Ghana",
				"group": "H",
				"extra_coeff": [60]
			},
			"URU": {
				"name": "Urugwaj",
				"group": "H",
				"extra_coeff": [13]
			},
			"KOR": {
				"name": "Korea Południowa",
				"group": "H",
				"extra_coeff": [29]
			}
		},
#		"teams_playoffs": [
#			{
#				"place": 2,
#				"teams": {
#					"PER": {
#						"name": "Peru",
#						"group": "D",
#						"extra_coeff": [22]
#					},
#					"UAE": {
#						"name": "Zjednoczone Emiraty Arabskie",
#						"group": "D",
#						"extra_coeff": [68]
#					},
#					"AUS": {
#						"name": "Australia",
#						"group": "D",
#						"extra_coeff": [42]
#					}
#				}
#			},
#			{
#				"place": 2,
#				"teams": {
#					"CRC": {
#						"name": "Kostaryka",
#						"group": "E",
#						"extra_coeff": [31]
#					},
#					"NZL": {
#						"name": "Nowa Zelandia",
#						"group": "E",
#						"extra_coeff": [101]
#					}
#				}
#			}
#		],
		"group_algorithm": [
			{
				"host": 1,
				"guest": 2
			},
			{
				"host": 3,
				"guest": 4
			},
			{
				"host": 1,
				"guest": 3
			},
			{
				"host": 4,
				"guest": 2
			},
			{
				"host": 4,
				"guest": 1
			},
			{
				"host": 2,
				"guest": 3
			}
		],
		"bracket_algorithm": [
			{
				"host": "A1",
				"guest": "B2"
			},
			{
				"host": "C1",
				"guest": "D2"
			},
			{
				"host": "E1",
				"guest": "F2"
			},
			{
				"host": "G1",
				"guest": "H2"
			},
			{
				"host": "B1",
				"guest": "A2"
			},
			{
				"host": "D1",
				"guest": "C2"
			},
			{
				"host": "F1",
				"guest": "E2"
			},
			{
				"host": "H1",
				"guest": "G2"
			}
		]
	}
}