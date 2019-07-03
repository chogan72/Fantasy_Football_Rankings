import csv
import os


def next_directory(folder):
    #Change Databse Directory
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


"""
Main
"""

#Stores old directory and changes current
first_directory = os.getcwd()
next_directory('/Database/')


#Sets Fantasy Pros Heading
fp_heading = ['Name', 'Position', 'Team']
#Imports Fantasy Pros Database
FPD = database_reader('Fantasy-Pros-Database.csv', fp_heading)


#Sets PFR Headings
stats_headings = {'Passing':['Player','Tm','Age','Pos','G','GS','QBrec','Cmp','Att','Cmp%','Yds','TD','TD%','Int','Int%','Lng','Y/A ','AY/A ','Y/C','Y/G','Rate','QBR','Sk','Yds','NY/A','ANY/A','Sk%','4QC','GWD'],
                  'Rushing':['Player','Tm','Age','Pos','G','GS','Att','Yds','TD','Lng','Y/A','Y/G','Fmb'],
                  'Receiving':['Player','Tm','Age','Pos','G','GS','Tgt','Rec','Ctch%','Yds','Y/R','TD','Lng','Y/Tgt','R/G','Y/G','Fmb'],
                  'Kicking':['Player','Tm','Age','Pos','G','GS','0-19 FGA','0-19 FGM','20-29 FGA','20-29 FGM','30-39 FGA','30-39 FGM','40-49 FGA','40-49 FGM','50+ FGA','50+ FGM','FGA','FGM','FG%','XPA','XPM','XP%','Pnt','Yds','Lng','Blck ','Y/P'],
                  'Defense':['Tm','G','PF','Yds','Ply','Y/P','TO','FL','1stD','Cmp','Att','Yds','TD','Int','NY/A','1stD','Att','Yds','TD','Y/A','1stD','Pen','Yds','1stPy','Sc%','TO%','EXP'],
                  'Fantasy':['Player','Tm','FantPos','Age','G','GS','Cmp','Att','Yds','TD','Int','Att','Yds','Y/A','TD','Tgt','Rec','Yds','Y/R','TD','Fmb','FL','TD','2PM','2PP','FantPt','PPR','DKPt','FDPt','VBD','PosRank','OvRank']}

#Sets PFR Import Names
stat_dicts = {'Defense-2016': [],'Defense-2017': [],'Defense-2018': [],
              'Fantasy-2016': [],'Fantasy-2017': [],'Fantasy-2018': [],
              'Kicking-2016': [],'Kicking-2017': [],'Kicking-2018': [],
              'Passing-2016': [],'Passing-2017': [],'Passing-2018': [],
              'Receiving-2016': [],'Receiving-2017': [],'Receiving-2018': [],
              'Rushing-2016': [],'Rushing-2017': [],'Rushing-2018': []}

#Scans Database Directory
for file in os.listdir():
    #Filters out non Stat Databases
    if file.startswith('Stats'):
        #Determines Proper List Headings
        for item in stats_headings:
            if item in file:
                function_list = stats_headings[item]
        #Determines Proper List Names
        for title in stat_dicts:
            if title in file:
                stat_dicts[title] = database_reader(file, function_list)

        
#print(stat_dicts['Fantasy-2018'])




"""

This program pulls stats from all of the databases.
Below will be the comination of all the needed data points.

"""


