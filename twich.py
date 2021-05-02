import requests

# URL = 'https://api.twitch.tv/helix/search/channels?query=sanninshow_3ns'
URL = 'https://api.twitch.tv/helix/channels?broadcaster_id=sakuramiko_hololive'
# URL = 'https://api.twitch.tv/kraken/streams/sanninshow_3ns'
authURL = 'https://id.twitch.tv/oauth2/token'
Client_ID = 'dfgvcsi22xnzq1t9c2dpmekadihy4l'
Secret  = '9yg5fc0iz3wytriy2qfm09ajx0e7eo'

AutParams = {'client_id': Client_ID,
            'client_secret': Secret,
            'grant_type': 'client_credentials'
            }


def Check():
    AutCall = requests.post(url=authURL, params=AutParams) 
    access_token = AutCall.json()['access_token']

    head = {
    'Client-ID' : Client_ID,
    'Authorization' :  "Bearer " + access_token
    }

    # r = requests.get(URL, headers = head)
    r = requests.get(URL, headers = head).json()['data']

    if r:
        r = r[0]
        if r['type'] == 'live':
            return True
        else:
            return False
    else:
        return False

print(Check())