# Spotify_Analytics_on_GCP

## Google Kubernetes Engine :

Pods run thanks to images which are stored in Artifact Registry (on GCP). Here commands to build the containers (dbt container & api extraction container):
#### Build 
    docker build . -f dbt/Dockerfile -t us-central1-docker.pkg.dev/daring-card-399612/docker-aho/image_dbt
#### Tag    
    docker tag us-central1-docker.pkg.dev/daring-card-399612/docker-aho/image_dbt \
        us-central1-docker.pkg.dev/daring-card-399612/docker-aho/image_dbt:#VERSION#
#### Push to Artifact registry
    docker push us-central1-docker.pkg.dev/daring-card-399612/docker-aho/image_dbt:#VERSION#


## Google Cloud Composer : Airflow 

Composer runs kubernetes pods to execute the two tasks.
  ### Workload identity configuration :

To make composer able to run pods, GCP advises to use Workload identity to make composer to launch pods:



  ### DAG
A unique airflow dag runs two tasks scheduled each hour:
![image](https://github.com/ah-portfolio/Spotify_Analytics_on_GCP/assets/110063004/de4a959d-0c71-4449-acf2-a7c0dece0b42)

#### Data extraction

Data extraction from Spotify API of the last 50 played track of the user. Data is stored on GCS on this path adil_bucket_test_asa/raw_spotify/

A dataset dbt_raw_spotify is created with one external table. In this way we can query csv files on big query.

Extraction are stored on CSV, for bigger extracts other file format can be usefull (Parquet, Avro, ...)

The data extraction run on a pod.

Authentification to upload file on GCS is done by env variable => it is not ideal for non-production environments, it can be optimized thanks to oauth authentification.

#### Dbt run

The second task runs two models on Big Query to transform our data on two different layers/datasets 
  ##### dbt_staging_spotify dataset :  table: list_of_track 
  
  -> all the track played without duplicate caused by the extraction & date_time at Paris timezone because Spotify API date/time is in UTC. 
  
  ![image](https://github.com/ah-portfolio/Spotify_Analytics_on_GCP/assets/110063004/382b234a-72ec-414e-947c-bd469a8e528f)

  ##### dbt_rep_spotify dataset : table: ten_most_played_track_monthly
  
  -> ten most played track agregated by month.
  
![image](https://github.com/ah-portfolio/Spotify_Analytics_on_GCP/assets/110063004/f825ccae-34ca-480c-b360-1a86ec84f675)


Authentification between pods which run dbt and big query is oauth based authentification. (Token exchange between service account)
