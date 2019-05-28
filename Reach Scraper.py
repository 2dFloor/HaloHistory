from bs4 import BeautifulSoup
import requests
import sys


def Reach():
	game_list = []
	player_list = []
	target_player = "" 

	def NextPage(soup):
		search = soup.find('div', attrs={'class':'disabledNext'})
		if (search is None):
			return True
		else:
			return False
	
	def GetGameList():
		print("Beginning GetGameList")
		more_pages = True
		page = 0

		# Make the name URL friendly by replacing whitespace
		name = target_player
		for char in name:
		    if char == ' ':
		        name = name.replace(' ', '%20')


		while (more_pages):
			request = requests.get("https://halo.bungie.net/stats/reach/playergamehistory.aspx?vc=0&player=" + name + "&page=" + str(page))
			soup = BeautifulSoup(request.text, 'html.parser') 
						
			for link in soup.findAll('a', attrs={'class':'overlay'}):
				game_list.append(link.get('href'))
			
			if (NextPage(soup)):
				page += 1
			else:
				more_pages = False


	def GetPlayerList():
		print("Beginning GetPlayerList")
		for game_link in game_list:
			request = requests.get("https://halo.bungie.net" + game_link)
			soup = BeautifulSoup(request.text, 'html.parser') 
			for player_link in soup.select(".playerInfo > p > strong > a"):
				player_list.append(player_link.get_text())	


	def SortPlayer():
		print("Beginning SortPlayer")
		abc = []
		xyz = []
		player_current = ""
		player_count = 0

		player_list.sort()
		
		for a in player_list:
			if a not in abc:
				abc.append(a)
				abc.append(player_list.count(a))

		# Put list into tuples 
		t = 0
		cba = []
		while t < len(abc):
			cba.append((abc[t], abc[t+1]))
			t+=2

		# Sort tuple list for writing, descending
		cba.sort(key=lambda tup: tup[1], reverse=True)

		# Write to file 
		try:
			file = open(target_player + " Reach.txt", "w")
			cntr = 0

			while cntr < len(cba):
				if cba[cntr][1] > 9:
					file.write("Name: {:-<20}Occurrences: {}\n".format(str(cba[cntr][0]), str(cba[cntr][1])))
				cntr+=1
			file.close()

		except Exception as e:
			print(e)
			file.close()
		
	GetGameList()
	GetPlayerList()
	SortPlayer()

Reach()