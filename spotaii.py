import groove
from groove.load import LoadPLaylist
from groove.metrics import LoadMetrics
from groove.weather import LoadWeather
import streamlit as st
import pandas as pd
import plotly.express as px

cid = st.secrets['CLIENT_ID']
secret = st.secrets['CLIENT_SECRET']

st.set_page_config(layout='wide',page_title='GrooveSpot')

st.title('GrooveSpot')
st.markdown('''
            An easy to use and fun tool to compare your spotify playlist with your friend!
            * Provides `music taste similarity`
            * Recommendations, cool, `interactive and creative analysis` and stats that'd make you go wow!
            ''')

with open('style.css', 'r') as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


st.sidebar.markdown("Enter playlist links for analysis or you can use `manually upload files` option in `debug section` for a quicker analysis.")
flink1 = st.sidebar.text_input("Your spotify playlist link")
flink2 = st.sidebar.text_input("Your friend's spotify playlist link")
abutton = st.sidebar.button('Analyse the playlists')
st.sidebar.divider()

st.sidebar.write('Weather settings')
st.sidebar.caption("Tweak the details from here and it'll be used in analysis")
city = st.sidebar.text_input('City')
country = st.sidebar.text_input('Country code', value='IN')
st.sidebar.divider()

st.sidebar.write('Debugging/Testing section')
st.sidebar.caption("Manually add files to analyse, it'll help in quick testing of all features")
file1 = st.sidebar.file_uploader('playlist file 1(.csv)')
file2 = st.sidebar.file_uploader('playlist file 2(.csv)')

def mood_plot(df):

    moodme = met.calculate_mood_distribution(df)
    labels = moodme.index
    valuedata = moodme.values
    fig = px.pie(names=labels,values=valuedata,hole=0.3,height=340)
    return fig

def sort_features(df,feature, top_n=5, asc=False):
  sorted = df.sort_values(by=feature, ascending=False)[['track_name', 'artist_name']]
  return sorted[:top_n]

def artist_songcount(df, top_n=6):
  ardf = pd.DataFrame(df['artist_name'].value_counts().reset_index()[:top_n])
  ardf.columns=['artist', 'songs']

  return ardf

def artist_accplot(df,ff='acousticness', height=400):

  fig = px.bar(df, x='artist_name', y=ff, range_y=(0,1),color=ff,height=height)
  return fig

def artist_songfreq(df):
  dddf = artist_songcount(df, top_n=7)
  fig = px.area(dddf, x='artist', y='songs', color='songs', height=400)
  return fig

def song_featuresplot(df, ff=['energy', 'acousticness', 'danceability']):
  fig = px.line(df[ff],height=400)
  return fig

def features_histplot(df,width=500,height=400, ff=['energy', 'acousticness', 'danceability', 'valence']):
  fig = px.histogram(df[ff], width=width, height=height)
  return fig


