import pandas as pd
import groove
import spotipy
import requests
from spotipy.oauth2 import SpotifyClientCredentials

class LoadWeather():
    def __init__(_self, fplay, client_id, client_secret):
        
        _self.fplay = fplay
        _self.client_id = client_id
        _self.client_secret = client_secret

        _self.sp = _self.create_spotipy_instance()

    def create_spotipy_instance(_self):
        client_credentials_manager = SpotifyClientCredentials(
            client_id=_self.client_id, client_secret=_self.client_secret
        )
        return spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    def weather_recommend(_self, weather):

        if 'rain' in weather.lower():
            mood = 'rainy'
        elif 'sun' in weather.lower() or 'clear' in weather.lower():
            mood = 'sunny'
        elif 'cloud' in weather.lower():
            mood = 'cloudy'
        elif 'snow' in weather.lower():
            mood = 'snowy'
        elif 'fog' in weather.lower():
            mood = 'foggy'
        else:
            mood = 'sunny'

        seed_genres = groove.mood_categories1[mood]['seed_genres']
        valence_range = groove.mood_categories1[mood]['valence']
        tempo_range = groove.mood_categories1[mood]['tempo']
        acousticness_range = groove.mood_categories1[mood]['acousticness']


        tracks = _self.sp.recommendations(seed_genres=seed_genres, target_valence=valence_range,
                                    target_tempo=tempo_range, target_acousticness=acousticness_range, limit=20)
        tracklist = []
        for i in tracks['tracks']:
            tracklist.append([i['name'], i['artists'][0]['name']])

        wrecom1 =  pd.DataFrame(tracklist, columns = ['track_name','artist_name'])

        mood_filter = (
            (_self.fplay['valence'] >= groove.mood_categories2[mood]['valence'][0]) &
            (_self.fplay['valence'] <= groove.mood_categories2[mood]['valence'][1]) &
            (_self.fplay['tempo'] >= groove.mood_categories2[mood]['tempo'][0]) &
            (_self.fplay['tempo'] <= groove.mood_categories2[mood]['tempo'][1]) &
            (_self.fplay['acousticness'] >= groove.mood_categories2[mood]['acousticness'][0]) &
            (_self.fplay['acousticness'] <= groove.mood_categories2[mood]['acousticness'][1])
        )
        wrecom2 =  _self.fplay[mood_filter]

        final_wrecom = pd.concat([wrecom1[['track_name', 'artist_name']], wrecom2[['track_name', 'artist_name']]], axis=0)
        final_wrecom = final_wrecom.sample(frac=1).reset_index(drop=True)

        return final_wrecom
    

    def get_weather(_self, api_key, city, country, units='metric'):
        base_url = "http://api.openweathermap.org/data/2.5/weather"
        params = {
            'q': f"{city},{country}",
            'appid': api_key,
            'units': units
        }

        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            weather_data = response.json()
            return weather_data
        except requests.exceptions.RequestException as e:
            return None
        
    def categorize_weather(_self, description):
        
        sunny_keywords = ['clear', 'sunny']
        rainy_keywords = ['rain', 'drizzle', 'thunderstorm']
        cloudy_keywords = ['cloud', 'overcast']
        foggy_keywords = ['fog', 'mist']

        description_lower = description.lower()

        if any(keyword in description_lower for keyword in sunny_keywords):
            return 'Sunny'
        elif any(keyword in description_lower for keyword in rainy_keywords):
            return 'Rainy'
        elif any(keyword in description_lower for keyword in cloudy_keywords):
            return 'Cloudy'
        elif any(keyword in description_lower for keyword in foggy_keywords):
            return 'Foggy'
        else:
            return 'Sunny'
        
        
    def fetch_weather_category(_self,weather_data):
        if weather_data:
            description = weather_data['weather'][0]['description']
            weather_category = _self.categorize_weather(description)
            return weather_category
            
        else:
            return "Failed to fetch weather data."
    

    
    






        