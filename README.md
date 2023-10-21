# Spotify_Analytics_on_GCP

## Google Cloud Composer : Airflow 

Composer run kubernetes pods to execute the tasks.
  ### Workload identity configuration :

To make composer able to run pods, GCP advises to use Workload identity to make composer to launch pods.


  ### DAG
A unique airflow dag runs two tasks scheduled each hour:
![image](https://github.com/ah-portfolio/Spotify_Analytics_on_GCP/assets/110063004/de4a959d-0c71-4449-acf2-a7c0dece0b42)

#### Data extraction

Data extraction from Spotify API of the last 50 played track of the user. Data is stored on GCS on this path adil_bucket_test_asa/raw_spotify/
Extraction are stored on CSV, for bigger extracts other file format can be usefull (Parquet, Avro, ...)

Authentification to upload file on GCS is done by env variable => it is not ideal for non-production environments, it can be optimized thanks to oauth authentification.

#### Dbt run

The second task run 2 models on Big Query. 
  dbt_staging_spotify dataset :  table: list_of_track -> all the track played without duplicate caused by the extraction. Paris timezone because Spotify API date/time are in UTC. 
  ![image](https://github.com/ah-portfolio/Spotify_Analytics_on_GCP/assets/110063004/382b234a-72ec-414e-947c-bd469a8e528f)

  dbt_rep_spotify dataset : table: ten_most_played_track_monthly -> ten most played track agregated by month.
![image](https://github.com/ah-portfolio/Spotify_Analytics_on_GCP/assets/110063004/f825ccae-34ca-480c-b360-1a86ec84f675)

Authentification between the pod which runs dbt and big query is oauth based authentification.


## Google Kubernetes Engine :

Pods run thanks to images which are stored in Artifact Registry (on GCP). Here commands to build the containers (dbt container & api extraction container):
#### Build 
    docker build . -f dbt/Dockerfile -t us-central1-docker.pkg.dev/daring-card-399612/docker-aho/image_dbt
#### Tag    
    docker tag us-central1-docker.pkg.dev/daring-card-399612/docker-aho/image_dbt \
        us-central1-docker.pkg.dev/daring-card-399612/docker-aho/image_dbt:#VERSION#
#### Push to Artifact registry
    docker push us-central1-docker.pkg.dev/daring-card-399612/docker-aho/image_dbt:#VERSION#

