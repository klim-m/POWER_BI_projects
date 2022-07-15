import pandas as pd
import json
import requests

def get_movie_data(movie):                 #a function get relevant data for movie name from OMDB API
    base_url = 'http://www.omdbapi.com/'
    api_key = "*****"
    param = {}
    param['t'] = movie
    param['r'] = "json"
    param['apikey']= api_key
    #print(param)
    omdb_api = requests.get(base_url, params = param)
    omdb_info = json.loads(omdb_api.text)
    return omdb_info

dataset= pd.read_excel("/Queros project/Movie - Data Set for Cleaning.xlsx")    #reading file to be cleaned

for key in dataset:
    dataset[key].fillna(0, inplace = True)        #filled the blank cells with value 0 
    
dataset['DIRECTOR_facebook_likes'] = dataset['DIRECTOR_facebook_likes'].replace('"', "", regex = True)  #removing unncessary characters from title column
dataset['DIRECTOR_facebook_likes'] = dataset['DIRECTOR_facebook_likes'].astype(float)                #converting str type to float for calculations


dataset['movie_title'] = dataset['movie_title'].str.replace('?', "")      #removing unncessary characters from title column
dataset['movie_title'] = dataset['movie_title'].str.replace('ÿ', "")  

movie_list = []
for movie in dataset['movie_title']:
    movie_list.append(movie)                  #adding all movies names from data set to a seperate list

list_of_tuples= []
for movie in movie_list:                           #using the the new movie list and custom function to get up-to-date information for each movie
    movie_metadata = get_movie_data(movie)
    duration = movie_metadata['Runtime']
    duration = int(duration.replace(" min", ""))
    year = int(movie_metadata['Year'])
    imdbRating = float(movie_metadata['imdbRating'])
    gross = movie_metadata["BoxOffice"]
    gross = gross.replace("$", "")
    gross = int(gross.replace(",", ""))
    tuple1 = movie, year, duration, gross, imdbRating
    list_of_tuples.append(tuple1)
    #print(tuple1)
    #print(movie, duration, imdbRating, gross)

#print(list_of_tuples)
dataframe2 = pd.DataFrame(list_of_tuples, columns =['Movie_title', 'Year',  'Duration', 'Gross', 'imdbRating'])   #creating a new dataframe with updated information 
#print(dataframe2)

                              
dataframe3 = pd.merge(dataframe2, dataset, left_index=True, right_index= True, how='left')       #merging the 2 dataframes and deleting duplicate (old) columns 
del dataframe3['movie_title']
del dataframe3['duration']
del dataframe3['title_year.1']
del dataframe3['gross']
del dataframe3['imdb_score']

dataframe3.to_excel("Movie Data cleaning (Klimston).xlsx", index = False)            #writing the dataset to excel

dataframe3.head()