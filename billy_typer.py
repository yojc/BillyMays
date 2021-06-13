import random
import re
from functools import cmp_to_key

from billy_typer_data import cups
import billy_shared as sh

WINNER_BOLD = False

# Internal stuff

current_cup = None
current_group = None

def group_sorter_comparator(a, b):
	to_compare = ["Pts", "GD", "GF", "W"]

	for stat in to_compare:
		if current_group[a][stat] > current_group[b][stat]:
			return -1
		elif current_group[a][stat] < current_group[b][stat]:
			return 1
	
	current_cup_teams = cups[current_cup]["teams"]
	extra_coeff_count = min(len(current_cup_teams[a]["extra_coeff"]), len(current_cup_teams[b]["extra_coeff"]))

	for i in range(0, extra_coeff_count):
		if current_cup_teams[a]["extra_coeff"][i] > current_cup_teams[b]["extra_coeff"][i]:
			return -1
		elif current_cup_teams[a]["extra_coeff"][i] < current_cup_teams[b]["extra_coeff"][i]:
			return 1
	
	return 0

def generate_goals_count(knockout=False, overtime=False):
	odd_modifier = 1

	if knockout:
		odd_modifier *= 1.25
	
	if overtime:
		odd_modifier /= 3

	odds = {
		"10": 0.0003,
		"9": 0.0005,
		"8": 0.001,
		"7": 0.003,
		"6": 0.005,
		"5": 0.01,
		"4": 0.05,
		"3": 0.1,
		"2": 0.2,
		"1": 0.4
	}

	for i in odds:
		if random.random() < odds[i] * odd_modifier:
			return int(i)
	
	return 0

def generate_penalty_count():
	penalty_odd = 0.95
	penalty_round = 0
	result = [0, 0]

	while True:
		if random.random() < penalty_odd:
			result[0] += 1
		if random.random() < penalty_odd:
			result[1] += 1
		
		if penalty_round > 1 and result[0] != result[1]:
			break
		else:
			penalty_round += 1
			penalty_odd -= 0.05
	
	return result

def generate_match_result(host, guest, overtime=False, penalties=True, knockout=False):
	was_overtime = False
	penalties_result = False

	sh.debug("Playing {} vs. {}...".format(host, guest))

	def decide_winner(h, g):
		if h > g:
			result["winner"] = host
			result["loser"] = guest
		elif h < g:
			result["winner"] = guest
			result["loser"] = host
	
	def format_name(name, full=False):
		if full:
			return_name = cups[current_cup]["teams"][name]["name"]
		else:
			return_name = name.upper()

		if WINNER_BOLD and result["winner"] == name:
			return "**{}**".format(return_name)
		else:
			return return_name
	
	def generate_strings(host, guest, result_host_ft, result_guest_ft, result_host_aet=None, result_guest_aet=None, result_host_penalties=None, result_guest_penalties=None, full=False):
		if not was_overtime:
			result_host_first = result_host_ft
			result_guest_first = result_guest_ft
		else:
			result_host_first = result_host_aet
			result_guest_first = result_guest_aet
		
		base = "{} {} : {} {}".format(format_name(host, full), result_host_first, result_guest_first, format_name(guest, full))

		if was_overtime:
			base += " (FT {} : {})".format(result_host_ft, result_guest_ft)

		if penalties_result:
			base += " (k. {} : {})".format(result_host_penalties, result_guest_penalties)
		
		return base

	result = {
		"winner": None,
		"loser": None,
		"goals_host": generate_goals_count(knockout=knockout),
		"goals_guest": generate_goals_count(knockout=knockout),
		"goals_overtime_host": None,
		"goals_overtime_guest": None,
		"goals_penalty_host": None,
		"goals_penalty_guest": None,
		"string": None,
		"string_full": None
	}

	decide_winner(result["goals_host"], result["goals_guest"])

	sh.debug("Generating overtime result")

	if overtime and not result["winner"]:
		was_overtime = True
		result["goals_overtime_host"] = result["goals_host"] + generate_goals_count(overtime=True, knockout=knockout)
		result["goals_overtime_guest"] = result["goals_guest"] + generate_goals_count(overtime=True, knockout=knockout)
		decide_winner(result["goals_overtime_host"], result["goals_overtime_guest"])

	sh.debug("Generating penalty result")
	
	if penalties and was_overtime and result["goals_overtime_host"] == result["goals_overtime_guest"]:
		penalties_result = generate_penalty_count()
		result["goals_penalty_host"] = penalties_result[0]
		result["goals_penalty_guest"] = penalties_result[1]
		decide_winner(result["goals_penalty_host"], result["goals_penalty_guest"])

	sh.debug("Generating output string")

	result["string"] = generate_strings(host, guest, result["goals_host"], result["goals_guest"], result["goals_overtime_host"], result["goals_overtime_guest"], result["goals_penalty_host"], result["goals_penalty_guest"])
	result["string_full"] = generate_strings(host, guest, result["goals_host"], result["goals_guest"], result["goals_overtime_host"], result["goals_overtime_guest"], result["goals_penalty_host"], result["goals_penalty_guest"], full=True)

	return result

