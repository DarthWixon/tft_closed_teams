
import numpy as np
import itertools
import time

def OriginTester(origin_array):
	are_origins_met = origin_array >= min_origin_array
	are_origins_empty = origin_array == 0
	are_origins_closed = np.all(are_origins_met + are_origins_empty)
	return are_origins_closed

def RoleTester(role_array):
	are_roles_met = role_array >= min_role_array
	are_roles_empty = role_array == 0
	are_roles_closed = np.all(are_roles_met + are_roles_empty)
	return are_roles_closed

def TeamTester(origin_array, role_array):
	is_origin_closed = OriginTester(origin_array)
	is_role_closed = RoleTester(role_array)
	is_team_closed = is_origin_closed and is_role_closed
	return is_team_closed

def LuxChecker(team):
	n_luxes = 0
	for unit in team:
		if unit.is_lux:
			n_luxes += 1
		if n_luxes > 1:
			return False
	return True

def QiyanaChecker(team):
	n_qiyanas = 0
	for unit in team:
		if unit.is_qiyana:
			n_qiyanas += 1
		if n_qiyanas > 1:
			return False
	return True

def FindingClosedTeams(max_units):
	teams_found = 0
	valid_teams = 0
	for n_units in range(1, max_units+1):
		squad = Team()

		for combination in itertools.combinations(unit_list, n_units):
			passed_lux_check = LuxChecker(combination)
			passed_qiyana_check = QiyanaChecker(combination)
			if passed_lux_check:
				if passed_qiyana_check:
					valid_teams += 1
					for unit in combination:
						# print unit.name
						squad.AddUnit(unit)
					closed = squad.MachineReport()
					# print closed
					if closed:
						squad.PrintReport()
						teams_found += 1

			squad.WipeTeam()

	print('Teams Found: {}'.format(teams_found))
	print('This is {}% of the total possible ({}) teams of size up to {}.'.format(np.around(teams_found/valid_teams*100, 3), valid_teams, max_units))

class Team:
	def __init__(self):
		self.n_units = 0
		self.origin_array = np.zeros(len(origin_dict))
		self.role_array = np.zeros(len(role_dict))
		self.team_members = []
		self.has_lux = False
		self.has_qiyana = False
		self.is_closed = False

	def AddUnit(self, unit):
		if self.n_units > max_units:
			pass
		elif unit.name in self.team_members:
			pass
		elif self.has_lux and unit.role_array[role_dict['avatar']] == 1:
			pass
		elif self.has_qiyana and unit.name in ['Cloud Qiyana', 'Inferno Qiyana', 'Ocean Qiyana', 'Mountain Qiyana']:
			pass
		else:
			self.n_units += 1
			self.origin_array += unit.origin_array
			self.role_array += unit.role_array
			self.team_members.append(unit.name)
			if unit.name in ['Cloud Qiyana', 'Inferno Qiyana', 'Ocean Qiyana', 'Mountain Qiyana']:
				self.has_qiyana = True
			if unit.role_array[role_dict['avatar']] == 1:
				self.has_lux = True

	def TestTeam(self):
		self.is_closed = TeamTester(self.origin_array, self.role_array)

	def PrintReport(self):
		self.TestTeam()
		print('This is a closed team of size {}: {}'.format(self.n_units, ", ".join(str(i) for i in self.team_members)))

	def MachineReport(self):
		self.is_closed = TeamTester(self.origin_array, self.role_array)
		return self.is_closed

	def WipeTeam(self):
		self.n_units = 0
		self.origin_array = np.zeros(len(origin_dict))
		self.role_array = np.zeros(len(role_dict))
		self.team_members = []
		self.has_lux = False
		self.has_qiyana = False

class Unit:
	# need to think about how to make this work better for assigning roles and units
	def __init__(self, name, origin_list, role_list):
		self.name = name
		self.origin_array = np.zeros(len(origin_dict))
		self.role_array = np.zeros(len(role_dict))
		self.is_lux = False
		self.is_qiyana = False

		if 'avatar' in role_list:
			self.is_lux = True
			self.role_array[role_dict['avatar']] += 1
			for origin in origin_list:
				self.origin_array[origin_dict[origin]] += 2 
		else:		
			for role in role_list:
				self.role_array[role_dict[role]] += 1
			for origin in origin_list:
				self.origin_array[origin_dict[origin]] += 1
		if self.name in ['Cloud Qiyana', 'Inferno Qiyana', 'Ocean Qiyana', 'Mountain Qiyana']:
			self.is_qiyana = True	

origin_dict = {
	'cloud': 0,
	'crystal': 1,
	'desert': 2,
	'electric': 3,
	'glacial': 4,
	'inferno': 5,
	'light': 6,
	'mountain': 7,
	'ocean': 8,
	'poison': 9,
	'shadow': 10,
	'steel': 11,
	'woodland': 12,
	'lunar': 13
}

