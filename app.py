

import streamlit as st
import pickle
import pandas as pd
import requests
from streamlit_option_menu import option_menu


with st.sidebar:
    selected = option_menu(
        menu_title="Menu",
        options=["Home","About"],
        icons=["house","file-earmark-person"],
        menu_icon="cast",
        default_index=0,
    )
    if selected == "Home":
        st.title("This is a Recommendation system used to recommend the related movie")
    if selected == "About":
        st.title("Hey this is Shruti Tambe\n")
        s = option_menu(
            menu_title=None,
            options=["instagram", "linkedin", "github"],
            icons=["instagram", "linkedin", "github"],
            menu_icon="cast",
            default_index=0,
         )
        if s == "github":
            st.title("Check my Github\nhttps://github.com/Shruti241")
        elif s == "Linkedin":
            st.title("Check my Linkedin\nhttps://www.linkedin.com/in/shruti-tambe-727657228/")
        elif s == "instagram":
            st.title("Check my Instagram\nhttps://www.instagram.com/sh_ruti7626/")


def crew(movie_id):
    response = requests.get(
        "https://api.themoviedb.org/3/movie/{0}/credits?api_key=b888bc3907fd642bcabbc5088a3da153&language=en-US".format(movie_id))
    data = response.json()
    crew_name = []
    final_cast = []
    k = 0
    for i in data["cast"]:
        if (k!=6):
            crew_name += [i['name']]
            final_cast += ["https://image.tmdb.org/t/p/w500/" + i['profile_path']]
            k += 1
        else:
            break
    return crew_name, final_cast

def date(movie_id):
    response = requests.get(
        "https://api.themoviedb.org/3/movie/{}?api_key=b888bc3907fd642bcabbc5088a3da153&language=en-US".format(movie_id))
    data = response.json()
    return data['release_date']


def genres(movie_id):
    response = requests.get(
        "https://api.themoviedb.org/3/movie/{}?api_key=b888bc3907fd642bcabbc5088a3da153&language=en-US".format(movie_id))
    data = response.json()
    return data['genres']

def overview(movie_id):
    response = requests.get(
        "https://api.themoviedb.org/3/movie/{}?api_key=b888bc3907fd642bcabbc5088a3da153&language=en-US".format(movie_id))
    data = response.json()
    return data['overview']
def poster(movie_id):
    response = requests.get(
        "https://api.themoviedb.org/3/movie/{}?api_key=047b5d937e9c61972de4800ecc7ba3f1&language=en-US".format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']



def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    cosine_angles = similarity_matrix[movie_index]
    recommended_movies = sorted(list(enumerate(cosine_angles)), reverse=True, key=lambda x: x[1])[0:7]

    movie_rec = []
    movie_rec_posters = []
    final_name, final_cast = crew(movies.iloc[movies[movies['title'] == movie].index[0]].movie_id)
    gen = genres(movies.iloc[movies[movies['title'] == movie].index[0]].movie_id)
    overview_final = overview(movies.iloc[movies[movies['title'] == movie].index[0]].movie_id)
    rel_date = date(movies.iloc[movies[movies['title'] == movie].index[0]].movie_id)

    for i in recommended_movies:
        movie_rec += [movies.iloc[i[0]].title]
        movie_rec_posters += [poster(movies.iloc[i[0]].movie_id)]
    return final_name, final_cast, rel_date, gen, overview_final, movie_rec, movie_rec_posters


movies_dict = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)

similarity_matrix = pickle.load(open('similarity_matrix.pkl','rb'))

st.title('Movie Recommender System')

select_movie_name = st.selectbox('How movie would you like to watch?',movies['title'].values)



def process(genre):
    final = []
    for i in genre:
        final.append(i['name'])

    return final

if st.button('Search'):
    name, cast, rel_date, gen, overview_final, ans, posters = recommend(select_movie_name)

    st.header(select_movie_name)
    col_1, col_2 = st.columns(2)

    with col_1:
        st.image(posters[0], width=225, use_column_width=True)

    with col_2:
        st.write("Title: {}".format(ans[0]))
        st.write("Overview: {}".format(overview_final))
        gen = process(gen)
        gen = ",".join(gen)
        st.write("Genres: {}".format(gen))
        st.write("Release Date: {}".format(rel_date))

        st.title("Top casts")



        c1, c2, c3 = st.columns(3)
        with c1:
            st.image(cast[0], width=225, use_column_width=True)
            st.caption(name[0])
        with c2:
            st.image(cast[1], width=225, use_column_width=True)
            st.caption(name[1])
        with c3:
            st.image(cast[2], width=225, use_column_width=True)
            st.caption(name[2])

        c1, c2, c3 = st.columns(3)
        with c1:
            st.image(cast[3], width=225, use_column_width=True)
            st.caption(name[3])

        with c2:
            st.image(cast[4], width=225, use_column_width=True)
            st.caption(name[4])

        with c3:
            st.image(cast[5], width=225, use_column_width=True)
            st.caption(name[5])

        st.title("")

        st.title("Similar Movies that you would like to watch")

        c1, c2, c3 = st.columns(3)
        with c1:
            st.image(posters[1], width=225, use_column_width=True)
            st.write(ans[1])
        with c2:
            st.image(posters[2], width=225, use_column_width=True)
            st.write(ans[2])
        with c3:
            st.image(posters[3], width=225, use_column_width=True)
            st.write(ans[3])

        c1, c2, c3 = st.columns(3)
        with c1:
            st.image(posters[4], width=225, use_column_width=True)
            st.write(ans[4])

        with c2:
            st.image(posters[5], width=225, use_column_width=True)
            st.write(ans[5])

        with c3:
            st.image(posters[6], width=225, use_column_width=True)
            st.write(ans[6])
