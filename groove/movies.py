import imdb
import random
import pandas as pd

def get_random_movies_dataframe(genres, n):
    ia = imdb.IMDb()
    movies = ia.get_top50_movies_by_genres(genres)

    mov_list = []

    for i in movies:
        mov_id = i.movieID
        mov_name = i.get('title')
        mov_plot = i.get('plot', 'N/A')

        mov_list.append({'id': mov_id, 'name': mov_name, 'plot': mov_plot})

    random.shuffle(mov_list)
    random_movies = mov_list[:n]

    df = pd.DataFrame(random_movies)

    return df