from fastapi import FastAPI
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import heapq
import numpy as np

df_names = pd.read_csv('df_platform.csv')
df_ml = pd.read_csv('df_ml.csv')

app = FastAPI()

@app.get('/get_max_duration/{anio}/{plataforma}/{dtype}')
def get_max_duration(anio: int, plataforma: str, dtype: str):
    selection = df_names.query('type == "movie" and release_year == @anio and duration_type == @dtype and id.str[0] == @plataforma[0]')
    return {'pelicula': selection.loc[selection["duration_int"].idxmax(), "title"]}

@app.get('/get_score_count/{plataforma}/{scored}/{anio}')
def get_score_count(plataforma: str, scored: float, anio: int):
    selection_name = df_names.query('type == "movie" and release_year == @anio and id.str[0] == @plataforma[0] and scored == @scored')
    return {
        'plataforma': plataforma,
        'cantidad': selection_name["id"].nunique(),
        'anio': anio,
        'score': scored
    }

@app.get('/get_count_platform/{plataforma}')
def get_count_platform(plataforma: str):
    movies = df_names.query('type == "movie" and id.str[0] == @plataforma[0]')
    return {'plataforma': plataforma, 'peliculas': movies.shape[0]}


@app.get('/get_actor/{plataforma}/{anio}')
def get_actor(plataforma: str, anio: int):
    selection = df_names.query('id.str[0] == @plataforma[0] and release_year == @anio')
    if selection.empty:
        return {"error": "No se encontraron resultados para los parámetros proporcionados"}
    actor = selection["cast"].str.split(", ", expand=True).stack().value_counts()
    return {
        'plataforma': plataforma,
        'anio': anio,
        'actor': actor.index[0],
        'apariciones': int(actor[0])
    }

@app.get('/prod_per_county/{tipo}/{pais}/{anio}')
def prod_per_county(tipo: str, pais: str, anio: int):
    products = df_names.query('release_year == @anio and type == @tipo and country == @pais')
    return {'pais': pais, 'anio': anio, 'contenido': products.shape[0]}

@app.get('/get_contents/{rating}')
def get_contents(rating: str):
    contents = df_names.query('rating == @rating')
    return {'rating': rating, 'contenido': contents.shape[0]}


# Precompute the vectorizer and cosine similarity matrix
vectorizer = TfidfVectorizer()
vectorizer_matrix = vectorizer.fit_transform(df_ml['listed_in'])
cosine_sim = cosine_similarity(vectorizer_matrix)
@app.get('/get_recomendation/{title}')
def get_recommendation(title, top=5):
    # Get the index of the movie that matches the title
    idx = df_ml[df_ml['title'] == title].index[0]

    # Get the cosine similarity scores of all movies with the given movie
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Keep only the top `top` elements at any given time
    top_sim_scores = heapq.nlargest(top, sim_scores, key=lambda x: x[1])

    # Loop until we have `top` recommended movies (excluding itself)
    movie_indices = []
    for idx, sim_score in top_sim_scores:
        if df_ml.iloc[idx]['title'] != title: #Exclude the same movie
            movie_indices.append(idx)

    # Use numpy to get the titles of the recommended movies
    movie_indices = np.array(movie_indices)
    a = list(df_ml.iloc[movie_indices]['title'].values)

    # Return the top `top` most similar movies
    return {'recomendacion': a}