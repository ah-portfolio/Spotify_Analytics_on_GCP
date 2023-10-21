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
print(df)


client = storage.Client()
bucket = client.get_bucket('adil_bucket_test_asa')
    
bucket.blob(f'raw_spotify/test_{datetime.today()}.csv').upload_from_string(df.to_csv(index=False,sep=';'), 'text/csv')


# # current date and time plus one hour due to time zone difference

# df["played_at"] = pd.to_datetime(df['date_playing'] + ' ' + df['hour_playing'])

# df["played_at"] = df["played_at"] + timedelta(hours=1, minutes=0) 


# #transform date_playing into date format


# #Filter on last 60 minute datas
# deltaTime = datetime.today() - timedelta(hours=1, minutes=0)
# df = df.loc[(df['played_at'] >= deltaTime)]

# df = df.drop('played_at', axis=1)
            

##UPLOAD REFINE DATA ON S3
#date_of_upload = datetime.now()
# region_name=os.getenv("region_name")
# aws_access_key_id=os.getenv("aws_access_key_id")
# aws_secret_access_key=os.getenv("aws_secret_access_key")


# s3_bucket = 'spotify-analytics'
# s3_client = boto3.client("s3",
#                   region_name=region_name,
#                   aws_access_key_id=aws_access_key_id,
#                   aws_secret_access_key=aws_secret_access_key)

# with io.StringIO() as csv_buffer:
#     df.to_csv(csv_buffer, index=False)

#     response = s3_client.put_object(
#         Bucket=s3_bucket, Key=f"data{date_of_upload}.csv", Body=csv_buffer.getvalue()
#     )


# azure_storage_account_key=os.getenv("azure_storage_account_key")
# azure_storage_account_name=os.getenv("azure_storage_account_name")
# azure_connection_string=os.getenv("azure_connection_string")


# ## Create archive of previous data
# # Source

# def archiveToBlobStorage(source_container_name,source_file_path,target_container_name,target_file_path):
#     blob_service_client = BlobServiceClient.from_connection_string(azure_connection_string)
#     source_blob = (f"https://{azure_storage_account_name}.blob.core.windows.net/{source_container_name}/{source_file_path}")
#     copied_blob = blob_service_client.get_blob_client(target_container_name, target_file_path)
#     copied_blob.start_copy_from_url(source_blob)
#     remove_blob = blob_service_client.get_blob_client(source_container_name, source_file_path)
#     remove_blob.delete_blob()


# last_data_upload = datetime.today()
# archiveToBlobStorage("test1","data.csv","archive",f"data{last_data_upload}.csv")


# ##UPLOAD REFINE DATA ON BLOB
# data_output = io.StringIO()
# data_output = df.to_csv (index=False, encoding = "utf-8",sep=';')


# def uploadToBlobStorage(file_name,df,container_name):
#    blob_service_client = BlobServiceClient.from_connection_string(azure_connection_string)
#    blob_client = blob_service_client.get_blob_client(container=container_name, blob=file_name)
#    blob_client.upload_blob(df,overwrite=True)


# uploadToBlobStorage('data.csv',data_output,'test1')