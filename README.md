# Fantasy Football Rankings

This project pulls data from multiple sources and creates fantasy football ranking models.


## Current Status

I have just recently finished creating the preseson model. There are some slight tweaks that can still be made to improve accuracy. One of which includes creating rookie rankings. I plan to keep this updated through out the season with mid-season rankings.


## Database Files

* CBS Injury Scraper
  * This is used to scrape https://www.cbssports.com/nfl/injuries/ to find the current Injury Report.
  * This is used to create Database/Injury-Report.csv
* Fantasy Pros Scraper
  * This is used to scrape https://www.fantasypros.com/nfl/rankings/consensus-cheatsheets.php to find all the current players in fantasy rankings. It also records there position, team, and bye week.
  * This is used to create Database/Fantasy-Pros-Database.csv
* Pro Football Reference
  * This is used to scrape https://www.pro-football-reference.com/years/2018/fantasy.htm to pull season long stats.
  * It also pulls stats form position specific pages to get more complete stats
  * This is used to create the files in Database/Position/
* Player Game Logs
  * This uses the nflgame api (https://github.com/derek-adair/nflgame) to pull player stats by games. 
  * This is used to create the files in Database/Players/
  
  
## Models

### Preseason Model

#### Scoring

* The first step to creating the model is determining players yearly fantasy points. This is done by using the player game logs to determine there scores.

#### Five Point
* Next, the 5 point analysis is created. This includes the Ceiling, High, Mid, Low and Floor. Depending on how many games a player played in a given season will determine the weighting of these categories. The below image illustrates how those averages are determined.

<img align="center" src="https://raw.githubusercontent.com/chogan72/Fantasy_Football_Rankings/master/RM-Files/Five-Point.JPG"></img>

#### Formula
* Next, I took those 5 stats to create a weekly average using the formula below.

<p align="center"> ((Ceiling - Low) * .1) + (High * .3) + (Mid * .2) + (Low * .3) + ((Floor - Low) * .1) </p>

#### Weight for weeks played
* That Number is then multiplied by the proper weight based on the number of games played.

 <table align="center"><thead>
  <tr align="center">
   <th>16</th><th>15</th><th>14</th><th>13</th><th>12</th><th>11</th><th>10</th><th>9</th><th>8</th><th>7</th><th>6</th><th>5</th><th>4</th><th>3</th><th>2</th><th>1</th>
  </tr><thead>
  <tbody><tr align="center">
   <td>1.10</td><td>1.08</td><td>1.06</td><td>1.04</td><td>1.02</td><td>1.00</td><td>.98</td><td>.96</td><td>.94</td><td>.92</td><td>.90</td><td>.88</td><td>.86</td><td>.84</td><td>.82</td><td>.80</td>
  </tr>
 </tbody></table>
 
#### Weight for years played
* Once this number is determined for the previous 3 years, those 3 numbers are weighted depending on how many seasons they played. The weightings below are for the 2019 preseason. 
  * The Heading years represent the years played. 
  * The Column years represent the year weights.

<table align="center"><thead>
  <th></th><th>18, 17, 16</th><th>18, 17</th><th>18, 16</th><th>17, 16</th><th>18</th><th>17</th><th>16</th>
 </thead>
 <tbody>
  <tr align="center">
   <td>2018</td><td>.75</td><td>.75</td><td>.75</td><td>-</td><td>1.1</td><td>-</td><td>-</td>
  </tr>
  <tr align="center">
   <td>2017</td><td>.2</td><td>.35</td><td>-</td><td>.6</td><td>-</td><td>.8</td><td>-</td>
  </tr>
  <tr align="center">
   <td>2016</td><td>.15</td><td>-</td><td>.25</td><td>.3</td><td>-</td><td>-</td><td>.7</td>
  </tr>
 </tbody></table>
 
#### Injuries and Suspensions
* Finally any Injuries and Suspensions are factored in. For example:
  * If someone has a 4 game suspension there current score would be multiplied by 12
  * Someone with no suspension would have there current score multiplied by 16
  
<h3 align="center"><b>This final number is the players total point projection for the year.</b></h3>

* This number is then added to the Point-Prediction.csv file

#### Rankings

* Each position is weighted to get an accurate overall ranking.

<table align="center"><thead>
  <th>QB</th><th>RB</th><th>WR</th><th>TE</th><th>K</th><th>DST</th>
 </thead>
 <tbody>
  <tr align="center">
   <td>0.55</td><td>1.10</td><td>1.05</td><td>1.20</td><td>0.60</td><td>1.00</td>
  </tr>
 </tbody></table>
 
* This number is the used to create the ranking csv files. This number is NOT there point prediction for the season. To get point predictions check out Point-Prediction.csv file.

## Issues

* Preseason Model
  * This does not include any Rookies
  * If players names are inconsistent between databases they are not ranked
* In the Player-API.py file there are four players that cause the program to break. My work around is just to skip them since the only played a few games. I have tried updating the players file multiple times but the problem is still there. 
