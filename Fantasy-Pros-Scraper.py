import bs4
import requests
import re
import csv

#Writes Players to CSV file
def database(path):
    with open(path + ".csv", 'a', newline='') as file:
        wr = csv.writer(file, dialect='excel')
        wr.writerow(player)

#beautifulsoup4 link
link = 'https://www.fantasypros.com/nfl/rankings/consensus-cheatsheets.php'
sauce = requests.get(link)
soup = bs4.BeautifulSoup(sauce.text, 'html.parser')
#Fantasy Positions
positions = ['QB', 'RB', 'WR', 'TE', 'K', 'DST']
#Player Format
player = ['Name', 'Position', 'Team']

#Pulls Table Data
for player in soup.find_all('td'):
    #Splits needed information
    gdata = (player.text)
    gdata = re.split('>|<', gdata)
    gdata = gdata[0]
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
                        player = [current, position, last_line[item]]
                        print(player)
                        database('Fantasy-Pros-Database')
            
            #DST
            if position == 'DST':
                last_line = re.split(' ', last_line)
                #Defense Information
                if len(last_line) == 4:
                    player = [last_line[0], position, last_line[1]]
                else:
                    player = [last_line[0] + ' ' + last_line[1], position, last_line[2]]
                #Defense Team
                if len(player[2]) > 7:
                    player[2] = player[2][5:]
                else:
                    player[2] = player[2][4:]
                print(player)
                database('Fantasy-Pros-Database')
            
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
                player = [current, position, last_line[item]]
                #Confirms Player
                if len(player[2]) <= 3 and '.' not in player[2]:
                    print(player)
                    database('Fantasy-Pros-Database')
            
    #Saves player info from last line
    last_line = gdata
