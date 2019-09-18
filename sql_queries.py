import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES
drop_schema="DROP SCHEMA IF EXISTS sparkifydb;"
set_search_path="SET SEARCH_PATH to sparkifydb;"
staging_events_table_drop = "DROP TABLE IF EXISTS staging_events;"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs;"
songplay_table_drop = "DROP TABLE IF EXISTS songplay;"
user_table_drop = "DROP TABLE IF EXISTS sparkifydb.users;"
song_table_drop ="DROP TABLE IF EXISTS sparkifydb.songs;"
artist_table_drop = "DROP TABLE IF EXISTS sparkifydb.artists;"
time_table_drop = "DROP TABLE IF EXISTS sparkifydb.time;"

#CREATE SCHEMA

create_sparkify_schema="CREATE SCHEMA IF NOT EXISTS sparkifydb;"

# CREATE TABLES

staging_events_table_create= ("""
CREATE TABLE staging_events
(
event_id            int identity(0,1) SORTKEY,
artist_name         text  NULL DISTKEY,
auth                text  NULL,
firstName           text  NULL,
gender              varchar(5) NULL,
itemInSession       bigint NULL,
lastName            text NULL,
length              double precision NULL,
level               text NULL,
location            text NULL,
method              text NULL,
page                text NULL,
registration        text NULL,
sessionId           bigint NULL,
song                text NULL,
status              int NULL,
ts                  text NULL,
userAgent           text NULL,
userId              bigint   
);
""")

staging_songs_table_create = ("""
CREATE TABLE staging_songs
(
num_songs        int,
artist_id        varchar(255) DISTKEY,
artist_latitude  varchar(255) NULL,
artist_longitude varchar(255) NULL,
artist_location  varchar(255) NULL,
artist_name      text NOT NULL,
song_id          varchar(255) SORTKEY NOT NULL,
title            text NOT NULL,
duration         double precision NOT NULL,
year             int NULL
);
""")

songplay_table_create = ("""
CREATE TABLE songplay
(
songplay_id  int identity(0,1) PRIMARY KEY SORTKEY NOT NULL, 
start_time   timestamp NOT NULL, 
user_id      text NOT NULL, 
level        text, 
song_id      text NOT NULL, 
artist_id    text NOT NULL DISTKEY, 
session_id   text, 
location     text, 
user_agent   text);
""")

user_table_create = ("""
CREATE TABLE users(
user_id          bigint PRIMARY KEY SORTKEY NOT NULL ,
first_name       text,
last_name        text, 
gender           varchar(10),
level            text
)diststyle all;
""")

song_table_create = ("""
CREATE TABLE songs(
song_id          varchar(255) SORTKEY PRIMARY KEY NOT NULL,
artist_id        text NOT NULL,
year             int, 
duration         double precision,
level            text
)diststyle all;
""")

artist_table_create = ("""
CREATE TABLE artists(
artist_id        text PRIMARY KEY SORTKEY, 
artist_name      text, 
location         text, 
lattitude        text, 
longitude        text
) diststyle all;

""")

time_table_create = ("""
CREATE TABLE time(
start_time      timestamp PRIMARY KEY SORTKEY,
hour            int,
day             int,
week            int,
month           int,
year            int,
weekday         int
) diststyle all;
""")

# STAGING TABLES

staging_events_copy = ("""copy staging_events from '{}'
    credentials 'aws_iam_role={}'
    compupdate off  
    region 'us-west-2'
    JSON '{}'
""").format(config['S3']['LOG_DATA'],config['IAM_ROLE']['ARN'],config['S3']['LOG_JSONPATH'])

staging_songs_copy = ("""copy staging_songs from '{}'
    credentials 'aws_iam_role={}'
    compupdate off     
    region 'us-west-2' 
    JSON 'auto'
""").format(config['S3']['SONG_DATA'],config['IAM_ROLE']['ARN'])

# FINAL TABLES

songplay_table_insert = ("""
INSERT INTO songplay(start_time,user_id,level,song_id,artist_id,session_id,location,user_agent)

SELECT
    TIMESTAMP 'epoch' + se.ts/1000 * INTERVAL '1 Second ' AS start_time,
    se.userId           AS  user_id,
    se.level            AS  level,
    ss.song_id          AS song_id,
    ss.artist_id        AS artist_id,
    se.sessionId        AS session_id,
    ss.artist_location  AS location,
    se.userAgent       AS user_agent
FROM staging_songs AS ss 
JOIN staging_events AS se ON (ss.title=se.song AND ss.artist_name=se.artist_name)
AND
  se.page = 'NextSong';
  
""")

user_table_insert = ("""
INSERT INTO users(user_id,first_name,last_name,gender,level)

SELECT DISTINCT(s.userId)   AS user_id,
    s.firstName AS first_name,
    s.lastName  AS last_name,
    s.gender    AS gender,
    s.level    AS level

FROM
   staging_events as s
WHERE s.page = 'NextSong' 

""")

song_table_insert = ("""
INSERT INTO songs (song_id,artist_id,year, duration)

SELECT DISTINCT(ss.song_id)   AS song_id,
  ss.artist_id AS artist_id,
  ss.year      AS year,
  ss.duration  AS duration
FROM
  staging_songs AS ss

""")

artist_table_insert = ("""
INSERT INTO artists (artist_id,artist_name,location,lattitude,longitude)

SELECT DISTINCT(s.artist_id) AS artist_id,
  s.artist_name   AS artist_name,
  s.artist_location      AS location,
  s.artist_latitude      AS lattitude,
  s.artist_longitude     AS longitude
FROM
  staging_songs AS s;
""")

time_table_insert = ("""
INSERT INTO time (start_time,hour,day,week,month,year,weekday)

SELECT   DISTINCT(TIMESTAMP 'epoch' + s.ts/1000 * INTERVAL '1 Second ') AS start_time,
   EXTRACT(HOUR from start_time)                          AS hour,
   EXTRACT(DAY  from  start_time)                         AS day,
   EXTRACT(WEEK from  start_time)                         AS week,
   EXTRACT(MONTH from start_time)                         AS month,
   EXTRACT(YEAR  from start_time)                         AS year,
   EXTRACT(DOW from start_time)                           AS weekday
FROM 
   staging_events AS s
WHERE 
   s.page = 'NextSong'; 

""")

# QUERY LISTS

create_table_queries =[set_search_path,songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create,staging_events_table_create,staging_songs_table_create]

drop_table_queries = [create_sparkify_schema,set_search_path,staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]

copy_table_queries = [set_search_path,staging_events_copy, staging_songs_copy]

insert_table_queries = [set_search_path,user_table_insert, song_table_insert, artist_table_insert, time_table_insert,songplay_table_insert]
