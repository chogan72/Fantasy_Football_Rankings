import csv
import os


def next_directory(folder):
    #Change Databse Directory
    os.chdir(first_directory)
    dirpath = os.getcwd()
    dirpath = dirpath + folder
    os.chdir(dirpath)

def database_reader(current_file, head_list):
    database_players = []
    #Read Database Files
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
    return(database_players)

#Finds 3 middle numbers
def stat():
    mid = 0
    index = 0
    while index < mid_len:
        if top_len < 0:
            mid += points_list[-index+top_len]
        else:
            mid += points_list[index+top_len]
        index += 1
    return(mid/mid_len)



#Fantasy Scorring Breakdown
scoring = [('Passing Yards', 0.04),
           ('Passing Touchdowns', 4),
           ('Passing Interceptions', -4),
           ('Passing Two Point Made', 2),
           ('Rushing Yards', .1),
           ('Rushing Touchdowns', 6),
           ('Rushing Two Point Made', 2),
           ('Receiving Yards', .1),
           ('Receiving Touchdowns', 6),
           ('Receiving Two Point Made', 2),
           ('Fumbles', -2)]

#Player CSV Headings
player_heading = ['Year','Week','Player Name',
              'Passing Attempts','Passing Yards','Passing Touchdowns','Passing Interceptions','Passing Two Point Attempts','Passing Two Point Made',
              'Rushing Attempts','Rushing Yards','Rushing Touchdowns','Rushing Two Point Attempts','Rushing Two Point Made',
              'Receiving Attempts','Receiving Yards','Receiving Touchdowns','Receiving Two Point Attempts','Receiving Two Point Made', 'Fumbles'
              ]

#Stores old directory and changes current
first_directory = os.getcwd()
next_directory('/Database/')

#Sets Fantasy Pros Heading
fp_heading = ['Name', 'Position', 'Team']
#Imports Fantasy Pros Database
FPD = database_reader('Fantasy-Pros-Database.csv', fp_heading)
FPD.append(['Test','Test','Test'])

#Change to Player Directory
next_directory('/Database/Players/')
#List of all Players
all_players = []
#Player Info
player_list = ['Name', '2016', '2017', '2018']

#Players inside Fantasy Pros Database
for player_name in FPD:
    all_players.append(player_list)
    player_list = [player_name, [], [], []]
    for file_name in os.listdir():
        #Checks player names with file names
        if player_name[0] in file_name:
            #Reads Player Databases
            player_stats = database_reader(file_name,player_heading)

            #Set Variables
            weeks_played = len(player_stats)
            points_list = []
            five_point = [0,0,0,0,0]
            fp_2016 =[]
            fp_2017 =[]
            for week in player_stats:
                #Calculates weekly fantasy points
                passing_points = (int(week[4])*float(scoring[0][1])) + (int(week[5])*int(scoring[1][1])) + (int(week[6])*int(scoring[2][1])) + (int(week[8])*int(scoring[3][1]))
                rushing_points = (int(week[10])*float(scoring[4][1])) + (int(week[11])*int(scoring[5][1])) + (int(week[13])*int(scoring[6][1])) + (int(week[19])*int(scoring[10][1]))
                receiving_points = (int(week[15])*float(scoring[7][1])) + (int(week[16])*int(scoring[8][1])) + (int(week[18])*int(scoring[9][1]))
                fantasy_points = passing_points + rushing_points + receiving_points
                points_list.append(fantasy_points)
                
            #sorts list form Low to High
            points_list.sort()
            
            #Find range for spread and Sets Floor and Ceiling
            if weeks_played >= 13:
                top_len = 3
                five_point[0] = (points_list[0]+points_list[1]+points_list[2])/top_len
                five_point[4] = (points_list[weeks_played-1]+points_list[weeks_played-2]+points_list[weeks_played-3])/top_len
            elif weeks_played >= 9 and weeks_played <= 12:
                top_len = 2
                five_point[0] = (points_list[0]+points_list[1])/top_len
                five_point[4] = (points_list[weeks_played-1]+points_list[weeks_played-2])/top_len
            elif weeks_played >= 6 and weeks_played <= 8:
                top_len = 1
                five_point[0] = points_list[0]
                five_point[4] = points_list[weeks_played-1]

            #Stas for Players who played 6 games or more
            if weeks_played >=6:
                #Mid length
                mid_len = (weeks_played-(top_len*2))
                #Mid Stat
                five_point[2] = stat()
                #Half Mid Length
                mid_len = mid_len/2
                if mid_len % 2 == 0:
                    pass
                else:
                    mid_len - .5
                #Low Stat
                five_point[1] = stat()
                #High Stat
                top_len = -top_len-1
                five_point[3] = stat()
                
            #Stas for Players who played 5 games or less
            else:
                low = min(points_list)
                mid = sum(points_list)/len(points_list)
                high = max(points_list)
                five_point = [low,(mid/2)+(low/2)/len(points_list),mid,(high/2)+(low/2)/len(points_list),high]

            #Write player data to player list
            if week[0] == '2016':
                player_list[1] = five_point
            elif week[0] == '2017':
                player_list[2] = five_point
            elif week[0] == '2018':
                player_list[3] = five_point
                
#Testing All Players Database
for item in all_players:
    print(item)
            
