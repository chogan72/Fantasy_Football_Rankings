import bs4
import requests
import re
import csv
import os

first_directory = os.getcwd()
#Change Databse Directory
def next_directory(folder):
    os.chdir(first_directory)
    dirpath = os.getcwd()
    dirpath = dirpath + folder
    os.chdir(dirpath)

#Writes Players to CSV file
def database(path, item_list):
    with open(path + '.csv', 'a', newline='') as file:
        wr = csv.writer(file, dialect='excel')
        wr.writerow(item_list)
        
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

#Player Stats Header
stats_headings = [['Player','School','Conf','G','Cmp','Att','Pct','Yds','Y/A','AY/A','TD','Int','Rate','Att','Yds','Avg','TD'],
                  ['Player','School','Conf','G','Att','Yds','Avg','TD','Rec','Yds','Avg','TD','Plays','Yds','Avg','TD'],
                  ['Player','School','Conf','G','Rec','Yds','Avg','TD','Att','Yds','Avg','TD','Plays','Yds','Avg','TD'],
                  ['Player','School','Conf','G','XPM','XPA','XP%','FGM','FGA','FG%','Pts']]

FP_head = ['Name','Position','Team','Bye']

next_directory('/Database/College/')
#Position: Column Length
position = {'passing':'17','rushing':'16','receiving':'16','kicking':'11'}
#Years to pull stats from
for year in range(2016,2019):
    page_index = 0
    for item in position:
        #Filename Path
        current_path = 'College-Stats-' + item.capitalize() + '-' + str(year)
        database(current_path, stats_headings[page_index])
        #beautifulsoup4 link
        link = 'https://www.sports-reference.com/cfb/years/' + str(year) + '-' + item + '.html'
        sauce = requests.get(link)
        soup = bs4.BeautifulSoup(sauce.text, 'html.parser')
        index = 1
        for player in soup.find_all('td'):
            gdata = (player.text)
            #First Column in File
            if index == 1:
                stats = []
                #Removes All-Pro and Pro-Bowl markers
                if '+' in gdata:
                    gdata = gdata[:-1]
                if '*' in gdata:
                    gdata = gdata[:-1]
            #Add item to row
            stats.append(gdata)
            #End of Column
            if index == int(position[item]):
                if year == 2018:
                    next_directory('/Database/')
                    FP_file = database_reader('Fantasy-Pros-Database.csv', FP_head)
                    for row in FP_file:
                        if row[0] == stats[0]:
                            database('Rookies-Database', [stats[0],stats[1]])
                next_directory('/Database/College/')         
                database(current_path, stats)
                index = 0
                #Adds each defensive team
                if item == 'opp':
                    def_index += 1
            index += 1
        page_index += 1
