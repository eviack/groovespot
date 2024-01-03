mood_categories1 = {
    'sunny': {'seed_genres': ['pop', 'upbeat', 'happy'], 'valence': (0.6, 1.0), 'tempo': (120, 180), 'acousticness': (0.0, 0.4)},
    'cloudy': {'seed_genres': ['indie', 'mellow', 'downtempo', 'winter'], 'valence': (0.0, 8.0), 'tempo': (120, 200), 'acousticness': (0.0, 0.4)},
    'rainy': {'seed_genres': ['acoustic', 'chill', 'sad'], 'valence': (0.0, 0.4), 'tempo': (60, 120), 'acousticness': (0.6, 1.0)},
    'snowy': {'seed_genres': ['ambient', 'instrumental', 'winter'], 'valence': (0.4, 0.8), 'tempo': (60, 120), 'acousticness': (0.6, 1.0)},
    'foggy': {'seed_genres': ['ambient', 'downtempo', 'chill'], 'valence': (0.4, 0.8), 'tempo': (60, 120), 'acousticness': (0.4, 0.7)},
}

mood_categories2 = {
    'sunny': {'valence': (0.6, 1.0), 'tempo': (120, 180), 'acousticness': (0.0, 0.4)},
    'cloudy': {'valence': (0.0, 8.0), 'tempo': (120, 200), 'acousticness': (0.0, 0.4)},
    'rainy': {'valence': (0.0, 0.4), 'tempo': (60, 120), 'acousticness': (0.6, 1.0)},
    'snowy': {'valence': (0.4, 0.8), 'tempo': (60, 120), 'acousticness': (0.6, 1.0)},
    'foggy': {'valence': (0.4, 0.8), 'tempo': (60, 120), 'acousticness': (0.4, 7.0)},
}
moodgenremap = {
    'gloomy':['mystery', 'horror', 'thriller','crime', 'psychological', 'romance', 'drama'],
    'neutral':['romance', 'mystery', 'sci-fi','action', 'comedy', 'drama', 'musical'],
    'happy':['romance', 'action', 'family', 'sci-fi', 'comedy', 'drama', 'musical']
}
api_key = '83ac504be17168811acb874c3d0fa8f5'