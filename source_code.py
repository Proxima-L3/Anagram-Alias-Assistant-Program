# ******************************************************************************
# Author:           Proxima-L3
# Date:             April 5, 2022
# Project Name:     Anagram Alias Assistant Program (AAAP) v1.1
# Update Summary:	Added line that imports lxml. Fixed program breaking bug that
# 					caused non anagrams to appear in the anagram results shown.
# 					Other minor ui changes.
# Description:      A program that uses web scraping to make lists of names
#                   from websites and uses them to help the user create anagrams.
# Goal/purpose:     Learn how to use web scraping, practice searching for and
#                   using random libraries/modules/functions that solve a problem
#                   in my algorithm, refresh my programming skills after being
#                   away from it for over a year, create a tool that has potential
#                   use in the future,
# Sources:          (https://en.wikipedia.org/wiki/List_of_Greek_mythological_figures)
#                   (https://www.anagrammer.com/)
#                   (https://www.coolgenerator.com/anagram-name-generator)
#
#                   (https://www.askpython.com/python/string/remove-character-from-string-python)
#                   (https://www.tutorialspoint.com/python-inserting-item-in-sorted-list-maintaining-order)
#                   (https://www.w3schools.com/python/python_tuples_unpack.asp)
#                   (https://www.educative.io/edpresso/how-to-find-the-length-of-a-string-in-python)
#                   (https://www.pythonpool.com/python-check-if-string-is-integer/)
#                   (Minimal review from one of my Udemy courses)
#					(https://softwareengineering.stackexchange.com/questions/3199/what-version-naming-convention-do-you-use?newreg=986f6d522b3d47478c0bef9677b24198)
# ******************************************************************************


import requests
import bs4
import lxml
import bisect


# This function ties all other functions together to make one coherent program
def main():
	intro()
	# while loop continuously checking to see what menu_choice the user picked
	while True:
		menu_choice = main_menu()
		if menu_choice == str(1):
			url_used, list_of_names = temp_wiki_scrape_list_func()
			pre_anagram, adv_op_list = anagram_assistant()

			anagram_generator(url_used, list_of_names, pre_anagram, adv_op_list)
			return_to_menu()
		# elif statements would go here when I decide to add more menu options
		else:
			break

	print("\nThanks for using AAAP")


# function for opening title screen (aka "intro")
def intro():
	user_choice = ''

	while True:
		user_choice = input("Anagram Alias Assistant Program (AAAP)\n\n(press enter to continue)")
		if user_choice != '' or user_choice == '':
			break
		else:
			pass
	print("\033[H\033[J")


# This function displays the main menu
def main_menu():

	menu_choice = 0
	print("\033[H\033[J")
	print("1: Make an Anagram!\n2: Quit\n\n")

	while True:
		menu_choice = input("")
		if menu_choice in ['1', '2']:
			return menu_choice
		else:
			print("Invalid input. Try again.\n")


# Temporary function that will be replaced with a file call. The external file will essentially be a database of all the collected names/figures/etc that have been scraped from websites
def temp_wiki_scrape_list_func():
	url_used = "https://en.wikipedia.org/wiki/List_of_Greek_mythological_figures"

	# assigning the html page to a variable via get request
	wiki_request1 = requests.get(url_used)

	# using beautiful soup to make raw html code organized
	wiki_soup = bs4.BeautifulSoup(wiki_request1.text, 'lxml')

	# making a list of all a tags in the html document
	raw_atag_list = wiki_soup.select('a')

	keyword_gibberish_list = ['',' ','q','w','e','r','t','y','u','i','o','p','a','s','d','f','g','h','j','k','l','z','x','c','v','b','n','m',"'",'`','~','!','@','#','$','%','^','&','*','(',')','-','=','_','+','[',']','{','}','|',';',':','"',',','.','/','<','>','?']
	filtered_atag_list = []
	int_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
	has_int = False

	# for loop with several if statements that filter out the unwanted things in my code, specifically names with ints, single letters, and repeats of names
	for item in raw_atag_list:
		item = item.getText()

		for num in int_list:
			if str(num) in item:
				has_int = True
				break
			else:
				has_int = False

		if has_int:
			continue
		elif item.lower() in keyword_gibberish_list:
			continue
		elif item in filtered_atag_list:
			continue
		else:
			bisect.insort(filtered_atag_list, item)

	return url_used, filtered_atag_list


