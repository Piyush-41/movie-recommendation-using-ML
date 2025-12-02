# import pandas as pd
# import requests
# import time

# API_KEY = '7013c7a7cecc1c74d8ef13d18c25287f'
# TMDB_SEARCH_URL = 'https://api.themoviedb.org/3/search/movie'
# TMDB_IMAGE_BASE_URL = 'https://image.tmdb.org/t/p/w500'

# # Load your movies
# df = pd.read_csv('movies.csv')

# poster_urls = []

# for title in df['title']:
#     params = {'api_key': API_KEY, 'query': title}
#     try:
#         response = requests.get(TMDB_SEARCH_URL, params=params)
#         data = response.json()
#         if data['results']:
#             poster_path = data['results'][0].get('poster_path')
#             if poster_path:
#                 full_url = TMDB_IMAGE_BASE_URL + poster_path
#                 poster_urls.append(full_url)
#             else:
#                 poster_urls.append('')
#         else:
#             poster_urls.append('')
#     except Exception as e:
#         poster_urls.append('')
#     time.sleep(0.25)  # Polite delay to avoid rate limits

# df['poster_url'] = poster_urls
# df.to_csv('movies_with_posters.csv', index=False)
# print("Done! Your new file 'movies_with_posters.csv' has poster URLs for each movie.")
