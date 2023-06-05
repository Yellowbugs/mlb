import statsapi
import json
import requests
from oddsapi import OddsApiClient
teamIds = {
    'Los Angeles Angels': 108,
    'Arizona Diamondbacks':109,
    'Baltimore Orioles': 110,
    'Boston Red Sox	': 111,
    'Chicago Cubs': 112,
    'Cincinnati Reds': 113,
    'Cleveland Guardians': 114,
    'Colorado Rockies': 115,
    'Detroit Tigers': 116,
    'Houston Astros': 117,
    'Kansas City Royals': 118,
    'Los Angeles Dodgers': 119,
    'Washington Nationals': 120,
    'New York Mets': 121,
    'Oakland Athletics': 133,
    'Pittsburgh Pirates': 134,
    'San Diego Padres': 135,
    'Seattle Mariners': 136,
    'San Francisco Giants': 137,
    'St. Louis Cardinals': 138,
    'Tampa Bay Rays': 139,
    'Texas Rangers': 140,
    'Toronto Blue Jays': 141,
    'Minnesota Twins': 142,
    'Philadelphia Phillies': 143,
    'Atlanta Braves': 144,
    'Chicago White Sox': 145,
    'Miami Marlins': 146,
    'New York Yankees': 147,
    'Milwaukee Brewers': 158,

}

client = OddsApiClient(api_key='b664d59f43cfee882082f8fb86a1c478')
odds_response = requests.get('https://api.the-odds-api.com/v3/odds', params={
    'api_key': 'b664d59f43cfee882082f8fb86a1c478',
    'sport': 'baseball_mlb',
    'region': 'us', # uk | us | eu | au
    'oddsFormat': 'american',
    "mkt": "totals",
    "bookmakers": [
        {
        "key": "draftkings",
        "title": "DraftKings",    
  
    }]
})
odds_json = json.loads(odds_response.text)
print(odds_json['data'])
print("odds:")
for x in range(len(odds_json['data'])):
    print(odds_json['data'][x]['teams'])
    print(odds_json['data'][x]['sites'][0]['odds']['totals']['points'][0])


print("projections:")
g = statsapi.schedule(date='06/06/2023')

for i in g:
    gameCount = 0
    totalRuns = 0
    print(i['home_name'])
    teamId = teamIds[str(i['home_name'])]
    #print(teamId)
    games = statsapi.schedule(start_date='06/01/2023',end_date='06/05/2023',team=teamId)
    for x in games:
        if x['status'] == 'Final':
            gameCount = gameCount + 1
            #print(x['summary'])
            #print(x['home_score'] + x['away_score'])
            totalRuns = totalRuns + x['home_score'] + x['away_score']
    print(totalRuns/gameCount)