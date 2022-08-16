import requests
import os

headers = {
    'Authorization': os.environ['OAUTH'],
    'Client-Id': os.environ['CLIENT_ID']
}

def get_user(user):
    params = {'login': user}
    return requests.get('https://api.twitch.tv/helix/users',
                        headers=headers,
                        params=params).json()['data'][0]
