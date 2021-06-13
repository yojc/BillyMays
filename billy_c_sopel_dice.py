# coding=utf-8
"""
dice.py - Dice Module
Copyright 2010-2012, Dimitri "Tyrope" Molenaars, TyRope.nl
Licensed under the Eiffel Forum License 2.
More info:
 * Jenni: https://github.com/myano/jenni/
 * Phenny: http://inamidst.com/phenny/
"""

import random
import re

import billy_shared as sh
import asyncio


async def c_dice(client, message):
	""".dice <formula> - Rolls dice using the XdY format, also does basic (+-*/) math."""
	#MATHTIME! Let's prepare the failsafes.
	legal_formula, no_dice = 1, 1
	#parsing time.
	msg = sh.get_args(message)
	formula = msg #back-up the original message, because you're going to feed it back to the user in the end.
	formula = formula.replace("-", " - ")
	formula = formula.replace("+", " + ") #add spaces
	formula = formula.replace("/", " / ") #for all
	formula = formula.replace("*", " * ") #the characters
	formula = formula.replace("(", " ( ") #supported
	formula = formula. replace(")", " ) ")
	arr = formula.split(" ") #aaaand, CUT IT APART! (this is why you needed the spaces.)
	full_string = "" #reset the formula
	for segment in arr:
		#let's look at this formula... piece, by, piece
		if segment != "":
			#the value of this segment is 0
			value = 0
			if re.search("[0-9]*(d|D|k|K)[0-9]+", segment): #if there's a dice (regex FTW!)
				value = rollDice(segment.lower()) #then roll the dice.
				no_dice = 0 # And let the bot know there's dice in the formula
			elif re.search("([0-9]|\+|\-|\*|\/|\(|\)| \+| \-| \*| \/| \(| \))", segment): #are any of the supported math characters in this piece?
				value = segment #then just make that the value.
			else:
				legal_formula = 0 #non-supported character found...
				break #ABORT, ABORT, ABORT!
			full_string += value #add this segment's value to the full string
	#repeat next segment
	#you done? good.
	if legal_formula == 1 and full_string != "": # did something break? no? good, continue.
		#at this point full string is something like: "4 + 6 + 12 * 4" etc.
		result = str(eval(full_string)) # so normally eval is UNSAFE... but since i've dumped regex over the user input i'm pretty confident in the security.
		#print result to chat
		if(no_dice): #no dice found, warn!
			await message.reply(msg+" = "+result)
		else: #dice found, just let the users know what's happening
			await message.reply("Wyrzucono "+msg+" ("+full_string+"): "+result)
#	else: #print illegal warning.
#		await message.reply("Coś tu jest nie teges: "+segment)

c_dice.command = r"(d|dice|roll|rzut|rzuc)"
c_dice.params = ["XdY / XkY"]
c_dice.desc = "Rzut kością"

def rollDice(diceroll):
#Time for the real fun, dice!
	if "k" in diceroll.lower():
		delimiter = "k"
	else:
		delimiter = "d"
	
	if(diceroll.lower().startswith(delimiter)): #check if it's XdX or dX
		#  dX
		rolls = 1 #no dice amounts specified, roll 1
		size = int(diceroll[1:]) # dice with this amount of sides
	else:
		# XdX
		rolls = int(diceroll.lower().split(delimiter)[0]) # dice amount specified, use it.
		size = int(diceroll.lower().split(delimiter)[1]) #  aswell as this size.
	result = "" #dice result is zero.
	for i in range(1,rolls+1): #for the amount of dice
		#roll 10 dice, pick a random dice to use, add string to result.
		# I should elaborate on this...
		# str() makes sure the number is in string format (required for the eval())
		# random.randint(1,size) is 1 dice and random.randint(0,9) selects one of the ten dice rolled
		# reason for this is fairness, true random has at least 2 stages.
		result += str((random.randint(1,size),random.randint(1,size),random.randint(1,size),random.randint(1,size),random.randint(1,size),random.randint(1,size),random.randint(1,size),random.randint(1,size),random.randint(1,size),random.randint(1,size))[random.randint(0,9)])
		if(i != rolls):
			#if it's not the last sign, add a plus sign.
			result += "+"
	return "("+result+")" #feed it back to the formula parser... add some parentheses so we know this is 1 roll.