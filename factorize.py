# I. Import des bibliotheques et dataframes

from module import import_local # Fonction personnelle pour charger des DF
from sklearn.neighbors import NearestNeighbors # L'algorithme utilisé

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

facteurs = {"actorCategory": 1,
            "is_title_french":1,
            "numVotes": 1/1000,
            "averageRating": 500,
            "startYear": 1,
            "genres": 1000
            }

for genre in unique_genres:
    facteurs[genre] = facteurs["genres"]

for category, facteur in facteurs.items():
    df_factorized[category] *= facteur

# 2. Définition du modèle et du calcul

dropables = ["tconst",
             "primaryTitle",
             "genres",
             "directors",
             "writers",
             "title",
             "firstActor"]

X = df_factorized.drop(columns=dropables)
y = df_factorized["tconst"]

def plus_proches_films(tconsts, nb_neighbors, X, algorithm ='auto'):

    modelKNN = NearestNeighbors(n_neighbors=nb_neighbors,
                                algorithm=algorithm
                                ).fit(X)
    if isinstance(tconsts, str):
        neighbors = modelKNN.kneighbors(
            df_factorized.loc[df_factorized.tconst == tconsts].drop(
                                                            columns=dropables
                                                                   )
                                       )
        titles = df_base_show[['show_title',
                               'directors',
                               'firstActor',
                               'genres',
                               'averageRating',
                               'numVotes',
                               'tconst']].loc[neighbors[1][0]]
        return titles
    else:
        for tconst in tconsts:
            plus_proches_films(tconst, nb_neighbors, X, algorithm=algorithm)
        
        
        
# IV. Tests        
       
 
algorithms = ['brute', 'kd_tree', 'ball_tree', 'auto']

liste_test = ['tt1853728',
              'tt0172495',
              'tt0372784',
              'tt0361748',
              'tt0102926',
              'tt0993846',
              'tt0848228',
              'tt1446714',
              'tt0144084',
              'tt0796366',
              'tt0073195',
              'tt0936501',
              'tt5052448',
              'tt3460252',
              'tt0234215',
              'tt0162222',
              'tt0413300',
              'tt0469494',
              'tt3783958',
              'tt0119488',
              'tt0120735',
              'tt8579674',
              'tt0120363',
              ]        

def tester(algorithms, liste_test):
    for algorithm in algorithms:
        print(f"{algorithm=}")
        for film in liste_test:
            print(plus_proches_films(film, 4, X, algorithm)["show_title"])

#tester(algorithms, liste_test)