import nflgame


statistics = {}
for year in range(2016, 2018):
    for week in range(1, 17):
        games = nflgame.games(year=year, week=week)
        players = nflgame.combine_game_stats(games)
        for player in players:
            if player.passing_att > 0 or player.rushing_att > 0 or player.receiving_rec > 0:
                p = nflgame.players[player.playerid]
                statistics= {
                    'year':  year,
                    'week':  week,
                    'player_name':  p.full_name,
                    'passing_attempts': player.passing_att,
                    'passing_yards': player.passing_yds,
                    'passing_touchdowns': player.passing_tds,
                    'passing_interceptions': player.passing_ints,
                    'passing_two_point_attempts': player.passing_twopta,
                    'passing_two_point_made': player.passing_twoptm,
                    'rushing_attempts': player.rushing_att,
                    'rushing_yards': player.rushing_yds,
                    'rushing_touchdowns': player.rushing_tds,
                    'rushing_two_point_attempts': player.rushing_twopta,
                    'rushing_two_point_made': player.rushing_twoptm,
                    'receiving_attempts': player.receiving_rec,
                    'receiving_yards': player.receiving_yds,
                    'receiving_touchdowns': player.receiving_tds,
                    'receiving_two_point_attempts': player.receiving_twopta,
                    'receiving_two_point_made': player.receiving_twoptm,
                    'fumbles': player.fumbles_tot}
            
                print(statistics)
