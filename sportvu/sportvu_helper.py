import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
from matplotlib import animation
import matplotlib.pyplot as plt
from datetime import datetime

mx = interp1d([-4.75, 42.5], [0, 47])
my = interp1d([-25, 25], [0, 50])

class GameData(object):

    def __init__(self, game_id, gd, ed, sd):
        self.game_id = game_id
        self.tracking_data = gd
        self.event_data = ed
        self.shot_data = sd

def load_game_index():
    return pd.read_csv("nba-movement-data/data/csv/index.csv")

def load_player_index():
    return pd.read_csv("players_index.csv")

def load_game_data(game_id):
    """
    Load the game data for a specified game id.

    Parameters
    ----------
        game_id : string
            The game id to load
    Returns
    ----------
        game : GameData
            GameData object containing 3 dataframes with
            tracking, event, and shot data
    """
    game_id = str(game_id)
    if len(game_id) != 10:
        game_id = "00" + str(game_id)
    gd = pd.read_csv("nba-movement-data/data/csv/%s.csv" % game_id)
    ed = pd.read_csv("nba-movement-data/data/events/%s.csv" % game_id)
    sd = pd.read_csv("nba-movement-data/data/shots/shots.csv")
    player_index = pd.read_csv("players_index.csv")

    gd = pd.merge(gd, ed[["EVENTNUM","EVENTMSGTYPE"]],
                  left_on = "event_id", right_on = "EVENTNUM",
                  how = 'left')
    gd = pd.merge(gd, player_index,
                  left_on = "player_id", right_on = "PLAYER_ID",
                  how = 'left')
    sd = sd[sd["GAME_ID"] == int(game_id)]

    # Convert shot map coordinates to court coordinates
    htm_id,vtm_id = gd[gd["event_id"] == 1]["team_id"].unique()[1:]

    def map_coordinates(shot):

        x_loc_copy = shot["LOC_X"]
        y_loc_copy = shot["LOC_Y"]

        if y_loc_copy > 425:
            y_loc_copy = 425
        if y_loc_copy < -47.5:
            y_loc_copy = -47.5

        shot["LOC_X"] = mx(y_loc_copy/10)
        shot["LOC_Y"] = my(x_loc_copy/10)
        period = shot["PERIOD"]
        if shot["TEAM_ID"] == htm_id:
            if period == 3 or period == 4:
                shot["LOC_X"] = 94 - shot["LOC_X"]
        else:
            if period == 1 or period == 2:
                shot["LOC_X"] = 94 - shot["LOC_X"]
        return shot

    sd = sd.apply(map_coordinates, axis = 1)

    # Convert event times to shot clock time

    def convert_time(event):
        time_object = datetime.strptime(event["PCTIMESTRING"],"%M:%S")
        event['game_clock'] = time_object.minute * 60 + time_object.second
        return event

    ed = ed.apply(convert_time, axis = 1)

    return GameData(game_id, gd, ed, sd)

def render_play(game_data, event_id):
    """
    Create an animation of the given event id.

    Parameters
    ----------
    game_data : GameData
        GameData object with full tracking data of the game
    event_id : string
        Event id of the event to render

    Returns
    ----------
    ani : matplotlib.animation
        Animation of the event
    """

    fig, ax = plt.subplots()

    tracking = game_data.tracking_data
    event = tracking[tracking['event_id'] == event_id]
    team_a, team_b = event['team_id'].unique()[1:]
    
    total_frames = int(event.shape[0]/11)

    particles_a, = ax.plot([], [], marker = 'o', linestyle = 'None', color = 'b')
    particles_b, = ax.plot([], [], marker = 'x', linestyle = 'None', color = 'r')
    particles_ball, = ax.plot([], [], marker = 'o', linestyle = 'None', color = 'orange')
    text = ax.text(38, 46, "")

    ax.set_xlim([0, 94])
    ax.set_ylim([0, 50])

    def animate(i):
        snapshot = event.iloc[i * 11: (i+1) * 11,:]
        ball_pos = snapshot[snapshot['team_id'] == -1][['x_loc', 'y_loc']].values
        team_a_pos = snapshot[snapshot['team_id'] == team_a][['x_loc', 'y_loc']].values
        team_b_pos = snapshot[snapshot['team_id'] == team_b][['x_loc', 'y_loc']].values

        particles_a.set_data(team_a_pos[:,0], team_a_pos[:,1])
        particles_a.set_markersize(6)

        particles_b.set_data(team_b_pos[:,0], team_b_pos[:,1])
        particles_b.set_markersize(6)

        particles_ball.set_data(ball_pos[:,0], ball_pos[:,1])
        particles_ball.set_markersize(6)

        text.set_text(str(snapshot['game_clock'].values[0]))

        return particles_a, particles_b, particles_ball, text,

    ani = animation.FuncAnimation(fig, animate, frames = total_frames, interval = 25, blit = True)
    return ani
