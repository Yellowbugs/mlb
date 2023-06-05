import statsapi
import json
import requests
import datetime
from datetime import timedelta, date
import re
from oddsapi import OddsApiClient
teamIds = {
    'Los Angeles Angels': 108,
    'Arizona Diamondbacks':109,
    'Baltimore Orioles': 110,
    'Boston Red Sox': 111,
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
projections = {}

client = OddsApiClient(api_key='b664d59f43cfee882082f8fb86a1c478')

def simulateday(date,today,datex, startdate):
    for i in today:
        gameCount = 0
        totalRuns = 0
        teamId = teamIds[str(i['home_name'])]
        games = statsapi.schedule(start_date=startdate,end_date= datex,team=teamId)
        for x in games:
            if x['status'] == 'Final':
                gameCount = gameCount + 1
                #print(x['summary'])
                #print(x['home_score'] + x['away_score'])
                totalRuns = totalRuns + x['home_score'] + x['away_score']
        prediction = totalRuns/gameCount
        projections.update({i['home_name']: prediction})

    for i in today:
        gameCount = 0
        totalRuns = 0
        teamId = teamIds[str(i['away_name'])]
        games = statsapi.schedule(start_date=startdate,end_date= datex,team=teamId)
        for x in games:
            if x['status'] == 'Final':
                gameCount = gameCount + 1
                #print(x['summary'])
                #print(x['home_score'] + x['away_score'])
                totalRuns = totalRuns + x['home_score'] + x['away_score']
        prediction = totalRuns/gameCount
        projections.update({i['away_name']: prediction})
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
    print('date: ', datex)
    odds_json = json.loads(odds_response.text)
    for x in range(len(odds_json['data'])):
        dt = datetime.datetime.fromtimestamp(odds_json['data'][x]['commence_time'])
        iso_format = dt.isoformat()
        if iso_format[:10] == date:
            print("game: " , odds_json['data'][x]['teams'])
            odds = odds_json['data'][x]['sites'][0]['odds']['totals']['points'][0]
            print("odds: " , odds)
            projectedTotal = (projections[str(odds_json['data'][x]['teams'][0])]+projections[str(odds_json['data'][x]['teams'][1])])/2
            print("projected total: " , projectedTotal)
            if projectedTotal <= odds:
                play = "under"
            else:
                play = "over"
            print("play: ", play)
            

userChoice = input("today(1) or tomorrow(2)?")
if userChoice == '2':
    today = date.today() + timedelta(days=1)
else:
    today = date.today()  
datex = re.sub(r'(\d{4})-(\d{1,2})-(\d{1,2})', '\\2/\\3/\\1', str(today))
n_days_ago = re.sub(r'(\d{4})-(\d{1,2})-(\d{1,2})', '\\2/\\3/\\1', str(today - timedelta(days=10)))
#print(today)
#print(datex, n_days_ago)
simulateday(str(today),statsapi.schedule(date=str(today)), datex, n_days_ago)