def generate_groups():
	global groups
	global matches

	groups = {}
	matches = {}
	matches["group"] = {}

	for team_id in cups[current_cup]["teams"]:
		team = cups[current_cup]["teams"][team_id]
		sh.debug("Processing team: " + team["name"])

		if team["group"] not in groups:
			sh.debug("Creating group: " + team["group"])
			groups[team["group"]] = {}
			matches["group"][team["group"]] = []
		
		stats = {
			"Pld": 0,
			"W": 0,
			"D": 0,
			"L": 0,
			"GF": 0,
			"GA": 0,
			"GD": 0,
			"Pts": 0
		}
		
		groups[team["group"]][team_id] = stats

def generate_group_matches():
	global current_group
	global groups
	global matches

	for group_id in groups:
		group_team_ids = []
		group = groups[group_id]
		current_group = groups[group_id]

		sh.debug("Generating matches order for group " + group_id)
		for team_id in group:
			group_team_ids.append(team_id)
		
		sh.debug("Generating matches for group " + group_id)
		for match in cups[current_cup]["group_algorithm"]:
			host_id = group_team_ids[match["host"]-1]
			guest_id = group_team_ids[match["guest"]-1]

			result = generate_match_result(host_id, guest_id)

			if result["winner"] and result["loser"]:
				group[result["winner"]]["W"] += 1
				group[result["loser"]]["L"] += 1
			else:
				group[host_id]["D"] += 1
				group[guest_id]["D"] += 1
			
			group[host_id]["Pld"] += 1
			group[host_id]["GF"] += result["goals_host"]
			group[host_id]["GA"] -= result["goals_guest"]

			group[guest_id]["Pld"] += 1
			group[guest_id]["GF"] += result["goals_guest"]
			group[guest_id]["GA"] -= result["goals_host"]

			matches["group"][group_id].append(result["string"] + "\n")
		
		sh.debug("Updating stats for group " + group_id)
		for team_id in group:
			group[team_id]["GD"] = group[team_id]["GF"] + group[team_id]["GA"]
			group[team_id]["Pts"] = group[team_id]["W"] * cups[current_cup]["win_pts"] +  group[team_id]["D"] * cups[current_cup]["draw_pts"]
		
		sh.debug("Sorting group " + group_id)
		group_team_ids.sort(key=cmp_to_key(group_sorter_comparator))
		groups[group_id] = {k: v for k, v in sorted(group.items(), key=lambda item: group_team_ids.index(item[0]))}

