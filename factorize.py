# -*- coding: utf-8 -*-

# I. Import des bibliotheques et dataframes

from module import import_local # Fonction personnelle pour charger des DF
from sklearn.neighbors import NearestNeighbors # L'algorithme utilisé
import requests
from bs4 import BeautifulSoup
import re

base_adress = "df_base_frenchie.csv" 
             # Base contenant les films qui ont une distribution en France

df_base = import_local(base_adress)



# II. Traitement de la base


df_factorized = df_base.copy()

# 1. Ajout de colonnes supplémentaires: chacun des genres uniques,
#    (approximation de l') origine française.

all_genres = df_base.genres.unique()
unique_genres = set()
for k in all_genres:
    if "," in k:
        for kk in k.split(','):
            unique_genres.add(kk)
    else:
        unique_genres.add(k)

for genre in unique_genres:
    df_factorized[genre] = df_base["genres"].apply(
                                        lambda x : 1 if genre in x else -1
                                                  )

df_factorized["is_title_french"] = (
    df_factorized["primaryTitle"] == df_factorized["title"]
                                )

# 2. Numérisation des colonnes non-numériques pertinentes

df_factorized["actorCategory"] = df_factorized["actorCategory"].apply(
                                        lambda x : 1 if x=='actress' else -1
                                                                     )

df_factorized["is_title_french"] = df_factorized["is_title_french"].apply(
                                                    lambda x : 1 if x else -1
                                                                         )

df_factorized.to_csv("df_factorized.csv")

# 3. Préparation de l'affichage des résultats

df_base_show = df_base.copy()
df_base_show = df_base_show[df_base['numVotes'] > 475].sort_values(
                                                            by='numVotes',
                                                            ascending=False
                                                                  )
df_base_show['show_title'] = df_base_show['title'].str.cat(
                                            df_base_show['startYear'].apply(
                                                lambda x:f'({x})'), sep =" "
                                                                           )



# III. Mise en place de l'algorithme


# 1. Détermination des poids


# 2. Définition du modèle et du calcul

dropables = ["tconst",
             "primaryTitle",
             "genres",
             "directors",
             "writers",
             "title",
             "firstActor"]


def plus_proches_films(df, tconst, nb_neighbors, my_X, algorithm ='auto'):

    modelKNN = NearestNeighbors(n_neighbors=nb_neighbors,
                                algorithm=algorithm
                                ).fit(my_X)

    neighbors = modelKNN.kneighbors(df.loc[df.tconst == tconst].drop(columns=dropables))

    titles = df_base_show[['show_title',
                           'directors',
                           'firstActor',
                           'genres',
                           'averageRating',
                           'numVotes',
                           'tconst']].loc[neighbors[1][0]]
    return titles


def image_film_choice(tconst):
    url = 'https://www.imdb.com/title/'+tconst
    html = requests.get(url)
    navigator = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1)'
    html = requests.get(url, headers={'User-Agent': navigator})
    soup = BeautifulSoup(html.text, 'html.parser')
    images = soup.find_all('img', {'src':re.compile('.jpg')})
    for image in images:
        affiche=[]
        affiche.append(image['src'])
        break
    return affiche

def title_to_tconst(full_title):
    row = df_base_show[df_base_show["show_title"] == full_title]
    tconst = row["tconst"].iloc[0]
    return tconst

