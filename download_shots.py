import requests
import time
import sys
import json
import pandas as pd
import argparse
import pathlib
import os.path

from api_helper import Client
from endpoints import ShotMapEndpoint

def download_season_data(player_id):
    if os.path.exists("players_data/%s" % player_id):
        return

    pathlib.Path("players_data/%s" % player_id).mkdir(parents = True, exist_ok = True)

    Seasons = ['2013-14', '2014-15', '2015-16', '2016-17', '2017-18', '2018-19', '2019-20']

    client = Client()
    # Download each seasons data
    for season in Seasons:
        time.sleep(5)
        print("%s - %s" % (season, player_id))
        e = ShotMapEndpoint(player_id, season)
        df = client.make_request(e)
        # write to csv
        if df.shape[0] > 0:
            df.to_csv('players_data/%s/%s_shots.csv' % (player_id,season) , sep = ',', index = False)

# Parse arguments for player and map it to the player id
parser = argparse.ArgumentParser()
parser.add_argument("--player", help="the player to download shots for")
parser.add_argument("--all", help="downloads from all in file"),
args = parser.parse_args()

if args.player:
    df = pd.read_csv("players_index.csv")
    player_id = df[df['PLAYER_NAME'] == args.player]['PLAYER_ID'].values
    if player_id.shape[0] == 0:
        raise SystemExit("Player %s not found in index" % args.player)

    player_id = player_id[0]
    download_season_data(player_id)
elif args.all:
    df = pd.read_csv(args.all)
    players = df[["PLAYER_NAME", "PLAYER_ID"]]
    for index, row in df.iterrows():
        print("Downloading for %s" % row['PLAYER_NAME'])
        player_id = row['PLAYER_ID']
        download_season_data(player_id)
