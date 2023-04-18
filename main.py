from fastapi import FastAPI
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

df_names = pd.read_csv('https://drive.google.com/uc?id=1jW-R0mTe748Kj7UdNwwLn70pqmZJts_3')

app = FastAPI()

@app.get('/get_max_duration/{anio}/{plataforma}/{dtype}')
def get_max_duration(anio: int, plataforma: str, dtype: str):
    selection = df_names.query('type == "movie" and release_year == @anio and duration_type == @dtype and id.str[0] == @plataforma[0]')
    return {'pelicula': selection.loc[selection["duration_int"].idxmax(), "title"]}

@app.get('/get_score_count/{plataforma}/{scored}/{anio}')
def get_score_count(plataforma: str, scored: float, anio: int):
    selection_name = df_names.query('type == "movie" and release_year == @anio and id.str[0] == @plataforma[0]')
    selection_rating = df_ratings.query('movieId in @selection_name["id"].values and scored > @scored')
    return {
        'plataforma': plataforma,
        'cantidad': selection_rating["movieId"].unique().shape[0],
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

@app.get('/get_recomendation/{title}')
def get_recomendation(title):
    vectorizer = TfidfVectorizer()
    vectorizer_matrix = vectorizer.fit_transform(df_names["listed_in"]) #Learn vocabulary and idf, return document-term matrix.
    # vectorizer.get_feature_names_out()
    cosine_sim = cosine_similarity(vectorizer_matrix)
    matching_content = sorted(list(enumerate(cosine_sim[10])), key=lambda x: x[1], reverse=True)
    top_matching = [i[0] for i in matching_content[1:6]]
    return {'recomendacion': df_names["title"].iloc[top_matching]}