# This function is the main function used to assist the user in collecting necessary information that will be used to make their anagrammed alias
def anagram_assistant():
	print("\033[H\033[J")

	pre_anagram = ''
	adv_op_choice = ''
	adv_op_list = []
	adv_op0 = 0

	while True:
		pre_anagram = input("Enter word or phrase to be anagrammed: ")
		if pre_anagram == '':
			print("You must enter something!\n")
		else:
			break

	# while loop used to determine if user wants to use advanced options
	while True:
		adv_op_choice = input("\n\n\tAdvanced options? (y/n): ")
		if adv_op_choice.lower() == 'y':
			adv_op0 = common_letters()
			adv_op_list.append(adv_op0)
			# would enter any other future advanced options here, under this if statement
			return pre_anagram, adv_op_list
		elif adv_op_choice.lower() == 'n':
			return pre_anagram, adv_op_list
		else:
			print("Invalid input")


# This function takes in user input regarding how many letters the user entered word/phrase and the anagram should have in common... MAYBE MAKE THIS A DECORATOR FOR THE ANAGRAM ASSISTANT FUNCTION...
def common_letters():
	print("\033[H\033[J")
	while True:
		print("\t\tAdvanced Options")
		letter_amount = input("\nHow many common letters minimum should be in the anagram? (enter nothing if you want true anagrams only): ")
		if letter_amount.isdigit():
			return int(letter_amount)
		elif letter_amount == '':
			return letter_amount
		else:
			print("Invalid input\n\n")


# function that takes in the url used, the list or database of names, the pre_anagram string, and a list of variables representing the choices made by the user in the advanced options section and uses that information to generate a list of possible anagrams/aliases
def anagram_generator(url_used, list_of_names, pre_anagram, adv_op_list):

	number_of_common_letters_list = []
	perfect_anagram_list = []
	adv_op0_anagram_list = []

# This is fun! I love programming. I can't imagine how amazing it'll be to do engineering projects

	# for loop used as outer layer of nested for loop to iterate through list_of_names list and create another list that holds the number of letters that the pre_anagram and each name in list_of_names have in common. (the index location of each item in list_of_names and each item in number_of_common_letters_list should be the same... although, in the future, we may want to figure out how to use a dictionary to do this whole process)
	for name in list_of_names:

		name_for_iterating = name.replace(' ', '').lower()
		pre_anagram_for_iterating = pre_anagram.replace(' ', '').lower()
		counter1 = 0

		# nested for loop used for checking how many letters pre_anagram and the current name (from list of names) have in common
		for letter in pre_anagram_for_iterating:
			if letter in name_for_iterating:
				pre_anagram_for_iterating = pre_anagram_for_iterating.replace(letter, '', 1)
				counter1 += 1
				name_for_iterating = name_for_iterating.replace(letter, '', 1)
			else:
				pass

		# this line adds how many common letters there are into a list that will be used later to find/index names (from the list_of_names list) that meet certain guidelines to be put into another list that will be shown to the user as possible viable anagrams/aliases
		number_of_common_letters_list.append(counter1)

		# this line takes the current "name string" being iterated through, gets rid of its spaces, and compares its remaining length to the remaining length of pre_anagram. if they are the same, it adds the current name being iterated through to a perfect anagram list
		if name_for_iterating == '' and pre_anagram_for_iterating == '':
			perfect_anagram_list.append(name)
		else:
			pass

	# actual code that makes and prints the list of anagrams/aliases
	# conditional statement that checks if user wanted perfect anagrams only then prints them. If they didn't, a new list of all the names with adv_op0 number of common letters or more is created then printed (Note: there is no elif statement used to determine if adv_op0 is an int or a str because we already set up an "else invalid input filter" in the common letters function)
	if adv_op_list == [] or adv_op_list[0] == '':
		print("\033[H\033[J")
		print(f"Word/Phrase: {pre_anagram}")
		print(f"Database/url used: ({url_used})")
		print(f"\n\n\nAnagrams Found: {len(perfect_anagram_list)}\n\n")
		for item in perfect_anagram_list:
			print(item)
	else:
		index_counter = 0

		for item in number_of_common_letters_list:
			if item >= adv_op_list[0]:
				adv_op0_anagram_list.append(list_of_names[index_counter])
			else:
				pass
			index_counter += 1

		print("\033[H\033[J")
		print(f"Word/Phrase: {pre_anagram}")
		print(f"Common letters: {adv_op_list[0]}")
		print(f"Database/url used: ({url_used})")
		print(f"\n\n\nAnagrams Found: {len(adv_op0_anagram_list)}\n\n")
		for item in adv_op0_anagram_list:
			print(item)


# this function keeps the user on the same screen until they decide they want to go back to the main menu
def return_to_menu():
	user_choice = ''

	while True:
		user_choice = input("\n(Press b to return to the main menu)\n")
		if user_choice.lower() == 'b':
			break
		else:
			print("Invalid input")


main()
