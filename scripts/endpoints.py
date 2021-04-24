import api_helper
import pandas as pd

class ShotMapEndpoint(api_helper.Endpoint):

    base_url = 'https://stats.nba.com/stats/shotchartdetail'

    def __init__(self, player_id, season):
        self.PlayerID = player_id
        self.CFPARAMS = season
        self.Season = season

        # default params
        self.AheadBehind = ''
        self.CFID = ''
        self.ClutchTime = ''
        self.Conference = ''
        self.ContextFilter = ''
        self.ContextMeasure = 'FG_PCT'  # FG3A FG2A FG_PCT
        self.DateFrom = ''
        self.DateTo = ''
        self.Division = ''
        self.EndPeriod = 10  # ?
        self.EndRange = 28800  # ?
        self.GROUP_ID = ''
        self.GameEventID = ''
        self.GameID = ''
        self.GameSegment = ''
        self.GroupID = ''
        self.GroupQuantity = 5  # ?
        self.LastNGames = 0
        self.LeagueID = '00'
        self.Location = ''
        self.Month = 0
        self.OnOff = ''
        self.OpponentTeamID = 0
        self.Outcome = ''
        self.PORound = 0
        self.Period = 0
        self.PlayerID1 = ''
        self.PlayerID2 = ''
        self.PlayerID3 = ''
        self.PlayerID4 = ''
        self.PlayerID5 = ''
        self.PlayerPosition = ''
        self.PointDiff = ''
        self.Position = ''
        self.angeType = 0
        self.RookieYear = ''
        self.SeasonSegment = ''
        self.SeasonType = 'Regular Season'
        self.ShotClockRange = ''
        self.StatPeriod = 1
        self.StatRange = 0
        self.StarterBench = ''
        self.TeamID = 0
        self.VsConference = ''
        self.VsDivision = ''
        self.VsPlayerID1 = ''
        self.VsPlayerID2 = ''
        self.VsPlayerID3 = ''
        self.VsPlayerID4 = ''
        self.VsPlayerID5 = ''
        self.VsTeamID = ''

    def build_request(self):
        return self.base_url, vars(self)

    def format_response(self, json_response):
        return pd.DataFrame(json_response['resultSets'][0]['rowSet'],
                            columns=json_response['resultSets'][0]['headers'])


class TrackingEndpoint(api_helper.Endpoint):

    base_url = 'https://stats.nba.com/stats/leaguedashptstats'

    def __init__(self, pt_measure_type, season):
        self.PtMeasureType = pt_measure_type
        self.Season = season

        self.College = ''
        self.Conference = ''
        self.Country = ''
        self.DateFrom = ''
        self.DateTo = ''
        self.Division = ''
        self.DraftPick = ''
        self.DraftYear = ''
        self.GameScope = ''
        self.Height = ''
        self.LastNGames = 0
        self.LeagueID = '00'
        self.Location = ''
        self.Month = 0
        self.OpponentTeamID = 0
        self.Outcome = ''
        self.PORound = 0
        self.PerMode = 'PerGame'
        self.PlayerExperience = ''
        self.PlayerOrTeam = 'Player'
        self.PlayerPosition = ''
        self.SeasonSegment = ''
        self.SeasonType = 'Regular Season'
        self.StarterBench = ''
        self.TeamID = 0
        self.VsConference = ''
        self.VsDivision = ''
        self.Weight = ''

    def build_request(self):
        return self.base_url, vars(self)

    def format_response(self, json_response):
        return pd.DataFrame(json_response['resultSets'][0]['rowSet'],
                            columns=json_response['resultSets'][0]['headers'])

class TeamTrackingEndpoint(api_helper.Endpoint):

    base_url = 'https://stats.nba.com/stats/leaguedashptstats'

    def __init__(self, pt_measure_type, season, month):
        self.PtMeasureType = pt_measure_type
        self.Season = season
        self.Month = month

        self.College = ''
        self.Conference = ''
        self.Country = ''
        self.DateFrom = ''
        self.DateTo = ''
        self.Division = ''
        self.DraftPick = ''
        self.DraftYear = ''
        self.GameScope = ''
        self.Height = ''
        self.LastNGames = 0
        self.LeagueID = '00'
        self.Location = ''
        self.OpponentTeamID = 0
        self.Outcome = ''
        self.PORound = 0
        self.PerMode = 'PerGame'
        self.PlayerExperience = ''
        self.PlayerOrTeam = 'Team'
        self.PlayerPosition = ''
        self.SeasonSegment = ''
        self.SeasonType = 'Regular Season'
        self.StarterBench = ''
        self.TeamID = 0
        self.VsConference = ''
        self.VsDivision = ''
        self.Weight = ''

    def build_request(self):
        return self.base_url, vars(self)

    def format_response(self, json_response):
        return pd.DataFrame(json_response['resultSets'][0]['rowSet'],
                            columns=json_response['resultSets'][0]['headers'])
    
class BoxScoreAdvanced(api_helper.Endpoint):

    base_url = 'https://stats.nba.com/stats/boxscoreadvancedv2'

    def __init__(self, gameId, 
                 startPeriod = 0, endPeriod = 14,
                 startRange = 0, endRange = 2147483647):
        self.GameId = gameId
        self.StartPeriod = startPeriod
        self.EndPeriod = endPeriod
        self.StartRange = startRange
        self.EndRange = endRange
        self.RangeType = 2

    def build_request(self):
        return self.base_url, vars(self)

    def format_response(self, json_response):
        return pd.DataFrame(json_response['resultSets'][0]['rowSet'],
                            columns=json_response['resultSets'][0]['headers'])
    
class BoxScoreTraditional(api_helper.Endpoint):

    base_url = 'https://stats.nba.com/stats/boxscoretraditionalv2'

    def __init__(self, gameId, 
                 startPeriod = 0, endPeriod = 14,
                 startRange = 0, endRange = 2147483647):
        self.GameId = gameId
        self.StartPeriod = startPeriod
        self.EndPeriod = endPeriod
        self.StartRange = startRange
        self.EndRange = endRange
        self.RangeType = 2

    def build_request(self):
        return self.base_url, vars(self)

    def format_response(self, json_response):
        return pd.DataFrame(json_response['resultSets'][1]['rowSet'],
                            columns=json_response['resultSets'][1]['headers'])
    
class PlayByPlay(api_helper.Endpoint):

    base_url = 'https://stats.nba.com/stats/playbyplayv2'

    def __init__(self, gameId, 
                 startPeriod = 0, endPeriod = 14):
        self.GameId = gameId
        self.StartPeriod = startPeriod
        self.EndPeriod = endPeriod

    def build_request(self):
        return self.base_url, vars(self)

    def format_response(self, json_response):
        return pd.DataFrame(json_response['resultSets'][0]['rowSet'],
                            columns=json_response['resultSets'][0]['headers'])

class BoxScoreSummary(api_helper.Endpoint):
    
    base_url = 'https://stats.nba.com/stats/boxscoresummaryv2'
    
    def __init__(self, gameId):
        self.GameId = gameId
        
    def build_request(self):
        return self.base_url, vars(self)
    
    def format_response(self, json_response):
        return pd.DataFrame(json_response['resultSets'][0]['rowSet'],
                            columns=json_response['resultSets'][0]['headers'])
    

if __name__ == '__main__':
    e = ShotMapEndpoint("203932", "2019-20")
    url, params = e.build_request()
    print(url)
    print(params)
