from module import *

df_base_6 = import_local('df_base_6.csv')
df_french = import_local('df_french.csv')

df_base_frenchie = df_base_6.merge(df_french,
                                   how='right',
                                   left_on='tconst',
                                   right_on='titleId',
                                   suffixes=(None,"_y")
                                   ).drop(columns=['titleId',"title_y"])
df_base_frenchie['startYear'] = df_base_frenchie['startYear'].astype(int)
df_base_frenchie['runtimeMinutes'] = df_base_frenchie[
                                                    'runtimeMinutes'
                                                      ].astype(int)
df_base_frenchie.to_csv("df_base_frenchie.csv")