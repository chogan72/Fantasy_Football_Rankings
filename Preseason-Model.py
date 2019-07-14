import csv
import os
import re


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

#Creates Yearly Score
def year_proj(year):
    score = 0
    high = item[year][3] * .3
    mid = item[year][2] * .2
    low = item[year][1] * .3
    ceiling = (item[year][4] - item[year][1]) * .1
    floor = (item[year][0] - item[year][1]) * .1
    score = high + mid + low + ceiling + floor
    for weight in games_weight:
        if weight == item[year][5]:
            return(score * games_weight[weight])



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
fp_heading = ['Name', 'Position', 'Team', 'Bye']
#Imports Fantasy Pros Database
FPD = database_reader('Fantasy-Pros-Database.csv', fp_heading)

#Change to Player Directory
next_directory('/Database/Players/')
#List of all Players
all_players = []

#Players inside Fantasy Pros Database
for player_name in FPD:
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
                five_point = [low,(mid/2)+(low/2),mid,(high/2)+(low/2),high]

            five_point.append(weeks_played)

            #Write player data to player list
            if week[0] == '2016':
                player_list[1] = five_point
            elif week[0] == '2017':
                player_list[2] = five_point
            elif week[0] == '2018':
                player_list[3] = five_point

    #Add Players to List
    all_players.append(player_list)


#Creates Ranking Dictionary    
rankings = {}
for item in all_players:
    final_pass = 0
    finals = [0,0,0]

    #Finds score for each year
    #Weight for games played
    games_weight = {int(16):float(1.1), int(15):float(1.08), int(14):float(1.06), int(13):float(1.04),
                    int(12):float(1.02), int(11):float(1), int(10):float(.98), int(9):float(.96),
                    int(8):float(.94), int(7):float(.92), int(6):float(.9), int(5):float(.88),
                    int(4):float(.86), int(3):float(.84), int(2):float(.82), int(1):float(.8)}
    #2018
    if len(item[3]) >= 5:
        finals[2] = year_proj(3)
    #2017
    if len(item[2]) >= 5:
        finals[1] = year_proj(2)
    #2016
    if len(item[1]) >= 5:
        finals[0] = year_proj(1)

    #Didn't Play
    if finals[0] == 0 and finals[1] == 0 and finals[2] == 0:
        final = 0
    #Played in 2016 only
    elif finals[1] == 0 and finals[2] == 0:
        final = (float(finals[0])*.7) + (float(finals[1])*.1) + (float(finals[2])*.2)
    #Played in 2017 only
    elif finals[0] == 0 and finals[2] == 0:
        final = (float(finals[1])*.8) + (float(finals[2])*.2)
    #Played in 2018 only
    elif finals[0] == 0 and finals[1] == 0:
        final = (float(finals[2]))
    #Played in 2016, 2017 only
    elif finals[2] == 0:
        final = (float(finals[0])*.35) + (float(finals[1])*.45) + (float(finals[2])*.2)
    #Played in 2016, 2018 only
    elif finals[1] == 0:
        final = (float(finals[0])*.25) + (float(finals[2])*.75)
    #Played in 2017, 2018 only
    elif finals[0] == 0:
        final = (float(finals[1])*.3) + (float(finals[2])*.7)
    #Played in 2016, 2017 and 2018
    else:
        final = (float(finals[0])*.15) + (float(finals[1])*.25) + (float(finals[2])*.6)

    #Injury Report
    next_directory('/Database/')
    header = ['Player', 'Position', 'Updated', 'Injury', 'Status']
    IR = database_reader('Injury-Report.csv', header)
    #Scans people on Injury Report
    for injury in IR:
        if item[0][0] == injury[0] and injury[4] != 'Questionable for the start of training camp':
            if 'IR.' in injury[4] or 'indefinitely' in injury[4]:
                final = 0

            elif any(char.isdigit() for char in injury[4]):
                week = int(re.sub("[^0-9]", "", injury[4]))
                if week > int(item[0][3]):
                    week -= 1
                    final = final * week
                    final_pass = 1

    if final_pass == 0:
        final = final * 16
    
    #Adds Name and Score to Rankings Dictionary
    rankings[item[0][0]] = final

#Sorts Players in Order
rankings_sorted = {key: value for key, value in sorted(rankings.items(), key=lambda x: x[1], reverse=True)}
print(rankings_sorted)
