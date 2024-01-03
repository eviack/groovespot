import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

class LoadMetrics():
    def __init__(_self, playdf1, playdf2):

        _self.playdf1 = playdf1
        _self.playdf2 = playdf2

    def similar_playlist_metrics(_self):

        try:
            m_sim_data1 = _self.playdf1['artist_name']+' '+ _self.playdf1['genre']
            m_sim_data2 = _self.playdf2['artist_name']+' '+ _self.playdf2['genre']

            m_simconcat1 = ' '.join(set(' '.join(map(str,m_sim_data1)).lower().split()))
            m_simconcat2 = ' '.join(set(' '.join(map(str,m_sim_data2)).lower().split()))

            cv = CountVectorizer()
            v1 = cv.fit_transform([m_simconcat1 if len(m_simconcat1)>len(m_simconcat2) else m_simconcat2])
            v2 = cv.transform([m_simconcat1 if len(m_simconcat1)<len(m_simconcat2) else m_simconcat2])

            return f'{round(cosine_similarity(v1,v2)[0][0]*100, 2)}' + ' %'
        
        except Exception as e :
            return e
        
    def cross_recommend(_self):
        try:
            tags1 = (_self.playdf1['genre'] + ' ' + _self.playdf1['artist_name']).apply(lambda x: str(x).lower())
            tags2 = (_self.playdf2['genre'] + ' ' + _self.playdf2['artist_name']).apply(lambda x: str(x).lower())
            #picking tags of top 3 songs from playlist 1 and adding it to playlist 2 tags
            simseries = pd.concat([tags1[:3], tags2], axis=0, ignore_index=True)

            cv2 = CountVectorizer()
            m_vec = cv2.fit_transform(simseries).toarray()

            #calculating cosine similarity of each song with each other in playlist 2
            similarity = cosine_similarity(m_vec)
            top_n =10
            sm1 = similarity[0][2:].argsort()[-top_n:][::-1]
            sm2 = similarity[1][2:].argsort()[-top_n:][::-1]
            sm3 = similarity[2][2:].argsort()[-top_n:][::-1]


            # Combine the top indices from both arrays
            combined_indices = np.concatenate((sm1,sm2,sm3))

            # Remove duplicates if any (optional)
            combined_indices = np.unique(combined_indices)

            # Sort the combined indices to get the overall top indices
            overall_top_indices = combined_indices[np.argsort(-similarity[0][1:][combined_indices])][:top_n]
            recomff= _self.playdf2.iloc[[i for i in overall_top_indices]]

            finalf =  recomff[~recomff.isin(_self.playdf1)].iloc[:,1:].reset_index(drop=True)

            return finalf
        
        except Exception as e:
            return e
    

    def get_stats(_self):
        try:
            index_list = ['oldest song','latest song', 'most popular song', 'most popular artist', 'most added artist']
            f1old = _self.playdf1.sort_values(by='added_at').iloc[0]['track_name'] #oldest song
            f2old = _self.playdf2.sort_values(by='added_at').iloc[0]['track_name'] #oldest song

            f1lat = _self.playdf1.sort_values(by='added_at', ascending=False).iloc[0]['track_name'] #latest song
            f2lat = _self.playdf2.sort_values(by='added_at', ascending=False).iloc[0]['track_name'] #latest song

            f1pop = _self.playdf1.sort_values(by='track_popularity', ascending=False).iloc[0]['track_name'] #most popular song
            f2pop= _self.playdf2.sort_values(by='track_popularity', ascending=False).iloc[0]['track_name'] #most popular song

            f1popart = _self.playdf1.sort_values(by='artist_popularity', ascending=False).iloc[0]['artist_name']  #most popular artist
            f2popart = _self.playdf2.sort_values(by='artist_popularity', ascending=False).iloc[0]['artist_name']  #most popular artist

            f1moccur = _self.playdf1['artist_name'].value_counts().index[0]+ f", {_self.playdf1['artist_name'].value_counts()[0]} times"
            f2moccur = _self.playdf2['artist_name'].value_counts().index[0]+ f", {_self.playdf2['artist_name'].value_counts()[0]} times"

            data = [[f1old, f2old], [f1lat, f2lat], [f1pop, f2pop], [f1popart, f2popart], [f1moccur, f2moccur]]

            stat_frame = pd.DataFrame(data, index=index_list, columns=['You', 'Your friend'])

            return stat_frame
        
        except Exception as e:
            return 'Error getting stats, seems like there is error is loading the playlist'
        
    def common_songs(_self):
        try :
            cmdf = pd.merge(_self.playdf1, _self.playdf2, how='inner', on=['uri'])
            return cmdf.iloc[:,1:8].reset_index(drop=True)
        except Exception as e:
            return 'Error finding common songs, seems like there is error is loading the playlist'
    

    def sort_features(_self,playdf,feature, top_n, asc=False):
        try:
            sorted = playdf.sort_values(by=feature, ascending=asc)[['track_name', 'artist_name',feature]]
            return sorted[:top_n]
        except Exception as e:
            return 'Unknown error occurred'

    def calculate_mood_distribution(_self, playdf):
        mood_distribution = {"Happy": 0, "Neutral": 0, "Gloomy": 0}

        for valence in playdf["valence"]:
            mood_category = _self.categorize_mood(valence)
            mood_distribution[mood_category] += 1

        return pd.Series(mood_distribution)

    def categorize_mood(_self, valence):
        if valence >= 0.7:
            return "Happy"
        elif 0.5 <= valence < 0.7:
            return "Neutral"
        else:
            return "Gloomy"
        
    
        