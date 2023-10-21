
/*
    Welcome to your first dbt model!
    Did you know that you can also configure models directly within SQL files?
    This will override configurations stated in dbt_project.yml

    Try changing "table" to "view" below
*/

{{ config(materialized='table') }}


SELECT distinct 
DATETIME(TIMESTAMP(date_playing||' '||hour_playing), 'Europe/Paris') as date_time,
Track_title	,			
Track_Singer,				
Track_Album,					
Album_release_date,			
Track_popularity
FROM  {{ source('dbt_raw_spotify', 'data_from_api') }}

/*
    Uncomment the line below to remove records with null `id` values
*/

-- where id is not null