if abutton:
    st.divider()
    with st.spinner('Analysing the playlist, please be patient...'):
        try:

            #1st row
            col1, col2, col3, col4, col5 = st.columns(5)

            with col1:

                if not flink1.strip() and not flink2.strip():
                    if file1 and file2:
                        df1 = pd.read_csv(file1).iloc[:,1:]
                        df2 = pd.read_csv(file2).iloc[:,1:]
                    
                elif flink1.strip() and flink2.strip():
                    lp1 = LoadPLaylist(flink1, cid, secret)
                    lp2 = LoadPLaylist(flink2, cid, secret)

                    df1 = lp1.generate_playlist_df()
                    df2 = lp2.generate_playlist_df()
                else:
                    st.sidebar.error('Error occurred!')
        
                met = LoadMetrics(df1, df2)
                score = met.similar_playlist_metrics()
                
                st.caption('Playlist similarity')
                st.title(score)
                st.divider()

            with col2:

                st.caption('Songs count(your)')
                countme = len(df1)
                st.title(countme)
                st.divider()
                
            with col3:
                st.caption("Songs count(friend)")
                countfr = len(df2)
                st.title(countfr)
                st.divider()

            with col4:
                st.caption('Avg track popularity(Your)')
                st.title(f"{round(df1['track_popularity'].sum()/countme,2)}")
                st.divider()

            with col5:
                st.caption("Avg track popularity(friend's)")
                st.title(f"{round(df2['track_popularity'].sum()/countfr,2)}")
                st.divider()

            
            #2nd row
            col21, col22, col23 = st.columns(3)

            with col21:
                st.write("Mood distribution(Yours)")
                fig = mood_plot(df1)
                st.plotly_chart(fig, use_container_width=True)        
                

            with col22:
                st.write("Mood distribution(your friend)")
                fig = mood_plot(df2)
                st.plotly_chart(fig, use_container_width=True)
                
            with col23:
                st.header('Overall playlist mood')
                mood1 = met.calculate_mood_distribution(df1)
                mood2 = met.calculate_mood_distribution(df2)

                st.markdown(f'''
                            * Your overall playlist is `{mood1.idxmax()}` with `{mood1[mood1.idxmax()]}` 
                            songs belonging to this category.

                            * Your friend's overall playlist is `{mood2.idxmax()}` with `{mood2[mood2.idxmax()]}` 
                            songs belonging to this category. 

                            '''
                            )

            st.divider()
            st.header('Song features variation')
            col31, col32 = st.columns(2)
            
            with col31:
                st.caption('Yours')
                feat1 = song_featuresplot(df1)
                st.plotly_chart(feat1, use_container_width=True)
            
            with col32:
                st.caption("You friend's")
                feat2 = song_featuresplot(df2)
                st.plotly_chart(feat2, use_container_width=True)

            
            outcol1, outcol2 = st.columns(2)
            with outcol1:
                st.header('Song features distribution')
                st.write("How the audio features are distributed among your playlists")
                scol11, scol22 = st.columns(2)
                with scol11:
                    st.caption('Yours')
                    feath1 = features_histplot(df1)
                    st.plotly_chart(feath1, use_container_width=True)
                
                with scol22:
                    st.caption("You friend's")
                    feath2 = features_histplot(df2)
                    st.plotly_chart(feath2, use_container_width=True)

            with outcol2:
                st.header('Most acoustic songs')
                st.write('These are cool and calm songs that give your soul a chill')
                scol421, scol422 = st.columns(2)
                with scol421:
                    st.caption('Yours')
                    acoust1 = sort_features(df1, 'acousticness', top_n=10)
                    acoust1.reset_index(drop=True, inplace=True)
                    
                    st.dataframe(acoust1)
                with scol422:

                    st.caption("Your friend's")
                    acoust2 = sort_features(df2, 'acousticness', top_n=10)
                    acoust2.reset_index(drop=True, inplace=True)
                    
                    st.dataframe(acoust2)

            col51, col52 = st.columns([1,2])
            with col51:
                st.header('Most energetic songs')
                st.write("These are energetic and sparkling songs that'll make you groove!")
                scol511, scol522 = st.columns(2)
                with scol511:
                    st.caption('Yours')
                    ener1 = sort_features(df1, 'energy', top_n=7)
                    ener1.reset_index(drop=True, inplace=True)
                    
                    st.dataframe(ener1)
                with scol522:

                    st.caption("Your friend's")
                    ener2 = sort_features(df2, 'energy', top_n=7)
                    ener2.reset_index(drop=True, inplace=True)
                    st.dataframe(ener2)

            with col52:
                st.header('Songs added on dates')
                datedf1 = pd.DataFrame(df1['added_at'].value_counts().reset_index())
                datedf1.columns = ['date', 'count']
                datedf1['category'] = 'You' 

                datedf2 = pd.DataFrame(df2['added_at'].value_counts().reset_index())
                datedf2.columns = ['date', 'count']
                datedf2['category'] = 'Your friend' 

                merged = pd.concat([datedf1, datedf2], axis=0)

                st.bar_chart(merged, x='date',y='count', color='category', use_container_width=True)

            
            st.divider()
            st.header('Artist analysis')
            st.caption('Analysis focusing on artists involved in playlists')

            col61, col62 = st.columns([1, 2])

            with col61:
                st.header('Misc stats')
                st.caption('Some cool stats based on both playlists')
                statdf = met.get_stats()
                st.dataframe(statdf)
            
            with col62:
                st.header('Song frequency')
                col621, col622 = st.columns(2)
                with col621:
                    st.caption('You')
                    afreq1 = artist_songfreq(df1)
                    st.plotly_chart(afreq1, use_container_width=True)

                with col622:
                    st.caption('Your friend')
                    afreq2 = artist_songfreq(df2)
                    st.plotly_chart(afreq2, use_container_width=True)

            st.header("Artist's energy")
            st.caption('Energies of various artists')

            col71, col72 = st.columns(2)

            with col71:
                st.caption('You')
                eplot1 = artist_accplot(df1, ff='energy')
                st.plotly_chart(eplot1, use_container_width=True)

            with col72:
                st.caption("Your friend")

                eplot2 = artist_accplot(df2, ff='energy')
                st.plotly_chart(eplot2, use_container_width=True)


            st.header("Artist's acousticness")
            st.caption('Acousticness of various artists')

            col81, col82 = st.columns(2)

            with col81:
                st.caption('You')
                aplot1 = artist_accplot(df1, ff='acousticness')
                st.plotly_chart(aplot1, use_container_width=True)

            with col82:
                st.caption("Your friend")

                aplot2 = artist_accplot(df2, ff='acousticness')
                st.plotly_chart(aplot2, use_container_width=True)

            col91, col92 = st.columns([2,1])
            with col91:
                st.header('Recommendations')
                st.caption("Recommending songs that you don't have, from your friend's playlist that're similar from your top 3 songs")

                recomdf = met.cross_recommend()
                st.dataframe(recomdf.iloc[:,0:7])
            with col92:
                st.header('Common songs')
                st.caption('Common songs between you both')
                simdf = met.common_songs()
                if len(simdf)>1:
                    st.dataframe(simdf)
                else:
                    st.warning(f'No common songs found between you two ! Maybe because the similarity is low, i.e {score}')

            st.divider()

            st.header('Playlist based on weather')
            st.caption('Generate a playlist based on the weather around you !')

            col101, col102 = st.columns([2,1])
            with col101:
                api = groove.api_key

                weth = LoadWeather(df2, cid, secret)
                weth_data = weth.get_weather(api, city, country)
                weth_cate = weth.fetch_weather_category(weth_data)
                weth_recomdf = weth.weather_recommend(weth_cate)
                st.dataframe(weth_recomdf, use_container_width=True)
            
            with col102:
                st.caption('Tempreture')
                temp = weth_data['main']['temp']
                st.header(str(temp)+' °C')
                st.divider()
                st.caption('Weather used for playlist')
                st.header(weth_cate)
                st.caption('It considers clear sky or blue sky as sunny for the analysis and generating playlist.')

        except Exception as e:
            st.error('Some unknown error occurred! ')
            print(e)


