# ProyectoMachingLearningOperations
To do this we are given 4 datasets from different streaming platforms, amazon, disney, hulu, netflix and 8 datasets containing the rating/score that certain users made.
# Objectives:
ETL transformations:
Generate id column: Each id will consist of the first letter of the platform name, followed by the show_id already present in the datasets.

Null values in the rating field must be replaced by the string "G".

Dates must be in the format YYYYY-mm-dd.

Text fields should be in lower case.

The duration column must be converted into two columns: duration_int and duration_type.
API development:
The function get_max_duration(year, platform, duration_type) returns only the movie name string. The movie (only movie, not series, etc) with the longest duration according to year, platform and duration type. 

The function get_score_count(platform, scored, year) returns an int, with the total number of movies that meet the request. The number of movies (only movies, not series, etc) by platform, with a score greater than XX in a given year. 

The function get_count_platform(platform) returns an int, with the total number of movies of that platform. Number of movies (only movies, not series, etc) by platform. Platforms should be named amazon, netflix, hulu, disney.

The function get_actor(platform, year) returns only the string with the name of the most repeated actor according to the given platform and year.

The function prod_per_county(type,country,year) returns the amount of contents/products according to the type of content (movie,series) by country and year in a dictionary with variables named 'country' (country name), 'year' (year), 'movie' (amount of contents/products).

The function get_contents(rating) returns the total number of contents with that audience rating (for which audience the movie was rated).
# Repository content:

The .gitignore file has the content that ignores the git push.

In the notebook ETL_EDA_ML.ipynb I perform the ETL, EDA and ML processes.
check

The file df_platform.csv is the dataset after the ETL and EDA to be consumed with the FastAPI.

The main.py file has the functions to be instantiated by FastAPI.

The requirements.txt file has the names of the libraries used for the deploy.
# Tools and languages used.
Visual Studio Code.
Git.
FastAPI.
Render.
Python.
# Links
Drive con los datasets:
https://drive.google.com/drive/folders/1f-wDJLGXNbYHJF5DRXRzOcUn_MW3ohbj?usp=share_link
Video explicativo de la API:

Deploy de la API en Render:
https://entertainment-recommendation.onrender.com/Docs
