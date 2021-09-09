import sqlalchemy
import pandas as pd
from sqlalchemy.orm import sessionmaker
import requests
import json
from datetime import datetime
import datetime
import sqlite3


DATABASE_LOCATION = "sqlite://my_played_tracks.sqlite" # call it whatever we like
USER_ID = "miko_zit"
TOKEN = "BQC6iD6MTevzXVlk0SIZbZBdzZta_20yUqznBR75finA1zV6a-FuJkb9D186KHe7OYEKVSRHAm5nkCtF42LTCo3udzMm-N9idjvLUyf4w1Ce0Ryz_2O9__gL5LBZ_wXIIB2kmD6ME80feA"



### Validation function
def check_if_data_is_valid(df: pd.DataFrame) -> bool:
    # Check if dataframe is empty
    if df.empty:
        print("No genres downloaded. Finishing execution.")
        return False
    
    # Primary Key Check
    if pd.Series(df['genres']).is_unique:
        pass
    else:
        raise Exception("Primary Key check is violated.")
    
    # Check for nulls
    if df.isnull().values.any():
        raise Exception("Null values found.")

    return True


if __name__ == "__main__":

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer {token}".format(token=TOKEN)
    }

    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1)
    yesterday_unix_timestamp = int(yesterday.timestamp())*1000 # in unix miliseconds

    print('today', today)
    print('timedelta', datetime.timedelta(days=1))
    print('yesterday', yesterday)
    print('timestamp', yesterday.timestamp())
    print('yesterday_unix_timestamp', yesterday_unix_timestamp)

    
    # ### Recently played version
    # r = requests.get("https://api.spotify.com/v1/me/player/recently-played/after={time}".format(time=yesterday_unix_timestamp), 
    # headers=headers)
    # r.raise_for_status()
    # data = r.json()
    # print(data)


    ### Available genre seeds
    r = requests.get("https://api.spotify.com/v1/recommendations/available-genre-seeds", headers=headers)
    data = r.json()
    print(data)


    ### Loading into df
    genres_dict = {
        'genres': data['genres']
    }

    genres_df = pd.DataFrame(genres_dict)
    print(genres_df)


    # Validate
    if check_if_data_is_valid(genres_df):
        print("Data valid, proceed to Load stage")
    

    # Load
    engine = sqlalchemy.create_engine(DATABASE_LOCATION)
    conn = sqlite3.connect('my_played_tracks.sqlite')
    cursor = conn.cursor()

    sql_query = """
    CREATE TABLE IF NOT EXIST my_played_tracks(
        genres VARCHAR(200),
        CONSTRAINT primary_key_constraint PRIMARY KEY (genres)
    )
    """

    cursor.execute(sql_query)
    print("Opened database successfully")

    try:
        genres_df.to_sql("my_played_tracks", engine, index=False, if_exists='append')
    except:
        print("Data already exists in the database")

    conn.close()
    print("Closed database successfully")


