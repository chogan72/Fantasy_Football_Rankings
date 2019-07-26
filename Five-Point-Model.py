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

#Writes Players to CSV file
def database(path, item_list):
    with open(path + '.csv', 'a', newline='') as file:
        wr = csv.writer(file, dialect='excel')
        wr.writerow(item_list)


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
K_head = ['Player','Tm','Age','Pos','G','GS','0-19 FGA','0-19 FGM','20-29 FGA','20-29 FGM','30-39 FGA','30-39 FGM','40-49 FGA','40-49 FGM','50+ FGA','50+ FGM','FGA','FGM','FG%','XPA','XPM','XP%','Pnt','Yds','Lng','Blck ','Y/P']
DST_head = ['Tm','G','PF','Total Yds','Ply','Y/P','TO','FL','1stD','Cmp','Pass Att','Pass Yds','Pass TD','Int','NY/A','Pass 1stD','Rush Att','Rush Yds','Rush TD','Y/A','Rush 1stD','Pen','Pen Yds','1stPy','Sc%','TO%','EXP']

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
    
    #Rookie Check
    rookie_check = 0
    next_directory('/Database/')
    rookie_db = database_reader('Rookies-Database.csv', ['Name','College'])
    for row in rookie_db:
        if player_name[0] == row[0]:
            rookie_check = 1

    #Rookies
    if rookie_check == 1:
        player_list = [player_name, ['Rookie'], [0], [0]]
        next_directory('/Database/College/')
        #Set CSV file
        positions = [['QB','Passing',['Player','School','Conf','G','Cmp','Att','Pct','Yds','Y/A','AY/A','TD','Int','Rate','Rush Att','Rush Yds','Rush Avg','Rush TD']],
                     ['RB','Rushing',['Player','School','Conf','G','Rush Att','Rush Yds','Rush Avg','Rush TD','Pass Rec','Pass Yds','Pass Avg','Pass TD','Plays','Yds','Avg','TD']],
                     ['WR','Receiving',['Player','School','Conf','G','Pass Rec','Pass Yds','Pass Avg','Pass TD','Rush Att','Rush Yds','Rush Avg','Rush TD','Plays','Yds','Avg','TD']],
                     ['K','Kicking',['Player','School','Conf','G','XPM','XPA','XP%','FGM','FGA','FG%','Pts']]]
        for position in positions:
            if position[0] == player_name[1]:
                csv_file = 'College-Stats-' + position[1] +'-2018.csv'
                rookie_stats = database_reader(csv_file, position[2])
                for row in rookie_stats:
                    if player_name[0] == row[0]:
                        year = 0
                        if player_name[1] == 'QB':
                            year = (float(row[7])*.04)+(float(row[10])*4)+(float(row[11])*-4)+(float(row[14])*.1)+(float(row[16])*6)
                        elif player_name[1] == 'RB' or player_name[1] == 'WR':
                            year = (float(row[13])*.1)+(float(row[15])*6)
                        elif player_name[1] == 'K':
                            year = (float(row[7])*.04)
                        player_list[3] = [year]
        next_directory('/Database/Players/')

    #Defense
    elif player_name[1] == 'DST':
        player_list = [player_name, [0], [0], [0]]
        next_directory('/Database/Position/')
        if player_name[0] == 'Los Angeles' or player_name[0] == 'New York':
            player_name[0] = player_name[0] + ' ' + player_name[2][2:]
        #Year Range
        for year in range(2016,2019):
            year_score = 0
            #Set CSV file
            csv_file = 'Stats-Defense-' + str(year) + '.csv'
            dst_stats = database_reader(csv_file, DST_head)
            for row in dst_stats:
                #print(row)
                if player_name[0] in row[0]:
                    for x in range(len(row)):
                        if row[x] == '':
                            row[x] = float(0)
                        elif x > 1 and '%' not in row[x]:
                            row[x] = float(row[x])

                    year_score = 0
                    
                    #Yards
                    if row[3]/16 > 0 and row[3]/16 < 100:
                       year_score += 5
                    elif row[3]/16 >= 100 and row[3]/16 <= 199:
                       year_score += 3
                    elif row[3]/16 >= 200 and row[3]/16 <= 299:
                       year_score += 2
                    elif row[3]/16 >= 350 and row[3]/16 <= 399:
                       year_score -= 1
                    elif row[3]/16 >= 400 and row[3]/16 <= 449:
                       year_score -= 3
                    elif row[3]/16 >= 450 and row[3]/16 <= 499:
                       year_score -= 5
                    elif row[3]/16 >= 500 and row[3]/16 <= 549:
                       year_score -= 6
                    elif row[3]/16 >= 550:
                       year_score -= 7

                    #Points
                    if row[2]/16 == 0:
                       year_score += 5
                    elif row[2]/16 >= 1 and row[2]/16 <= 6:
                       year_score += 4
                    elif row[2]/16 >= 7 and row[2]/16 <= 13:
                       year_score += 3
                    elif row[2]/16 >= 14 and row[2]/16 <= 17:
                       year_score += 1
                    elif row[2]/16 >= 28 and row[2]/16 <= 34:
                       year_score -= 1
                    elif row[2]/16 >= 35 and row[2]/16 <= 45:
                       year_score -= 3
                    elif row[2]/16 >= 46:
                       year_score -= 5

                    #TO
                    year_score += (row[6]/16) * 2
                    #TD
                    year_score += (row[6]/16) * .1 * 6
                    
                    #Adds year scores
                    if year == 2016:
                        player_list[1] = [year_score]
                    elif year == 2017:
                        player_list[2] = [year_score]
                    elif year == 2018:
                        player_list[3] = [year_score]
        next_directory('/Database/Players/')

    #Kickers
    elif player_name[1] == 'K':
        player_list = [player_name, [0], [0], [0]]
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
                        player_list[1] = [year_score]
                    elif year == 2017:
                        player_list[2] = [year_score]
                    elif year == 2018:
                        player_list[3] = [year_score]
        next_directory('/Database/Players/')

    #Skill Players
    else:
        next_directory('/Database/Players/')
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


#Write CSV file
fp_head = ['1','2','3','4','5','6']
next_directory('/Rankings/16-18-Five-Point/')
for players in all_players:
    file_name = players[0][0] + ' Five Point'
    database(file_name, fp_head)
    for item in players:
        if item == []:
            item = [0]
        database(file_name, item)

