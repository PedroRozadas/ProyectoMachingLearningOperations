from fastapi import FastAPI
import pandas as pd

df_names = pd.read_csv('https://drive.google.com/uc?id=1z3-83_I7ZfHrxbB0qC2gAzz0AfgZH7GI')
list_url = ["https://drive.google.com/uc?id=1ImYbz29myZKGDZCYY4r5yzXWcdPqp-DL",
            "https://drive.google.com/uc?id=1rlpHWaxvo5kX5hyyOP7i5zpC5V9RfsaV",
            "https://drive.google.com/uc?id=1CBZA4xkDhfa-CX8dr92rhjKR3HhgctzE",
            "https://drive.google.com/uc?id=1CsaTyLVB-AZ78yJp9XeSw2qvTSNj9aYx",
            "https://drive.google.com/uc?id=1QztUrbE6CEC57AgbNcR9XJf9WIvwUF3P",
            "https://drive.google.com/uc?id=1y0TKNdKhSumjjaDSUGQTPIlMZuFqy1Zn",
            "https://drive.google.com/uc?id=18WgvpsLVK_5uhCJm5HyZSytNreOIRiT1",
            "https://drive.google.com/uc?id=1dwqAfTL7BXbOvJn_A3bwQkL9_gbIFoTz"]

#Merging multiple csv files into a single dataframe
df_ratings = pd.concat(map(pd.read_csv, list_url))

df_ratings.reset_index(drop=True, inplace=True)

df_names["rating"] = df_names["rating"].fillna("G")

df_names["date_added"] = df_names["date_added"].str.strip()
df_names["date_added"] = pd.to_datetime(df_names["date_added"], format="%B %d, %Y")

df_ratings["timestamp"] = pd.to_datetime(df_ratings["timestamp"], unit="s")

cols = ["type", "title", "director", "cast", "country", "listed_in", "description", "rating"]
df_names[cols] = df_names[cols].apply(lambda x: x.str.lower())

# split duration into two separate columns
df_duration = df_names["duration"].str.split(" ", n=1, expand=True)

# assign the resulting columns to duration_int and duration_type respectively
df_names["duration_int"] = df_duration[0].apply(lambda x: x if pd.notnull(x) else None)

df_names["duration_type"] = df_duration[1].apply(lambda x: x if pd.notnull(x) else None)

df_names["duration_int"] = df_names["duration_int"].astype(pd.UInt16Dtype())

app = FastAPI()

@app.get('/get_max_duration/{anio}/{plataforma}/{dtype}')
def get_max_duration(anio: int, plataforma: str, dtype: str):
    selection = df_names.query('type == "movie" and release_year == @anio and duration_type == @dtype and id.str[0] == @plataforma[0]')
    return {'pelicula': selection.loc[selection["duration_int"].idxmax(), "title"]}

@app.get('/get_score_count/{plataforma}/{scored}/{anio}')
def get_score_count(plataforma: str, scored: float, anio: int):
    selection_name = df_names.query('type == "movie" and release_year == @anio and id.str[0] == @plataforma[0]')
    selection_rating = df_ratings.query('movieId in @selection_name["id"].values and rating > @scored')
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
    return {'pais': pais, 'anio': anio, 'peliculas': products.shape[0]}

@app.get('/get_contents/{rating}')
def get_contents(rating: str):
    contents = df_names.query('rating == @rating')
    return {'rating': rating, 'contenido': contents.shape[0]}

# @app.get('/get_recomendation/{title}')
# def get_recomendation(title,):
    
#     return {'recomendacion':respuesta}