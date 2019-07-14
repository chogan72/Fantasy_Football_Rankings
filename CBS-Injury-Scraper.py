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

#beautifulsoup4 link
BS_link = 'https://www.cbssports.com/nfl/injuries/'
sauce = requests.get(BS_link)
soup = bs4.BeautifulSoup(sauce.text, 'html.parser')

#Variables
header = ['Player', 'Position', 'Updated', 'Injury', 'Status']
database('Injury-Report', header)
final = []
index = 0

for player in soup.find_all("td"):
    #Splits needed information
    gdata = (player.text)
    gdata = re.split(">|<|\n", gdata)
    for person in gdata:
        if re.search('[a-zA-Z]+',person):
            final.append(person.strip())
            index += 1
        if index == 6:
            final.pop(0)
            database('Injury-Report', final)
            final = []
            index = 0
            
    
