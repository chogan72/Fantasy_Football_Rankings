import bs4
import requests
import re
import csv
import os

#Change Databse Directory
dirpath = os.getcwd()
dirpath = dirpath + '/Database/College/'
os.chdir(dirpath)

#Writes Players to CSV file
def database(path, item_list):
    with open(path + '.csv', 'a', newline='') as file:
        wr = csv.writer(file, dialect='excel')
        wr.writerow(item_list)  

#Player Stats Header
stats_headings = [['Player','School','Conf','G','Cmp','Att','Pct','Yds','Y/A','AY/A','TD','Int','Rate','Att','Yds','Avg','TD'],
                  ['Player','School','Conf','G','Att','Yds','Avg','TD','Rec','Yds','Avg','TD','Plays','Yds','Avg','TD'],
                  ['Player','School','Conf','G','Rec','Yds','Avg','TD','Att','Yds','Avg','TD','Plays','Yds','Avg','TD'],
                  ['Player','School','Conf','G','XPM','XPA','XP%','FGM','FGA','FG%','Pts']]

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
                database(current_path, stats)
                index = 0
                #Adds each defensive team
                if item == 'opp':
                    def_index += 1
            index += 1
        page_index += 1
