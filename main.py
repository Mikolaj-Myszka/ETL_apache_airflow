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
TOKEN = "BQDqoUXlWpAuMuWfmHplEWZVivl8TMG3uSiHHtQIeAZtJL931hmDMuFN9SfTd-EVpHB4zcDmKf61gN-o4iKsswkzu3tCR7LCySVZXIlh1dEpy2CflbqqKzEUoSVk_3MR3XN7BpcY7Zufzg"



### Validation function
def check_if_data_is_valid(df: pd.Dataframe) -> bool:
    # Check if dataframe is empty
    if df.empty:
        print("No genres downloaded. Finishing execution")
        return False
    
    # Primary Key Check
    if pd.Series(df['genre']).is_unique:
        pass
    else:
        raise Exception("Primary Key check is violated")


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



