from fastapi import FastAPI
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

df_names = pd.read_csv('df_platform.csv')

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


@app.get('/get_recomendation/{title}')
def get_recomendation(title):
    top=5
    vectorizer = TfidfVectorizer()
    #Construct the required TF-IDF matrix by fitting and transforming the data
    vectorizer_matrix = vectorizer.fit_transform(df_names['listed_in'])

    #Compute the cosine similarity matrix
    cosine_sim = cosine_similarity(vectorizer_matrix)
    #Get the index of the movie that matches the title
    idx = df_names[df_names['title'] == title].index[0]

    #Get the cosine similarity scores of all movies with the given movie
    sim_scores = list(enumerate(cosine_sim[idx]))

    #Sort the movies based on the cosine similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    #Loop until we have 5 recommended movies (excluding itself)
    movie_indices = []
    count = 0
    while len(movie_indices) < top:
        idx = sim_scores[count][0]
        if df_names.iloc[idx]['title'] != title: #Exclude the same movie
            movie_indices.append(idx)
        count += 1
    a = list(df_names.iloc[movie_indices]['title'].values)
    
    #Return the top n most similar movies
    return {'recomendacion': a}