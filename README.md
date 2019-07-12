# Fantasy Football Rankings

This project pulls data from multiple sources and creates fantasy football ranking models.

## Current Status

I have just recently finished collecting all the data I need for making my models. The next step is to make a preseason fantasy football ranking. I plan to keep this updated through out the season with mid-season rankings.

## Database Files

* Fantasy Pros Scraper
  * This is used to scrape https://www.fantasypros.com/nfl/rankings/consensus-cheatsheets.php to find all the current players is fantasy rankings. It also records there position and teams.
  * This is used to create Database/Fantasy-Pros-Database.csv
* Pro Football Reference
  * This is used to scrape https://www.pro-football-reference.com/years/2018/fantasy.htm to pull season long stats.
  * It also pulls stats form position specific pages to get more complete stats
  * This is used to create the files in Database/Position/
* Player Game Logs
  * This uses the nflgame api (https://github.com/derek-adair/nflgame) to pull player stats by games. 
  * This is used to create the files in Database/Players/
  
## Models

Coming Soon...

## Issues

* In the Player-API.py file there are four players that cause the program to break. My work around is just to skip them since the only played a few games. I have tried updateing the players file multiple times but the problem is still there. If anyone knows a fix for this please let me know.
* I intially tried to use the SportsReference API (https://sportsreference.readthedocs.io/en/stable/), but there were multiple issues pulling data.
