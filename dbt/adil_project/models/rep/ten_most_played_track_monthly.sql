
-- Use the `ref` function to select from other models

-- SELECT
-- FORMAT_DATETIME("%E4Y", DATETIME( `date`)) as periode , SUM(stock) as stock , SUM(debit) as debit 	
-- FROM  {{ ref('list_of_track') }}
-- group by FORMAT_DATETIME("%E4Y", DATETIME( `date`))

WITH
most_played_track_table
as
(
select 
EXTRACT(MONTH FROM date_time)||'/'||EXTRACT(YEAR FROM date_time) as month_year,track_title as most_played_track,count(*)  as number_of_time
FROM {{ ref('list_of_track') }}
group by 1,2 
order by 3 desc
limit 10)

select 
distinct
mpt.month_year,
mpt.number_of_time,
mpt.most_played_track,
lot.Track_Singer as singer,				
lot.Track_Album as album,					
lot.Album_release_date as album_release_date ,			
lot.Track_popularity as popularity
FROM most_played_track_table mpt
JOIN {{ ref('list_of_track') }} lot ON mpt.most_played_track=lot.Track_title 


