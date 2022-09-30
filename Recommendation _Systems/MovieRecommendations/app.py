import streamlit as st
import pickle
import pandas as pd
import requests

#get the movie and the poster
def fetch_poster(movie_id):
    response=requests.get("https://api.themoviedb.org/3/movie/{}?api_key=ed073dd4f6c66dc43d288008cbd13a5f&language=en-US".format(movie_id))
    data=response.json()
    return "https://image.tmdb.org/t/p/w500/"+data["poster_path"]

#get the recommendations
def recommend_me(movie):
    movie_index = movies[movies["title"] == movie].index[0]
    distance = similarity[movie_index]
    movie_list = sorted(enumerate(distance), reverse=True, key=lambda x: x[1])[1:6]

    recommendation_list = []
    poster_list = []

    for i in movie_list:
        movie_id = movies.iloc[i[0]].id
        recommendation_list.append(movies.iloc[i[0]].title)
        poster_list.append(fetch_poster(movie_id))

    return recommendation_list, poster_list


#get the pkl objects
movie_dict = pickle.load(open("movieNamedict.pkl", 'rb'))
similarity = pickle.load(open("similarity.pkl", 'rb'))

movies = pd.DataFrame(movie_dict)
st.title("Movie Recommender System")

#User selects the movie
Movie_i_like = st.selectbox("Choose your movie", movies['title'].values)

#user clicks on the recommend button
if st.button("Recommend"):
    recommendations, posters=recommend_me(Movie_i_like)

    col1, col2, col3, col4, col5 = st.columns(5)
    cols=list([col1, col2, col3, col4, col5])
    for i in range (1 , 6):
        with cols[i-1]:
            st.text(recommendations[i-1])
            st.image(posters[i-1])

