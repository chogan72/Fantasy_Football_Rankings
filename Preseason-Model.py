import csv
import os
import re


#Change Databse Directory
def next_directory(folder):
    os.chdir(first_directory)
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

#Writes Players to CSV file
def database(path, item_list):
    with open(path + '.csv', 'a', newline='') as file:
        wr = csv.writer(file, dialect='excel')
        wr.writerow(item_list)

#Sort Rankings and Create CSV Name
def sort_rank(begining,now_list):
    sorted_list = {key: value for key, value in sorted(now_list.items(), key=lambda x: x[1], reverse=True)}
    csv_name = begining + '-Rankings'
    for thing in sorted_list:
        db_list = []
        db_list.append(thing)
        db_list.append(sorted_list[thing])
        database(csv_name, db_list)


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

K_scoring = [('PAT', 1),
           ('PATM', -1),
           ('FGM', -1),
           ('<39', 3),
           ('40-49', 4),
           ('>50', 5)]

#Player CSV Headings
player_heading = ['Year','Week','Player Name',
              'Passing Attempts','Passing Yards','Passing Touchdowns','Passing Interceptions','Passing Two Point Attempts','Passing Two Point Made',
              'Rushing Attempts','Rushing Yards','Rushing Touchdowns','Rushing Two Point Attempts','Rushing Two Point Made',
              'Receiving Attempts','Receiving Yards','Receiving Touchdowns','Receiving Two Point Attempts','Receiving Two Point Made', 'Fumbles'
              ]
K_head = ['Player','Tm','Age','Pos','G','GS','0-19 FGA','0-19 FGM','20-29 FGA','20-29 FGM','30-39 FGA','30-39 FGM','40-49 FGA','40-49 FGM','50+ FGA','50+ FGM','FGA','FGM','FG%','XPA','XPM','XP%','Pnt','Yds','Lng','Blck ','Y/P']

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
    
    #Kickers
    if player_name[1] == 'K':
        player_list = [player_name, 0, 0, 0]
        next_directory('/Database/Position/')
        #Year Range
        for year in range(2016,2019):
            year_score = 0
            #Set CSV file
            csv_file = 'Stats-Kicking-' + str(year) + '.csv'
            kicker_stats = database_reader(csv_file, K_head)
            for row in kicker_stats:
                if player_name[0] == row[0]:
                    for x in range(len(row)):
                        if row[x] == '':
                            row[x] = float(0)
                        elif x > 3 and '%' not in row[x]:
                            row[x] = float(row[x])
                    yards = ((row[7]+row[9]+row[11]) * 3) + (row[13] * 4) + (row[15] * 5) + row[17]
                    miss = (row[6]+row[8]+row[10]+row[12]+row[14]+row[16]) - (row[7]+row[9]+row[11]+row[13]+row[15]+row[17])
                    year_score = (yards - miss)/row[4]
                    #Adds year scores
                    if year == 2016:
                        player_list[1] = year_score
                    elif year == 2017:
                        player_list[2] = year_score
                    elif year == 2018:
                        player_list[3] = year_score
        next_directory('/Database/Players/')

    #Skill Players
    else:
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
ALL_rankings = {}
QB_rankings = {}
RB_rankings = {}
WR_rankings = {}
TE_rankings = {}
NOQB_rankings = {}
K_rankings = {}

for item in all_players:
    final_pass = 0
    finals = [0,0,0]

    #Finds score for each year
    #Weight for games played
    games_weight = {int(16):float(1.1), int(15):float(1.08), int(14):float(1.06), int(13):float(1.04),
                    int(12):float(1.02), int(11):float(1), int(10):float(.98), int(9):float(.96),
                    int(8):float(.94), int(7):float(.92), int(6):float(.9), int(5):float(.88),
                    int(4):float(.86), int(3):float(.84), int(2):float(.82), int(1):float(.8)}

    #Creates Kicker Year Scores
    if item[0][1] == 'K':
        finals = [item[1],item[2],item[3]]
        
    else:
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
        final = (float(finals[0])*.7)
    #Played in 2017 only
    elif finals[0] == 0 and finals[2] == 0:
        final = (float(finals[1])*.8)
    #Played in 2018 only
    elif finals[0] == 0 and finals[1] == 0:
        final = (float(finals[2])*1.1)
    #Played in 2016, 2017 only
    elif finals[2] == 0:
        final = (float(finals[0])*.3) + (float(finals[1])*.6)
    #Played in 2016, 2018 only
    elif finals[1] == 0:
        final = (float(finals[0])*.25) + (float(finals[2])*.75)
    #Played in 2017, 2018 only
    elif finals[0] == 0:
        final = (float(finals[1])*.35) + (float(finals[2])*.75)
    #Played in 2016, 2017 and 2018
    else:
        final = (float(finals[0])*.15) + (float(finals[1])*.2) + (float(finals[2])*.75)

    #Injury Report
    next_directory('/Database/')
    header = ['Player', 'Position', 'Updated', 'Injury', 'Status']
    IR = database_reader('Injury-Report.csv', header)
    #Scans people on Injury Report
    for injury in IR:
        if item[0][0] == injury[0]:
            if 'IR.' in injury[4] or 'indefinitely' in injury[4]:
                final = 0
            elif 'Questionable' in injury[4]:
                final = final * 15
                final_pass = 1
            elif any(char.isdigit() for char in injury[4]):
                week = int(re.sub("[^0-9]", "", injury[4]))
                if week > int(item[0][3]):
                    week -= 1
                final = final * week
                final_pass = 1

    #Play full season
    if final_pass == 0:
        final = final * 16

    #Write Point Prediction CSV
    next_directory('/Rankings/Preseason-Model')
    db_list = []
    db_list.append(item[0][0])
    db_list.append(final)
    database('Point-Prediction', db_list)

    #Position Weight
    if item[0][1] == 'QB':
        final = final * .55
    elif item[0][1] == 'RB':
        final = final * 1.1
    elif item[0][1] == 'WR':
        final = final * 1.05
    elif item[0][1] == 'TE':
        final = final * 1.2
    elif item[0][1] == 'K':
        final = final * .6

    #Adds Name and Score to Rankings Dictionary
    ALL_rankings[item[0][0]] = final
    if item[0][1] == 'QB':
        QB_rankings[item[0][0]] = final
    elif item[0][1] == 'K':
        K_rankings[item[0][0]] = final
    else:
        NOQB_rankings[item[0][0]] = final
        if item[0][1] == 'RB':
            RB_rankings[item[0][0]] = final
        elif item[0][1] == 'WR':
            WR_rankings[item[0][0]] = final
        elif item[0][1] == 'TE':
            TE_rankings[item[0][0]] = final


#Sorts Players in Order and Creates CSV Files
next_directory('/Rankings/Preseason-Model')
csv_names = ['ALL','QB','RB','WR','TE','NOQB','K']
index = 1
for name in csv_names:
    if index == 1:
        sort_rank(name,ALL_rankings)
    elif index == 2:
        sort_rank(name,QB_rankings)
    elif index == 3:
        sort_rank(name,RB_rankings)
    elif index == 4:
        sort_rank(name,WR_rankings)
    elif index == 5:
        sort_rank(name,TE_rankings)
    elif index == 6:
        sort_rank(name,NOQB_rankings)
    elif index == 7:
        sort_rank(name,K_rankings)
    index += 1

