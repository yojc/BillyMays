from datetime import date
from functools import cmp_to_key

from billy_birthdays_data import server_birthdays, intervals
import billy_shared as sh

def comparator(a, b):
	if a["delta"] > b["delta"]:
		return 1
	elif a["delta"] < b["delta"]:
		return -1
	elif a["name"].lower() > b["name"].lower():
		return 1
	elif a["name"].lower() < b["name"].lower():
		return -1
	else:
		return 0

def generate_birthday_date(starting_date, month, day):
	starting_year = starting_date.year
	
	if starting_date.month > month or (starting_date.month == month and starting_date.day > day):
		return date(starting_date.year+1, month, day)
	else:
		return date(starting_date.year, month, day)


def return_birthdays_periodic(checked_date=date.today()):
	sh.debug("Processing birthdays for date {}".format(checked_date.strftime("%Y/%m/%d")))
	
	ret = []
	
	for server in server_birthdays:
		sh.debug("Processing server {}".format(server["name"]))
		
		birthday_data = {
			"target_users" : server["target_users"],
			"target_channels" : server["target_channels"],
			"users" : []
		}
		
		for user in server["users"]:
			sh.debug("Processing user {}".format(user["name"]))
			
			user_date = generate_birthday_date(checked_date, user["month"], user["day"])
			
			sh.debug("Next/current birthday: {}".format(user_date.strftime("%Y/%m/%d")))
			
			date_delta = (user_date - checked_date).days
			
			sh.debug("Days delta: {}".format(date_delta))
			
			if date_delta in intervals[user["how_often"]]:
				sh.debug("Found interval, adding to notification list")
				birthday_data["users"].append({
					"name" : user["name"],
					"date" : user_date,
					"delta" : date_delta
				})
			else:
				sh.debug("Interval not found")
		
		birthday_data["users"].sort(key=cmp_to_key(comparator))

		if len(birthday_data["users"]) > 0:
			sh.debug("Found {} users matching criteria".format(len(birthday_data["users"])))
			ret.append(birthday_data)
		else:
			sh.debug("No matching users found")
	
	return ret

def check_upcoming_birthdays(target, checked_days=30, starting_date=date.today()):
	checked_server = None
	
	for server in server_birthdays:
		if (isinstance(target, int) and target in server["ids"]) or (isinstance(target, str) and target.lower() in server["name"]):
			sh.debug("Found matching server: {}/{}".format(server["name"], target))
			checked_server = server
			break
	
	if not checked_server:
		sh.debug("Server {} not found".format(target))
		return None
	
	returned_users = []
	
	for user in checked_server["users"]:
		sh.debug("Processing user {}".format(user["name"]))
		
		user_date = generate_birthday_date(starting_date, user["month"], user["day"])
		
		sh.debug("Next/current birthday: {}".format(user_date.strftime("%Y/%m/%d")))
		
		date_delta = (user_date - starting_date).days
		
		sh.debug("Days delta: {}".format(date_delta))
		
		if date_delta <= checked_days:
			sh.debug("Adding to list")
			
			returned_users.append({
				"name" : user["name"],
				"date" : user_date,
				"delta" : date_delta
			})
		else:
			sh.debug("Skipping")
	
	if len(returned_users) > 0:
		sh.debug("Found {} users; sorting array".format(len(returned_users)))
		returned_users.sort(key=cmp_to_key(comparator))
	else:
		sh.debug("No matching users found")
	
	return returned_users
