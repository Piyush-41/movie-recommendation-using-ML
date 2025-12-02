import streamlit as st
import pandas as pd
import numpy as np
import difflib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import requests
import time  # For rate limiting

# # TMDB API key (keep this secure; consider environment variables in production)
# TMDB_API_KEY = "7013c7a7cecc1c74d8ef13d18c25287f"

# def fetch_poster(id):
#     """Fetch poster URL for a movie by TMDB ID."""
#     if pd.isna(id) or id == '':
#         return ''
    
#     url = f"https://api.themoviedb.org/3/movie/{id}?api_key={TMDB_API_KEY}&language=en-US"
#     try:
#         response = requests.get(url, timeout=10)
#         if response.status_code == 200:
#             data = response.json()
#             poster_path = data.get('poster_path')
#             if poster_path:
#                 return f"https://image.tmdb.org/t/p/w500{poster_path}"
#         return ''  # Return empty if no poster or error
#     except requests.RequestException:
#         return ''
#     finally:
#         time.sleep(0.1)  # Rate limiting to respect TMDB limits

# === Streamlit App ===
st.title('Movie Recommendation System')

# === Load Data ===
@st.cache_data  # Cache for performance; clears on data change
def load_and_prepare_data():
    movies_data = pd.read_csv('movies.csv')
    # movies_data = movies_data.head(1) # Limit for performance in demo
    # Fetch and add posters if not already present (assumes 'movie_id' column exists)
    # if 'poster_url' not in movies_data.columns:
    #     st.info("Fetching movie posters... This may take a few minutes for large datasets.")
    #     movies_data['poster_url'] = movies_data['id'].apply(fetch_poster)
    #     # Optionally save updated CSV: movies_data.to_csv('movies_with_posters.csv', index=False)
    # else:
    #     st.success("Using cached posters from movies.csv.")
    
    def combine_features(row):
        return f"{row['genres']} {row['keywords']} {row['tagline']} {row['cast']} {row['director']}"
    
    movies_data['combined_features'] = movies_data.apply(combine_features, axis=1)
    movies_data['combined_features'] = movies_data['combined_features'].fillna('')
    
    # TFIDF and Similarity (cache these too for efficiency)
    vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')  # Added limits for performance
    tfidf_matrix = vectorizer.fit_transform(movies_data['combined_features'])
    similarity = cosine_similarity(tfidf_matrix)
    
    return movies_data, vectorizer, tfidf_matrix, similarity

movies_data, vectorizer, tfidf_matrix, similarity = load_and_prepare_data()

def recommend_movies(movie_name, num_recommendations=10):
    movie_title_list = movies_data['title'].tolist()
    close_matches = difflib.get_close_matches(movie_name, movie_title_list, n=1)
    if not close_matches:
        return []
    best_match = close_matches[0]
    idx = movies_data[movies_data['title'] == best_match].index[0]
    similarity_scores = list(enumerate(similarity[idx]))
    sorted_movies = sorted(similarity_scores, key=lambda x: x[1], reverse=True)[1:num_recommendations+1]
    recommendations = []
    
    for i in sorted_movies:
        movie_info = movies_data.iloc[i[0]]
        recommendations.append({
            'Title': movie_info['title'],
            'Genres': movie_info['genres'],
            'Overview': movie_info.get('overview', ''),
            'Cast': movie_info.get('cast', ''),
            'Director': movie_info.get('director', ''),
            'Tagline': movie_info.get('tagline', ''),
            'Poster': movie_info.get('poster_url', '')  # Use the new column
        })
    return recommendations

# === Streamlit UI ===
user_input = st.text_input('Enter a movie name:')
num_rec = st.slider('Number of recommendations', 1, 20, 10)

if st.button('Recommend'):
    if user_input:
        recs = recommend_movies(user_input, num_rec)
        if recs:
            for movie in recs:
                st.subheader(movie['Title'])
                # Display poster
                if movie['Poster'] and movie['Poster'] != '':
                    st.image(movie['Poster'], width=200, caption=movie['Title'])
                else:
                    st.write("🖼️ Poster not available")
                col1, col2 = st.columns([1, 2])  # Layout for better display
                with col1:
                    st.write('**Genres:**', movie['Genres'])
                    st.write('**Cast:**', movie['Cast'])
                    st.write('**Director:**', movie['Director'])
                with col2:
                    st.write('**Overview:**', movie['Overview'])
                    st.write('**Tagline:**', movie['Tagline'])
                st.divider()
        else:
            st.error('No close match found. Try a different movie name.')
    else:
        st.warning('Please enter a movie name.')

# Quick script to add movie_ids if needed (run separately)
# def get_movie_id(title):
#     search_url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={title.replace(' ', '%20')}&page=1"
#     try:
#         response = requests.get(search_url)
#         if response.status_code == 200:
#             data = response.json()
#             if data['results']:
#                 return data['results'][0]['id']
#     except:
#         pass
#     return ''

# # Load CSV and add IDs (uncomment to use)
# df = pd.read_csv('movies.csv')
# df['movie_id'] = df['title'].apply(get_movie_id)
# df.to_csv('movies_with_ids.csv', index=False)









# Footer
st.markdown("---")
st.caption("Movie Recommendation System powered by Streamlit and TMDB API \nDeveloped by Piyush Patel")