role_dict = {
	'alchemist': 0,
	'assassin': 1,
	'avatar': 2,
	'beserker': 3,
	'blademaster': 4,
	'druid': 5,
	'mage': 6,
	'mystic': 7,
	'predator': 8,
	'ranger': 9,
	'summoner': 10,
	'warden': 11,
	'soulbound': 12
}

# these arrays specific the minimum number of units needed for the particular
# origin or role to be satsified, order is the same as the dictionaries above
# taken from the RockPaperShotgun list at https://www.rockpapershotgun.com/2019/12/16/tft-set-2-origins-and-classes-9-24/
# I added lunar manually later when I realised I'd forgotton it
min_origin_array = np.array([2, 2, 2, 2, 2, 3, 3, 2, 2, 3, 3, 2, 3, 2])
min_role_array = np.array([1, 3, 1, 3, 2, 2, 3, 2, 3, 2, 3, 2, 2])

aatrox = Unit('Aatrox', ['light'], ['blademaster'])
amumu = Unit('Amumu', ['inferno'], ['warden'])
annie = Unit('Annie', ['inferno'], ['summoner'])
ashe = Unit('Ashe', ['crystal'], ['ranger'])
azir = Unit('Azir', ['desert'], ['summoner'])
brand = Unit('Brand', ['inferno'], ['mage'])
braum = Unit('Braum', ['glacial'], ['warden'])
diana = Unit('Diana', ['inferno'], ['assassin'])
dr_mundo = Unit('Dr. Mundo', ['poison'], ['beserker'])
ezreal = Unit('Ezreal', ['glacial'], ['ranger'])
ivern = Unit('Ivern', ['woodland'], ['druid'])
janna = Unit('Janna', ['cloud'], ['mystic'])
jax = Unit('Jax', ['light'], ['beserker'])
karma = Unit('Karma', ['lunar'], ['mystic'])
khazix = Unit("Kha'zix", ['desert'], ['assassin'])
kindred = Unit('Kindred', ['shadow', 'inferno'], ['ranger'])
kogmaw = Unit("Kog'Maw", ['poison'], ['predator'])
leblanc = Unit('LeBlanc', ['woodland'], ['mage', 'assassin'])
leona = Unit('Leona', ['lunar'], ['warden'])
lucian = Unit('Lucian', ['light'], ['soulbound'])
lux_cloud = Unit('Cloud Lux', ['cloud'], ['avatar'])
lux_crystal = Unit('Crystal Lux', ['crystal'], ['avatar'])
lux_electric = Unit('Electric Lux', ['electric'], ['avatar'])
lux_glacial = Unit('Glacial Lux', ['glacial'], ['avatar'])
lux_inferno = Unit('Inferno Lux', ['inferno'], ['avatar'])
lux_light = Unit('Light Lux', ['light'], ['avatar'])
lux_ocean = Unit('Ocean Lux', ['ocean'], ['avatar'])
lux_shadow = Unit('Shadow Lux', ['shadow'], ['avatar'])
lux_steel = Unit('Steel Lux', ['steel'], ['avatar'])
lux_woodland = Unit('Woodland Lux', ['woodland'], ['avatar'])
malphite = Unit('Malphite', ['mountain'], ['warden'])
malzahar = Unit('Malzahar', ['shadow'], ['summoner'])
maokai = Unit('Maokai', ['woodland'], ['druid'])
master_yi = Unit('Master Yi', ['shadow'], ['mystic', 'blademaster'])
nami = Unit('Nami', ['ocean'], ['mystic'])
nasus = Unit('Nasus', ['light'], ['warden'])
nautilus = Unit('Nautilus', ['ocean'], ['warden'])
neeko = Unit('Neeko', ['woodland'], ['druid'])
nocturne = Unit('Nocturne', ['steel'], ['assassin'])
olaf = Unit('Olaf', ['glacial'], ['beserker'])
ornn = Unit('Ornn', ['electric'], ['warden'])
qiyana_cloud = Unit('Cloud Qiyana', ['cloud'], ['assassin'])
qiyana_inferno = Unit('Inferno Qiyana', ['inferno'], ['assassin'])
qiyana_mountain = Unit('Mountain Qiyana', ['mountain'], ['assassin'])
qiyana_ocean = Unit('Ocean Qiyana', ['ocean'], ['assassin'])
reksai = Unit("Rek'Sai", ['steel'], ['predator'])
renekton = Unit('Renekton', ['desert'], ['beserker'])
senna = Unit('Senna', ['shadow'], ['soulbound'])
singed = Unit('Singed', ['poison'], ['alchemist'])
sion = Unit('Sion', ['shadow'], ['beserker'])
sivir = Unit('Sivir', ['desert'], ['blademaster'])
skarner = Unit('Skarner', ['crystal'], ['predator'])
soraka = Unit('Soraka', ['light'], ['mystic'])
syndra = Unit('Syndra', ['ocean'], ['mage'])
taliyah = Unit('Taliyah', ['mountain'], ['mage'])
taric = Unit('Taric', ['crystal'], ['warden'])
thresh = Unit('Thresh', ['ocean'], ['warden'])
twitch = Unit('Twitch', ['poison'], ['ranger'])
varus = Unit('Varus', ['inferno'], ['ranger'])
vayne = Unit('Vayne', ['light'], ['ranger'])
veigar = Unit('Veigar', ['shadow'], ['mage'])
vladimir = Unit('Vladimir', ['ocean'], ['mage'])
volibear = Unit('Volibear', ['electric', 'glacial'], ['beserker'])
warwick = Unit('Warwick', ['glacial'], ['predator'])
yasuo = Unit('Yasuo', ['cloud'], ['blademaster'])
yorick = Unit('Yasuo', ['light'], ['summoner'])
zed = Unit('Zed', ['electric'], ['assassin', 'summoner'])
zyra = Unit('Zyra', ['inferno'], ['summoner'])

