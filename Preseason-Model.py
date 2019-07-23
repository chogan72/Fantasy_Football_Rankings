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

#Creates Yearly Score
def year_proj(year):
    score = 0
    high = float(item[year][3]) * .3
    mid = float(item[year][2]) * .2
    low = float(item[year][1]) * .3
    ceiling = (float(item[year][4]) - float(item[year][1])) * .1
    floor = (float(item[year][0]) - float(item[year][1])) * .1
    score = high + mid + low + ceiling + floor
    for weight in games_weight:
        if int(weight) == int(item[year][5]):
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
    database(csv_name, rank_head)
    index = 1
    for thing in sorted_list:
        for ranks in ALL_print:
            if thing == ranks[1]:
                ranks[0] = index
                database(csv_name, ranks)
                index += 1

#Read Five Point
all_players = []
first_directory = os.getcwd()
next_directory('/Rankings/16-18-Five-Point/')
fp_head = ['1','2','3','4','5','6']
for file in os.listdir(os.getcwd()):
    this_list = database_reader(file, fp_head)
    if this_list[0][1] == 'K' or this_list[0][1] == 'DST':
        this_list[3] = this_list[3][0]
        this_list[2] = this_list[2][0]
        this_list[1] = this_list[1][0]
    else:
        if this_list[1][0] == '0':
            this_list[1] = []
        if this_list[2][0] == '0':
            this_list[2] = []
        if this_list[3][0] == '0':
            this_list[3] = []
    all_players.append(this_list)

#Creates Ranking Dictionary
ALL_rankings = {}
QB_rankings = {}
RB_rankings = {}
WR_rankings = {}
TE_rankings = {}
FLEX_rankings = {}
K_rankings = {}
DST_rankings = {}
ALL_print = []

rank_head = ['Rank','Name','Team','Position','Bye','Point Prediction']

for item in all_players:
    final_pass = 0
    finals = [0,0,0]
    rank_print = ['',item[0][0],item[0][2],item[0][1],item[0][3],'']

    #Finds score for each year
    #Weight for games played
    games_weight = {int(16):float(1.1), int(15):float(1.08), int(14):float(1.06), int(13):float(1.04),
                    int(12):float(1.02), int(11):float(1), int(10):float(.98), int(9):float(.96),
                    int(8):float(.94), int(7):float(.92), int(6):float(.9), int(5):float(.88),
                    int(4):float(.86), int(3):float(.84), int(2):float(.82), int(1):float(.8)}

    #Creates Kicker Year Scores
    if item[0][1] == 'K' or item[0][1] == 'DST':
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
            if 'IR. Injured Reserve' in injury[4] or 'indefinitely' in injury[4] or 'Physically Unable to Perform' in injury[4]:
                final = 0
            elif any(char.isdigit() for char in injury[4]):
                week = int(re.sub("[^0-9]", "", injury[4]))
                if item[0][2] != 'FA' and week > int(item[0][3]):
                    week -= 1
                final = final * (16 - week)
                final_pass = 1
            elif 'Questionable' in injury[4] or 'Out for the start of training camp' in injury[4]:
                final = final * 15
                final_pass = 1
           
    #Play full season
    if final_pass == 0:
        final = final * 16

    #Write Point Prediction
    rank_print[5] = final

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
    elif item[0][1] == 'DST':
        final = final * 1


    #Adds Name and Score to Rankings Dictionary
    ALL_print.append(rank_print)
    ALL_rankings[item[0][0]] = final
    if item[0][1] == 'QB':
        QB_rankings[item[0][0]] = final
    elif item[0][1] == 'K':
        K_rankings[item[0][0]] = final
    elif item[0][1] == 'DST':
        DST_rankings[item[0][0]] = final
    else:
        FLEX_rankings[item[0][0]] = final
        if item[0][1] == 'RB':
            RB_rankings[item[0][0]] = final
        elif item[0][1] == 'WR':
            WR_rankings[item[0][0]] = final
        elif item[0][1] == 'TE':
            TE_rankings[item[0][0]] = final


#Sorts Players in Order and Creates CSV Files
next_directory('/Rankings/Preseason-Model')
csv_names = ['ALL','QB','RB','WR','TE','FLEX','K','DST']
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
        sort_rank(name,FLEX_rankings)
    elif index == 7:
        sort_rank(name,K_rankings)
    elif index == 8:
        sort_rank(name,DST_rankings)
    index += 1
    
