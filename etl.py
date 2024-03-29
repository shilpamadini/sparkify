import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    
    """function processes song file and inserts data into song table and artists table."""
   
    # open song file
    df = pd.read_json(filepath,lines= True)
    
    # insert artist record
    artist_data = df[['artist_id','artist_name','artist_location','artist_latitude','artist_longitude']].values[0].tolist()
    cur.execute(artist_table_insert, artist_data)
    
    # insert song record
    song_data = df[['song_id','title','artist_id','year','duration']].values[0].tolist()
    cur.execute(song_table_insert, song_data)


def process_log_file(cur, filepath):
    
    """functions processes log file and inserts data into tables time,user and songplay."""
    
    # open log file
    df = pd.read_json(filepath,lines= True)

    # filter by NextSong action
    df = df.loc[df['page']=='NextSong']

    # convert timestamp column to datetime
    df['ts'] = df['ts'].apply(pd.to_datetime)
    t = df['ts']
    
    # retrieve time data records
    timestamp = t.values.tolist()
    hour = t.dt.hour.values.tolist()
    day = t.dt.day.values.tolist()
    week = t.dt.week.values.tolist()
    month = t.dt.month.values.tolist()
    year = t.dt.year.values.tolist()
    weekday = t.dt.weekday.values.tolist()
    
    # insert time data records
    time_data = list(zip(timestamp,hour,day,week,month,year,weekday)) 
    column_labels = ['timestamp','hour', 'day','week','month','year','weekday']
    time_df = pd.DataFrame(time_data,columns=column_labels)
    time_df['timestamp']= time_df['timestamp'].apply(pd.to_datetime)

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[['userId','firstName','lastName','gender','level']] 
    
    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)
    
    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        results = cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        if results:
            songid = results[0]
            artistid = results[1]
        else:
            songid = None
            artistid = None

        # insert songplay record
        songplay_data = [row.ts, row.level, row.userId, songid, artistid,row.sessionId, row.location, row.userAgent ]
        cur.execute(songplay_table_insert, songplay_data)

def process_data(cur, conn, filepath, func):
    
    """function passes all the files under a filepath to given function as argument and executes the given function.""" 
   
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))
        print('{} file is processed.'.format(datafile))



def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()