unit_list = [aatrox, amumu, annie, ashe, azir, brand, braum, diana, dr_mundo, ezreal, ivern, janna, jax, karma, khazix, kindred, kogmaw, leblanc, leona, lucian, lux_cloud, lux_crystal, lux_electric, lux_glacial, lux_inferno, lux_light, lux_ocean, lux_shadow, lux_steel, lux_woodland, malphite, malzahar, maokai, master_yi, nami, nasus, nautilus, neeko, nocturne, olaf, ornn, qiyana_cloud, qiyana_inferno, qiyana_mountain, qiyana_ocean, reksai, renekton, senna, singed, sion, sivir, skarner, soraka, syndra, taliyah, taric, thresh, twitch, varus, vayne, veigar, vladimir, volibear, warwick, yasuo, yorick, zed, zyra]
unit_list_no_weirdness = [aatrox, amumu, annie, ashe, azir, brand, braum, diana, dr_mundo, ezreal, ivern, janna, jax, karma, khazix, kindred, kogmaw, leblanc, leona, lucian, malphite, malzahar, maokai, master_yi, nami, nasus, nautilus, neeko, nocturne, olaf, ornn, qiyana_cloud, reksai, renekton, senna, singed, sion, sivir, skarner, soraka, syndra, taliyah, taric, thresh, twitch, varus, vayne, veigar, vladimir, volibear, warwick, yasuo, yorick, zed, zyra]
unit_list_no_lux = [aatrox, amumu, annie, ashe, azir, brand, braum, diana, dr_mundo, ezreal, ivern, janna, jax, karma, khazix, kindred, kogmaw, leblanc, leona, lucian, malphite, malzahar, maokai, master_yi, nami, nasus, nautilus, neeko, nocturne, olaf, ornn, qiyana_cloud, qiyana_inferno, qiyana_mountain, qiyana_ocean, reksai, renekton, senna, singed, sion, sivir, skarner, soraka, syndra, taliyah, taric, thresh, twitch, varus, vayne, veigar, vladimir, volibear, warwick, yasuo, yorick, zed, zyra]


max_units = 9 # hardcoded in to stop things getting too big

# start = time.time()
# FindingClosedTeamsNoLuxNoQiyana(3)
# end = time.time()
# print 'Time taken = {} minutes'.format(np.around((end-start)/60, 2))

user_max_units = int(input('How many units do you want? An integer please. \n'))

start = time.time()
FindingClosedTeams(user_max_units)
end = time.time()
print('Time taken = {} minutes'.format(np.around((end-start)/60, 2)))

testing = False
if testing: 
	test_team = Team()
	test_team.PrintReport()

	print('Adding Thresh')
	test_team.AddUnit(thresh)
	test_team.PrintReport()

	print('Adding Nautilus')
	test_team.AddUnit(nautilus)
	test_team.PrintReport()

	test_team_2 = Team()

	test_team_2.AddUnit(ivern)
	test_team_2.PrintReport()

	test_team_2.AddUnit(maokai)
	test_team_2.PrintReport()

	test_team_2.AddUnit(neeko)
	test_team_2.PrintReport()

	test_team_3 = Team()

	a = list(itertools.combinations(unit_list_no_weirdness, 2))
	for c in range(len(a)):
		team_list = a[c]
		for unit in team_list:
			test_team_3.AddUnit(unit)
		closed = test_team_3.MachineReport()
		if closed:
			test_team_3.PrintReport()


		test_team_3.WipeTeam()
	pass