# Imports
import pandas as pd
# Functions

adresses = {"title_akas": "https://datasets.imdbws.com/title.akas.tsv.gz", 
            "name_basics": "https://datasets.imdbws.com/name.basics.tsv.gz", 
            "title_basics": "https://datasets.imdbws.com/title.basics.tsv.gz", 
            "title_crew": "https://datasets.imdbws.com/title.crew.tsv.gz", 
            "title_principals": "https://datasets.imdbws.com/title.principals.tsv.gz", 
            "title_ratings": "https://datasets.imdbws.com/title.ratings.tsv.gz",
            }

def import_web(web_path):
    return pd.read_csv(web_path, sep='\t', na_values=["\\N"])

def import_local(local_path):
    return pd.read_csv(local_path).drop(columns=["Unnamed: 0"])