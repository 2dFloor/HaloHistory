from bs4 import BeautifulSoup
import requests
import sys

def Halo3():
	games_list = []
	players_list = []
	target_name = ""

	def GetMatchmakingHistory():
		print("Beginning GetMatchmakingHistory")
		more_pages = True
		page = 1

		# Make the name URL friendly by replacing whitespace
		name = target_name
		for char in name:
		    if char == ' ':
		        name = name.replace(' ', '%20')

		while (more_pages):   
			request = requests.get("https://halo.bungie.net/stats/playerstatshalo3.aspx?player=" + name + "&ctl00_mainContent_bnetpgl_recentgamesChangePage=" + str(page))
			soup = BeautifulSoup(request.text, 'html.parser') 
						
			for link in soup.select("tbody > tr > td > a"):
				games_list.append(link.get('href'))
			
			if soup.find('a', attrs={'title':'Next Page'}).get('href') != None:
				page += 1
			else:
				more_pages = False
			
		# Old ass site that uses outdated code, the games list has a lot of shit that needs removal 
		for ele in games_list:
			if "javascript" in ele:
				games_list.remove(ele)


	def GetCustomGameHistory():
		print("Beginning GetCustomGameHistory")
		more_pages = True
		page = 1

		# Make the name URL friendly by replacing whitespace
		name = target_name
		for char in name:
		    if char == ' ':
		        name = name.replace(' ', '%20')

		while (more_pages):   
			request = requests.get("https://halo.bungie.net/stats/playerstatshalo3.aspx?player=" + name + "&cus=1" + "&ctl00_mainContent_bnetpgl_recentgamesChangePage=" + str(page))
			soup = BeautifulSoup(request.text, 'html.parser') 
						
			for link in soup.select("tbody > tr > td > a"):
				games_list.append(link.get('href'))
			
			if soup.find('a', attrs={'title':'Next Page'}).get('href') != None:
				page += 1
			else:
				more_pages = False
			
		# Old ass site that uses outdated code, the games list has a lot of shit that needs removal 
		for ele in games_list:
			if "javascript" in ele:
				games_list.remove(ele)


	def GetPlayerList():
		print("Beginning GetPlayerList")
		for game_link in games_list:
			request = requests.get("https://halo.bungie.net" + game_link)
			soup = BeautifulSoup(request.text, 'html.parser') 
			for player_name in soup.select(".name > a"):
				players_list.append(player_name.get_text())


	def SortPlayer():
		print("Beginning SortPlayer")
		non_repeating_names = []
		occurrences = []
		tuple_list = []

		# Create list on non-repeating names 
		for name in players_list:
			if name not in non_repeating_names:
				non_repeating_names.append(name)
		# Alphabetically sort the non-repeating list so it 
		# lines up with the number of occurrences properly 
		non_repeating_names.sort()
		# Count the number of occurrences with the unique list
		for name in non_repeating_names:
			occurrences.append(players_list.count(name))
		# Combine the two lists into one of tuples 
		c = 0
		while c < len(non_repeating_names):
			tuple_list.append((non_repeating_names[c], occurrences[c]))
			c+=1
		# Finally sort the tuples list by most occurring, then format and write
		tuple_list.sort(key=lambda tup: tup[1], reverse=True)
		# Write to file 
		try:
			file = open(target_name + " Halo3.txt", "w")
			cntr = 0

			while cntr < len(tuple_list):
				if tuple_list[cntr][1] > 9:
					file.write("Name: {:-<20}Occurrences: {}\n".format(str(tuple_list[cntr][0]), str(tuple_list[cntr][1])))
				cntr+=1
			file.close()

		except Exception as e:
			print(e)
			file.close()	


	GetMatchmakingHistory()
	GetCustomGameHistory()
	GetPlayerList()
	SortPlayer()
Halo3()