import streamlit as st
import pickle
import pandas as pd
import requests


def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=091b43a27788bdcced566b8197137cf1&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w185/"+ data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title']==movie].index[0]
    distance = similarity[movie_index]
    movies_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters =[]
    for i in movies_list:
        movies_id = movies.iloc[i[0]].id
        recommended_movies.append(movies.iloc[i[0]].title)
        ## fetch poster from API
        recommended_movies_posters.append(fetch_poster(movies_id))
    return recommended_movies,recommended_movies_posters

movies_dict = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl','rb'))

st.title('Movie Recommender System ')

option = st.selectbox("Select a movie",movies['title'].values)

if st.button("Recommend"):
    names,posters = recommend(option)
    cols = st.columns(5)

    for i, col in enumerate(cols):
        with col:
            st.text(names[i])
            st.image(posters[i])