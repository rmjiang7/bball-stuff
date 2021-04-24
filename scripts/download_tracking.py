import time
import pathlib

from api_helper import Client
from endpoints import TrackingEndpoint

pathlib.Path("../data/pt_data").mkdir(exist_ok=True)

# Download each measure type, for each season
PtMeasureTypes = ['Drives', 'Defense', 'CatchShoot',
                  'Passing', 'Possessions', 'PullUpShot',
                  'Rebounding', 'Efficiency', 'SpeedDistance',
                  'ElbowTouch', 'PostTouch', 'PaintTouch']
Seasons = ['2013-14', '2014-15', '2015-16',
           '2016-17', '2017-18', '2018-19']
SeasonType = ['Regular Season']

client = Client()
for pt in PtMeasureTypes:
    for season in Seasons:
        time.sleep(5)
        print("%s - %s" % (season, pt))
        e = TrackingEndpoint(pt, season)
        df = client.make_request(e)
        df.to_csv('../data/pt_data/%s_%s.csv' %
                  (season, pt), sep=',', index=False)
