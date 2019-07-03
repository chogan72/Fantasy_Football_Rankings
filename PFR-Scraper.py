import bs4
import requests
import re
import csv
import os

#Change Databse Directory
dirpath = os.getcwd()
dirpath = dirpath + '/Database/'
os.chdir(dirpath)

#Writes Players to CSV file
def database(path, item_list):
    with open(path + '.csv', 'a', newline='') as file:
        wr = csv.writer(file, dialect='excel')
        wr.writerow(item_list)  

#Player Stats Header
stats_headings = [['Player','Tm','Age','Pos','G','GS','QBrec','Cmp','Att','Cmp%','Yds','TD','TD%','Int','Int%','Lng','Y/A ','AY/A ','Y/C','Y/G','Rate','QBR','Sk','Yds','NY/A','ANY/A','Sk%','4QC','GWD'],
                  ['Player','Tm','Age','Pos','G','GS','Att','Yds','TD','Lng','Y/A','Y/G','Fmb'],
                  ['Player','Tm','Age','Pos','G','GS','Tgt','Rec','Ctch%','Yds','Y/R','TD','Lng','Y/Tgt','R/G','Y/G','Fmb'],
                  ['Player','Tm','Age','Pos','G','GS','0-19 FGA','0-19 FGM','20-29 FGA','20-29 FGM','30-39 FGA','30-39 FGM','40-49 FGA','40-49 FGM','50+ FGA','50+ FGM','FGA','FGM','FG%','XPA','XPM','XP%','Pnt','Yds','Lng','Blck ','Y/P'],
                  ['Tm','G','PF','Yds','Ply','Y/P','TO','FL','1stD','Cmp','Att','Yds','TD','Int','NY/A','1stD','Att','Yds','TD','Y/A','1stD','Pen','Yds','1stPy','Sc%','TO%','EXP'],
                  ['Player','Tm','FantPos','Age','G','GS','Cmp','Att','Yds','TD','Int','Att','Yds','Y/A','TD','Tgt','Rec','Yds','Y/R','TD','Fmb','FL','TD','2PM','2PP','FantPt','PPR','DKPt','FDPt','VBD','PosRank','OvRank']]

#Position: Column Length
position = {'passing':'29','rushing':'13','receiving':'17','kicking':'27', 'opp':'27', 'fantasy':'32'}
#Years to pull stats from
years = ['2016','2017','2018']
for year in years:
    page_index = 0
    for item in position:
        #Filename Path
        if item == 'opp':
             current_path = 'Stats-Defense-' + year
        else:
            current_path = 'Stats-' + item.capitalize() + '-' + year
        database(current_path, stats_headings[page_index])
        #beautifulsoup4 link
        link = 'https://www.pro-football-reference.com/years/' + year +'/' + item + '.htm'
        sauce = requests.get(link)
        soup = bs4.BeautifulSoup(sauce.text, 'html.parser')
        index = 1
        def_index = 0
        for player in soup.find_all('td'):
            gdata = (player.text)
            #Checks amount of Defence teams in database
            if def_index >= 32:
                break
            else:
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
                    print(stats)
                    database(current_path, stats)
                    index = 0
                    #Adds each defensive team
                    if item == 'opp':
                        def_index += 1
                index += 1
        page_index += 1