def generate_third_places():
	global current_group
	global groups

	groups["3rd"] = {}
	group_team_ids = []
	current_group = groups["3rd"]

	for group_id in groups:
		group = groups[group_id]
		group_teams = list(group.items())
		team_id = group_teams[2][0]
		group_team_ids.append(team_id)
		groups["3rd"][team_id] = group_teams[2][1]
	
	group_team_ids.sort(key=cmp_to_key(group_sorter_comparator))
	groups["3rd"] = {k: v for k, v in sorted(group.items(), key=lambda item: group_team_ids.index(item[0]))}

def generate_knockout_teams():
	global cups
	global groups
	global knockout

	knockout = []

	third_teams = groups["3rd"].copy()

	def get_team(code):
		if code == "3":
			team_id = next(iter(third_teams))
			third_teams.pop(team_id)
			return team_id
		else:
			group_id = code[0]
			team_id = int(code[1])-1
			return list(groups[group_id].items())[team_id][0]

	for match in cups[current_cup]["bracket_algorithm"]:
		host = get_team(match["host"])
		guest = get_team(match["guest"])

		knockout.append({
			"host": host,
			"guest": guest
		})

def generate_knockout():
	global cups
	global knockout
	global matches

	matches["knockout"] = {}

	while len(knockout) > 0:
		round_name = str(len(knockout))
		sh.debug("Playing knockout stage 1/{}".format(str(len(knockout))))
		next_step = []
		next_host = True

		matches["knockout"][round_name] = []

		for match in knockout:
			result = generate_match_result(match["host"], match["guest"], knockout=True, overtime=True)
			matches["knockout"][round_name].append(result["string"])

			if (round_name != "1"):
				if next_host:
					next_host = False
					next_step.append({
						"host": result["winner"],
						"guest": None
					})
				else:
					next_host = True
					next_step[-1]["guest"] = result["winner"]
			else:
				matches["final"] = result["string_full"]
		
		knockout = next_step

# Output

def output_group(group):
	global groups

	if group != "3rd":
		ret = "Grupa " + group + ":\n"
	else:
		ret = "Ranking trzecich drużyn:\n"

	ret += "```Pld   W   D   L  GF  GA  GD Pts\n"
	for team_id in groups[group]:
		for stat in groups[group][team_id]:
			ret += str(groups[group][team_id][stat]).rjust(3, " ") + " "
		
		ret += cups[current_cup]["teams"][team_id]["name"] + "\n"
	
	return ret[:-1] + "```"

def output_group_matches(group):
	global matches

	ret = ""

	for match in matches["group"][group]:
		ret += "`" + match[:-1] + "`\n"

	return ret

def output_knockout_matches():
	global matches

	ret = ""

	for step in matches["knockout"]:
		if step == "1":
			ret += "\nFINAŁ:\n"
		elif step == "2":
			ret += "\nPółfinały:\n"
		elif step == "4":
			ret += "\nĆwierćfinały:\n"
		else:
			ret += "\nFaza 1/{}:\n".format(step)
		
		for match in matches["knockout"][step]:
			ret += "`" + match + "`\n"

	return ret[:-1]

# Public

def generate_cup(given_cup):
	global cups
	global current_cup

	current_cup = None

	for cup in cups:
		if re.match(cups[cup]["regex"], given_cup, re.IGNORECASE):
			current_cup = cup
	
	if not current_cup:
		return "Nie znaleziono podanych rozgrywek."
	
	generate_groups()
	generate_group_matches()
	generate_third_places()
	generate_knockout_teams()
	generate_knockout()

def output_cup():
	ret = {
		"group": "",
		"knockout": None,
		"final": None,
	}

	for group_id in groups:
		if group_id == "3rd":
			continue
		
		ret["group"] += output_group(group_id) + "\n"
		ret["group"] += output_group_matches(group_id) + "\n"
	
	ret["knockout"] = output_group("3rd")
	ret["knockout"] += output_knockout_matches()

	ret["final"] = matches["final"]

	return ret
