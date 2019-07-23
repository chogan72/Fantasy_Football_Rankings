import bs4
import requests
import re
import csv
import os


def change_directory(folder):
    #Change Databse Directory
    dirpath = os.getcwd()
    dirpath = dirpath + folder
    os.chdir(dirpath)


def database(path, item_list):
    #Writes Players to CSV file
    with open(path + '.csv', 'a', newline='') as file:
        wr = csv.writer(file, dialect='excel')
        wr.writerow(item_list)


change_directory('\\Database\\')

#Fantasy Positions
positions = ['QB', 'RB', 'WR', 'TE', 'K', 'DST']
#Player Format
players = ['Name', 'Position', 'Team', 'Bye']
database('Fantasy-Pros-Database', players)

#Player Name Fix
players_skip ={
        'Steven Hauschka':'Stephen Hauschka',
        'Mitch Trubisky':'Mitchell Trubisky',
        'Robert Griffin':'Robert Griffin III',
        'Ronald Jones II':'Ronald Jones',
        'Devante Parker':'DeVante Parker',
        'Equanimeous S':'Equanimeous St. Brown',
        'Odell Beckham Jr.':'Odell Beckham',
        'Chris Herndon IV':'Chris Herndon'
        }

#beautifulsoup4 link
BS_link = 'https://www.fantasypros.com/nfl/rankings/consensus-cheatsheets.php'
sauce = requests.get(BS_link)
soup = bs4.BeautifulSoup(sauce.text, 'html.parser')

#Bye week Variable
bye_week = 0

#Pulls Table Data
for player in soup.find_all('td'):
    #Splits needed information
    gdata = (player.text)
    gdata = re.split('>|<', gdata)
    gdata = gdata[0]
    #Bye Week Check
    if bye_week == 1:
        players.append(gdata)
        database('Fantasy-Pros-Database', players)
        bye_week = 0
    #Pulls out player data
    for position in positions:            
        if str(gdata).startswith(position):
            
            #K
            if position == 'K':
                #Removes unneeded results
                kicker = ['K0','K1','K2','K3','K4','K5','K6','K7','K8','K9']
                for number in kicker:
                    if str(gdata).startswith(number):
                        last_line = re.split(' ', last_line)
                        item = len(last_line) - 2
                        #Player Name
                        if '.' in last_line[1]:
                            current = last_line[0] + ' ' + last_line[1][:-2]
                        else:
                            current = last_line[0] + ' ' + last_line[1] + ' ' + last_line[2][:-2]
                        #Player Information
                        players = [current, position, last_line[item]]
                        bye_week = 1
            
            #DST
            elif position == 'DST':
                last_line = re.split(' ', last_line)
                #Defense Information
                if len(last_line) == 4:
                    players = [last_line[0], position, last_line[1]]
                else:
                    players = [last_line[0] + ' ' + last_line[1], position, last_line[2]]
                #Defense Team
                if len(players[2]) > 7:
                    players[2] = players[2][5:]
                else:
                    players[2] = players[2][4:]
                bye_week = 1
            
            #QB, RB, WR, TE
            elif position == 'QB' or position == 'RB' or position == 'WR' or position == 'TE':
                last_line = re.split(' ', last_line)
                item = len(last_line) - 2
                #Player Name
                if '.' in last_line[1]:
                    current = last_line[0] + ' ' + last_line[1][:-2]
                else:
                    current = last_line[0] + ' ' + last_line[1] + ' ' + last_line[2][:-2]
                #Player Information
                players = [current, position, last_line[item]]
                #Confirms Player
                if len(players[2]) <= 3 and '.' not in players[2]:
                    bye_week = 1
                    
            #Name Fix
            for skip in players_skip:
                if players[0] == skip:
                    players[0] = players_skip[skip]
    #Saves player info from last line
    last_line = gdata
