import nflgame
import os
import csv


#Change Databse Directory
def next_directory(folder):
    dirpath = os.getcwd()
    dirpath = dirpath + folder
    os.chdir(dirpath)

#Read Database Files
def database_reader(current_file, head_list):
    database_players = []
    with open(current_file) as csvfile:
        reader = csv.DictReader(csvfile)
        #Reads rows of CSV file
        for row in reader:
            index = 0
            player_list = []
            #Sets row to proper information
            while index < len(row):
                player_list.append(row[head_list[index]])
                index += 1
            database_players.append(player_list)
    #Returns Database as List
    return(database_players)

#Writes Players to CSV file
def database(path, item_list):
    with open(path + '.csv', 'ab') as file:
        wr = csv.writer(file, dialect='excel')
        wr.writerow(item_list)

#Coverts Dictionary to list
def dict_list(dic, position):
    new_list = []
    for item in dic:
        new_list.append(item[position])
    return(new_list)


#Stores old directory and changes current
first_directory = os.getcwd()
next_directory('/Database/')
#Sets Fantasy Pros Heading
fp_heading = ['Name', 'Position', 'Team', 'Bye']
#Imports Fantasy Pros Database
FPD = database_reader('Fantasy-Pros-Database.csv', fp_heading)
#Returns to original directory
os.chdir(first_directory)


#Sets Year Range
first = '2016'
last = '2018'

#Players to Skip
#Shaun Wilson, David Grinnage, David Williams, Keith Ford, David Johnson(FB)
id_skip = ['00-0034621','00-0032634','00-0034427','00-0034509','00-0026957']
           
#Change directory to Players Database
next_directory('/Database/Players/')

for year in range(int(first), int(last)+1):
    for week in range(1, 18):
        games = nflgame.games(year=year, week=week)
        players = nflgame.combine_game_stats(games)
        for player in players:
            statistics = {}
            #Verrifies Fantasy Players
            if player.passing_att > 0 or player.rushing_att > 0 or player.receiving_rec > 0:
                #Skip broken players
                if player.playerid in id_skip:
                    pass
                else:
                    #Stats needed for players
                    statistics = [
                        ('Year', year),
                        ('Week',  week),
                        ('Player Name',  nflgame.players[player.playerid].full_name),
                        ('Passing Attempts', player.passing_att),
                        ('Passing Yards', player.passing_yds),
                        ('Passing Touchdowns', player.passing_tds),
                        ('Passing Interceptions', player.passing_ints),
                        ('Passing Two Point Attempts', player.passing_twopta),
                        ('Passing Two Point Made', player.passing_twoptm),
                        ('Rushing Attempts', player.rushing_att),
                        ('Rushing Yards', player.rushing_yds),
                        ('Rushing Touchdowns', player.rushing_tds),
                        ('Rushing Two Point Attempts', player.rushing_twopta),
                        ('Rushing Two Point Made', player.rushing_twoptm),
                        ('Receiving Attempts', player.receiving_rec),
                        ('Receiving Yards', player.receiving_yds),
                        ('Receiving Touchdowns', player.receiving_tds),
                        ('Receiving Two Point Attempts', player.receiving_twopta),
                        ('Receiving Two Point Made', player.receiving_twoptm),
                        ('Fumbles', player.fumbles_tot)
                            ]


                    for item in FPD:
                        #compares Database to NFLgame
                        if item[0] == statistics[2][1]:
                            #Creates file path
                            new_file = item[0] + ' ' + str(year)
                            current_path = os.getcwd() + '\\' + new_file +'.csv'
                            if os.path.isfile(current_path):
                                pass
                            #Adds header
                            else:
                                head = dict_list(statistics, 0)
                                database(new_file, head)
                            #Writes Data
                            row = dict_list(statistics, 1)
                            database(new_file, row)

                                
