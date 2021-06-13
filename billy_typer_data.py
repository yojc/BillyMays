cups = {
	"euro2021": {
		"regex": r"euro ?202[01]",
		"win_pts": 3,
		"draw_pts": 1,
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
	}
}