import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import re
import pandas as pd
import datetime
import streamlit as st

class LoadPLaylist():
    def __init__(_self,plink, client_id, client_secret):
        _self.plink = plink
        _self.client_id = client_id
        _self.client_secret = client_secret

        _self.sp = _self.create_spotipy_instance()
       


    def create_spotipy_instance(_self):
        client_credentials_manager = SpotifyClientCredentials(
            client_id=_self.client_id, client_secret=_self.client_secret
        )
        return spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    
    def generate_playlist_df(_self):

        playlist_id = _self.extract_playlist_id(_self.plink)
        playlist = _self.sp.playlist(playlist_id)

        total_tracks = playlist['tracks']['total']

        limit = 100 
        offset = 0

        final_data = []
        
        while offset < total_tracks:
            
            tracks = _self.sp.playlist_tracks(playlist_id, offset=offset, limit=limit)

            for i in tracks['items']:
                if i['track'] is not None:
                    artist_uri = i["track"]["artists"][0]["uri"]
                    artist_info = _self.sp.artist(artist_uri)
                    artist_name = i["track"]["artists"][0]["name"]
                    artist_pop = artist_info["popularity"]
                    artist_genres = artist_info["genres"]
                    features = _self.sp.audio_features(i['track']['uri'])

                    data_pos = [
                    i['track']['uri'],i['track']['name'], i["track"]["popularity"], i['added_at'].split('T')[0],
                    artist_name, artist_pop, ' '.join(artist_genres), i['track']['artists'][0]['external_urls']['spotify']
                    ]

                    for feature in features:
                        data_pos.extend([feature['loudness'],feature['energy'],feature['valence'],feature['tempo'], feature['danceability'], feature['acousticness']])

                    final_data.append(data_pos)


            offset += limit

        column_list= ['uri','track_name','track_popularity', 'added_at', 'artist_name', 'artist_popularity', 'genre', 'artist_url',
                    'loudness',	'energy','valence','tempo','danceability','acousticness']
        m_df = pd.DataFrame(final_data, columns = column_list)
        m_df['added_at'] = m_df['added_at'].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d').date())

        return m_df
    

    def extract_playlist_id(_self, plink):
        pattern = re.compile(r'playlist/([^/?]+)')
        match = pattern.search(plink)

        if match:
            playlist_id = match.group(1)
            return playlist_id
        else:
            return 'Invalid URL format'
        
    

    