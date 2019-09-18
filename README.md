# Project3-Data-Warehouse-Amazon-Redshift
Data Engineering Nano Degree

# Project Idea:

Sparkify is the music straming app , they have their data residing on Amazon S3. It has JSON logs which has events ### genrated as a part of user activites on app and song metadata of the songs in their app.

Project goals are,

   1. Extracting the data from S3.
   2. Staging the data on database residing on RedShift cluster.
   3. Transoform  data to dimensional and facts table.

These tables will then in turn used by analytics team in finding insights about songs users are listening to from their ### app and get the statistics about the usage.


# Project Instructions:

## 1. Launch Redshift cluster:
Use the redshift_cluster_config.ipynb script to create the I AM Role and redshift cluster on AWS cloud.
This script will use the config file dwh_cluster.cfg , which will be parsed in order to get the configuration information to set up cluster.

***** dwh_cluster.cfg *****

  ##### [AWS]
  ##### KEY=
  ##### SECRET=

  ##### [DWH] 
  ##### DWH_CLUSTER_TYPE=multi-node
  ##### DWH_NUM_NODES=4
  ##### DWH_NODE_TYPE=dc2.large
  ##### DWH_IAM_ROLE_NAME=
  ##### DWH_CLUSTER_IDENTIFIER=
  ##### DWH_DB=sparkify
  ##### DWH_DB_USER=
  ##### DWH_DB_PASSWORD=
  ##### DWH_PORT=5439
******************************

## 2. Run the create_table.py script:
This script uses configuartion file dwh.cfg which has configuration required to access redshift cluster which was obtained from previous step. 

***** dwh.cfg *****

##### [CLUSTER]
##### HOST=host
##### DB_USER=user
##### DB_PASSWORD=password
##### DB_PORT=5439

##### [IAM_ROLE]
##### ARN= Role

##### [S3]
##### LOG_DATA=s3://udacity-dend/log_data
##### LOG_JSONPATH=s3://udacity-dend/log_json_path.json
##### SONG_DATA=s3://udacity-dend/song_data/
##### SONG_SINGLE=s3://udacity-dend/song_data/A/A/
*******************
  1. Create the sparkifydb schema if does not exit.
  2. Drop the existing tables from schema.
  3. Create tables,
      ##### staging_events
      ##### staging_songs
      ##### songs
      ##### users
      ##### artists
      ##### songplay
    
## 3. Run the etl.py script:

This script will be used to,
  1. Load staging tables staging_event and staging_songs by copying the log data  and song_data from
     S3 object.
  2. Insert data into dimensional tables and fact tables.

## 4. Run the sampleQueries.ipnyb:

Run the analytical queries from sampleQueries.ipnyb to check if the tables are as per expectaions from analytics team.


# Schema Design

Facts tables and dimension tables has been created by using the staging tables staging_events and staging_songs.
staging_events and staging_songs table are created using the song and event datasets from Udacity's S3 buckets.

Below are the fact and dimensions tables created.

Fact Table
  songplays - It has records in event data associated with song plays i.e. records with page NextSong
    songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent. This table

Dimension Tables
  users - users in the app
    user_id, first_name, last_name, gender, level

  songs - songs in music database
    song_id, title, artist_id, year, duration
    
  artists - artists in music database
    artist_id, name, location, lattitude, longitude
    
  time - timestamps of records in songplays broken down into specific units
    start_time, hour, day, week, month, year, weekday
    
# Project Template
Udacity has provided project templates to work on,

 1. create_table.py is where you'll create your fact and dimension tables for the star schema in Redshift.
 2. etl.py is where you'll load data from S3 into staging tables on Redshift and then process that data into your analytics     tables on Redshift.
 3. sql_queries.py is where you'll define you SQL statements, which will be imported into the two other files above.
 4. README.md is where you'll provide discussion on your process and decisions for this ETL pipeline.

 
# ETL Pipeline:
   1. All the tables has been created with proper fields and datatypes before performing tranformation and load.

   2. Sparkify dataset is present in form of JSON directories which has two types of data log data and song data.Log data is the  information about user activity obtained from app and song data has metadata of the all songs in app.These directories resides on S3. This data is extracted from S3 to staging tables on redshift cluster by using sortkeys distkeys in order to make optimal use of cluster nodes.
    
  3. Now data obtained from staging_tables is transformed into fact and dimension tables by performing INSERT statements.
  
  4. Few analytical queries are run to verify if data is loaded properly inside tables.
  
 
  
     
    
    
   
