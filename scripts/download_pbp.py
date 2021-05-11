import time
import pathlib
import pandas as pd
import os

from api_helper import Client
from endpoints import PlayByPlay, BoxScoreAdvanced

# Download each measure type, for each season
Seasons = ['2013-14', '2014-15', '2016-17', 
           '2017-18', '2018-19', '2019-20']

def calculate_time_at_period(period):
    if period > 5:
        return (720 * 4 + (period - 5) * (5 * 60)) * 10
    else:
        return (720 * (period - 1)) * 10

def split_subs(df, tag):
    subs = df[[tag, 'PERIOD', 'time']]
    subs['SUB'] = tag
    subs.columns = ['PLAYER_ID', 'PERIOD', 'time', 'SUB']
    return subs

def get_pbp_and_starters(game_id, pbp = None):
    
    client = Client()
    
    if pbp is None:
        e_pbp = PlayByPlay(game_id)
        pbp = client.make_request(e_pbp)
    
        def f(v):
            m, s = v.split(":")
            return 12 * 60 - (int(m) * 60 + int(s))
        pbp['time'] = pbp['PCTIMESTRING'].apply(f)
    
    # Get the subsitution times
    substitutions = pbp[pbp["EVENTMSGTYPE"] == 8][['PERIOD', 'time', 'PLAYER1_ID', 'PLAYER2_ID']]
    substitutions.columns = ['PERIOD', 'time', 'OUT', 'IN']

    # Split to sub in and sub out events
    subs_in = split_subs(substitutions, 'IN')
    subs_out = split_subs(substitutions, 'OUT')

    full_subs = pd.concat([subs_out, subs_in], axis=0).reset_index()[['PLAYER_ID', 'PERIOD', 'time', 'SUB']]
    first_event_of_period = full_subs.loc[full_subs.groupby(by=['PERIOD', 'PLAYER_ID'])['time'].idxmin()]
    players_subbed_in_at_each_period = first_event_of_period[first_event_of_period['SUB'] == 'IN'][['PLAYER_ID', 'PERIOD', 'SUB']]

    periods = players_subbed_in_at_each_period['PERIOD'].drop_duplicates().values.tolist()

    frames = []
    for period in periods:
        time.sleep(1)
        low = calculate_time_at_period(period) + 5
        high = calculate_time_at_period(period + 1) - 5
        e_bs = BoxScoreAdvanced(game_id, startRange=low, endRange=high)
        boxscore = client.make_request(e_bs)
        boxscore_players = boxscore[['PLAYER_NAME', 'PLAYER_ID', 'TEAM_ABBREVIATION']]
        boxscore_players['PERIOD'] = period

        players_subbed_in_at_period = players_subbed_in_at_each_period[players_subbed_in_at_each_period['PERIOD'] == period]

        joined_players = pd.merge(boxscore_players, players_subbed_in_at_period, on=['PLAYER_ID', 'PERIOD'], how='left')
        joined_players = joined_players[pd.isnull(joined_players['SUB'])][['PLAYER_NAME', 'PLAYER_ID', 'TEAM_ABBREVIATION', 'PERIOD']]
        frames.append(joined_players)

    starters = pd.concat(frames)
    
    
    return pbp, starters

for season in Seasons:
    game_ids = pd.read_csv('../data/game_ids/{}.csv'.format(season), header = None)[0].values
    for game_id in game_ids:
        gid = '00' + str(game_id)
        if not os.path.exists("../data/pbp/{}/{}.csv".format(season, gid)):
            try:
                time.sleep(1)
                print("%s - %s" % (season, gid))
                pbp, starters = get_pbp_and_starters(gid)
                pbp.to_csv('../data/pbp/{}/{}.csv'.format(season, gid), sep=',', index=False)
                starters.to_csv('../data/pbp/{}/{}_{}.csv'.format(season, gid, "starters"), sep=',', index=False)
            except KeyboardInterrupt:
                raise
            except:
                print("Error")
                pass
        else:
            print("Reprocessing {} - {}".format(season, gid))
            if os.path.exists("../data/pbp/{}/{}_starters.csv".format(season, gid)):
                df = pd.read_csv("../data/pbp/{}/{}_starters.csv".format(season, gid))
                if (df.groupby(['TEAM_ABBREVIATION', 'PERIOD'])['PLAYER_ID'].count() != 5).sum() > 0:
                    pbp = pd.read_csv("../data/pbp/{}/{}.csv".format(season, gid))
                    _, starters = get_pbp_and_starters(gid, pbp = pbp)
                    starters.to_csv("../data/pbp/{}/{}_{}.csv".format(season, gid, "starters"), sep = ",", index = False)
            else:
                pbp = pd.read_csv("../data/pbp/{}/{}.csv".format(season, gid))
                _, starters = get_pbp_and_starters(gid, pbp = pbp)
                starters.to_csv("../data/pbp/{}/{}_{}.csv".format(season, gid, "starters"), sep = ",", index = False)
