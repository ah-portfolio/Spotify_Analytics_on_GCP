import requests
import base64
from dotenv import load_dotenv
import os
import base64
import json
import pandas as pd
import datetime
from datetime import datetime
from google.cloud import storage



load_dotenv()


cwd = os.getcwd()
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = cwd+'/daring-card-399612-0e1ff4eca0a0.json'
refresh_t=os.getenv("refresh_t")


#GET THE NEW TOKEN THANKS TO THE REFRESH TOKEN
def get_token(a):
    load_dotenv()
    client_id=os.getenv("CLIENT_ID")
    client_secret=os.getenv("CLIENT_SECRET")
    token_url = "https://accounts.spotify.com/api/token"

    encoded_credentials = base64.b64encode(client_id.encode() + b':' + client_secret.encode()).decode("utf-8")
    headers = {
        "Authorization": "Basic " + encoded_credentials,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type": "refresh_token",
        "refresh_token":a
    }
    
    result=requests.post(token_url,headers=headers,data=data)
    json_result = json.loads(result.content)
    token = json_result.get('access_token')
    return(token)

token = get_token(refresh_t)

##GET DATA REQUEST

def get_datas():
    user_headers = {
        "Authorization": "Bearer " + str(token),
        "Content-Type": "application/json"
    }
    user_params = {
        "limit": 50
    }

    user_tracks_response = requests.get("https://api.spotify.com/v1/me/player/recently-played", params=user_params, headers=user_headers)

    datas = user_tracks_response.json()

    return(datas)

datas = get_datas()

#GET DATA FROM RESPONSE
headers = ['date_playing','hour_playing','Track_title', 'Track_Singer', 'Track_Album','Album_release_date','Track_popularity']
data=[]

print(datas['items'][int(0)]['played_at'])

for i in range (50):
    data.append( [datas['items'][int(i)]['played_at'].split('T')[0],
    datas['items'][int(i)]['played_at'].split('T')[1].split('.')[0],
    datas['items'][int(i)]['track']['name'],
    datas['items'][int(i)]['track']['artists'][int(0)]['name'],
    datas['items'][int(i)]['track']['album']['name'],
    datas['items'][int(i)]['track']['album']['release_date'],
    datas['items'][int(i)]['track']['popularity']
    ])

df = pd.DataFrame(data,columns=headers)
#print(df)


client = storage.Client()
bucket = client.get_bucket('adil_bucket_test_asa')
    
bucket.blob(f'raw_spotify/test_{datetime.today()}.csv').upload_from_string(df.to_csv(index=False,sep=';'), 'text/csv')
