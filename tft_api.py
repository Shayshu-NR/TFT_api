#~~~~~Libraries~~~~~
import requests 
import json
import matplotlib.pyplot as plt
#~~~~~~~~~~~~~~~~~~~

#~~~~~Global Variable~~~~~
API_KEY = '?api_key=RGAPI-2adadb2e-67a6-4e83-bfbf-02f4866c05c1'
USER_NAME = 'DotsXL'
#~~~~~~~~~~~~~~~~~~~~~~~~~

#~~~~~Functions~~~~~
#Make a requrest to riot api and get the puuid from an:
#API key, and summoner name, 
def get_puuid(key, summonerName):
    url_request = 'https://na1.api.riotgames.com/tft/summoner/v1/summoners/by-name/' +  summonerName + key
    responseJson = requests.get(url_request).json()
    puuid = responseJson['puuid']

    return puuid

#Get the number of matches and their respective ids
def get_match_ids(key, puuid):
    url_request = 'https://americas.api.riotgames.com/tft/match/v1/matches/by-puuid/' + puuid + '/ids' + key
    responseJson = requests.get(url_request).json()
    match_ids = responseJson

    return match_ids

#Get the match data for a given match id
def get_match_data(key, match_id):
    url_request = 'https://americas.api.riotgames.com//tft/match/v1/matches/' + match_id + key
    responseJson = requests.get(url_request).json()

    return responseJson

#Get the length of the match respective to the match data
def get_match_length(match_data):
    time = float(match_data['info']['game_length'])

    return time

#Get the time at which the player was eliminated
def get_match_time_eliminated(match_data, player_num):
    elimination = float(match_data['info']['participants'][player_num]['time_eliminated'])

    return elimination

#
def get_placement(match_data, player_num):
    placement = int(match_data['info']['participants'][player_num]['placement'])

    return placement

#Get the level when we were eliminated/won
def get_level(match_data, player_num):
    level = int(match_data['info']['participants'][player_num]['level'])

    return level

#Get the total player damage done in a given match
def get_total_player_damage(match_data, player_num):
    damage = int(match_data['info']['participants'][player_num]['total_damage_to_players'])

    return damage

#
def get_end_board(match_data, player_num, board):
    for i in range(0, len(match_data['info']['participants'][player_num]['units'])):
        
        name  = match_data['info']['participants'][player_num]['units'][i]['character_id']

        board[name[5:]] += 1
    
    return board
#~~~~~~~~~~~~~~~~~~~

#~~~~~ ~~~~~
puuid = get_puuid(API_KEY, USER_NAME)
match_ids = get_match_ids(API_KEY, puuid)
game_length = []
time_eliminated = []
percent_played = []
level = []
total_player_damage = []
placement = []
end_board = {
    'Ahri': 0,
    'Amumu' : 0,
    'Annie': 0,
    'Ashe': 0,
    'AurelionSol': 0,
    'Azir' : 0,
    'Blitzcrank': 0,
    'Braum' : 0,
    'Caitlyn': 0,
    'ChoGath' : 0,
    'Darius' : 0,
    'DrMundo' : 0,
    'Ekko' : 0,
    'Ezreal' : 0,
    'Fiora' : 0,
    'Fizz' : 0,
    'Gangplank' : 0,
    'Graves' : 0,
    'Irelia' : 0,
    'JarvanIV' : 0, 
    'Jayce' : 0,
    'Jhin' : 0,
    'Jinx' : 0,
    'KaiSa' : 0,
    'Karma' : 0,
    'Kassadin' : 0,
    'Kayle' : 0,
    'KhaZix' : 0,
    'KogMaw' : 0,
    'Leona' : 0, 
    'Lucian' : 0,
    'Lulu' : 0,
    'Lux' : 0,
    'Malphite' : 0,
    'MasterYi' : 0,
    'MissFortune' : 0,
    'Mordekaiser' : 0,
    'Neeko' : 0,
    'Poppy' : 0,
    'Rakan' : 0,
    'Rumble' : 0,
    'Shaco' : 0,
    'Shen' : 0,
    'Sona' : 0,
    'Soraka' : 0,
    'Syndra' : 0,
    'Thresh' : 0,
    'TwistedFate' : 0,
    'VelKoz' : 0,
    'Vi' : 0,
    'WuKong' :0,
    'Xayah' : 0,
    'Xerath' : 0,
    'XinZhao' : 0,
    'Yasuo' : 0,
    'Ziggs' : 0,
    'Zoe' : 0
}
end_traits = {
    'Class' : {
        'Set3_Blademaster' : 0,
        'Blaster' : 0,
        'Set3_Brawler' : 0,
        'Demolitionist' : 0,
        'Infiltrator' : 0,
        'ManaReaver' : 0,
        'Mercenary' : 0,
        'Set3_Mystic' : 0,
        'Protector' : 0,
        'Sniper' : 0,
        'Set3_Sorcerer' : 0,
        'Starship' : 0,
        'Vanguard' : 0
    },
    'Origin' : {
        'Set3_Celestial' : 0,
        'Chrono' : 0,
        'Cybernetic' : 0,
        'DarkStar' : 0,
        'MechPilot' : 0,
        'Rebel' : 0,
        'SpacePirate' : 0,
        'StarGuardian' : 0,
        'Set3_Void' : 0
    }
}
axis = []

#Goes through all my match history and gets the relavent information
for j in range(0, len(match_ids)):
    match_data = get_match_data(API_KEY, match_ids[j])
    player_number = 0

    for i in range(0,7):
        if(match_data['metadata']['participants'][i] == puuid):
            player_number = i
    
    #Get the raw data in an easily digestable format for matplotlib
    game_length.append(get_match_length(match_data))
    
    time_eliminated.append(get_match_time_eliminated(match_data, player_number))
    
    level.append(get_level(match_data, player_number))
    
    total_player_damage.append(get_total_player_damage(match_data, player_number))
    
    placement.append(get_placement(match_data, player_number))
    
    percent_played.append((time_eliminated[j]/game_length[j])*100)

    get_end_board(match_data, player_number, end_board)
    
    axis.append(j)

plt.plot(axis, percent_played)
plt.show()

print(game_length)
print(time_eliminated)
print(level)
print(total_player_damage)
print(end_board)
#~~~~~ ~~~~~

