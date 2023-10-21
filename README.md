# Spotify_Analytics_on_GCP

## Google Cloud Composer : Airflow 

Composer run kubernetes pods to execute the tasks.
  ### Workload identity :


One airflow dag runs two tasks :
![image](https://github.com/ah-portfolio/Spotify_Analytics_on_GCP/assets/110063004/de4a959d-0c71-4449-acf2-a7c0dece0b42)


## Google Kubernetes Engine :

Pods run thanks to images which are stored in Artifact Registry (on GCP). Here commands to build and push docker image on the registry :

docker build . -f dbt/Dockerfile -t us-central1-docker.pkg.dev/daring-card-399612/docker-aho/image_dbt

docker tag us-central1-docker.pkg.dev/daring-card-399612/docker-aho/image_dbt \
    us-central1-docker.pkg.dev/daring-card-399612/docker-aho/image_dbt:#VERSION#

docker push us-central1-docker.pkg.dev/daring-card-399612/docker-aho/image_dbt:#VERSION#
