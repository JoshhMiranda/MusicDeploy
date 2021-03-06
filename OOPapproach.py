# -*- coding: utf-8 -*-
"""
Created on Mon May  3 23:07:27 2021

@author: Josh
"""

import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
from statistics import mode
from statistics import StatisticsError
import pickle


song_df_normalised = pd.read_csv("datasets/song_df_normalised.csv")
song_df_normalised.head()

pickle_in = open("nn_model2.pkl","rb")
model_nn = pickle.load(pickle_in)

global recommended_song_list
recommended_song_list =[]

def getsimilarsongs(song_name):
    
    song_features = song_df_normalised.set_index("track_name")
    #song_features.drop("Unnamed: 0",axis=1,inplace=True)
    song_features.drop(['track_artist', 'lyrics', 'track_album_name','track_popularity',
           'playlist_name', 'playlist_genre', 'playlist_subgenre','language','sentiment','song_artist','links'],axis=1,inplace=True)
    #song_features.head()
    song_features_csr = csr_matrix(song_features.values)
    #model_nn = NearestNeighbors(metric='cosine',algorithm='brute')
    model_nn.fit(song_features_csr)

    temp = song_features.copy()
    temp.reset_index(inplace=True)
    songsearch = song_name
    songsearch = songsearch.lower()
    song_index = temp.index[temp['track_name'] ==songsearch].tolist()[0]
    #print(song_index)
    #print(song_features.index[song_index])
    distances,indices = model_nn.kneighbors(X = song_features.iloc[song_index,:].values.reshape(1,-1), n_neighbors=6)

    for i in range(1,3):
        if song_features.index[indices.flatten()[i]] not in recommended_song_list:
            recommended_song_list.append(song_features.index[indices.flatten()[i]])


def getartistsongs(artist_name,song_name):
    artist_data = song_df_normalised[song_df_normalised['track_artist'] == artist_name]
    artist_song_features=artist_data.set_index("track_name")
    artist_song_features.drop(['track_artist', 'lyrics', 'track_album_name','track_popularity',
           'playlist_name', 'playlist_genre', 'playlist_subgenre','language','sentiment','song_artist','links'],axis=1,inplace=True)
    #artist_song_features.head()
    #from scipy.sparse import csr_matrix

    artist_song_features_csr = csr_matrix(artist_song_features.values)

    #model_nn = NearestNeighbors(metric='cosine',algorithm='brute')
    model_nn.fit(artist_song_features_csr)

    temp = artist_song_features.copy()
    temp.reset_index(inplace=True)
    songsearch = song_name
    songsearch = songsearch.lower()
    song_index = temp.index[temp['track_name'] ==songsearch].tolist()[0]
    #print(song_index)

    #print(artist_song_features.index[song_index])

    if artist_data.shape[0] < 6:
        n = artist_data.shape[0]
        distances,indices = model_nn.kneighbors(X = artist_song_features.iloc[song_index,:].values.reshape(1,-1), n_neighbors=n)
        for i in range(1,n): 
            recommended_song_list.append(artist_song_features.index[indices.flatten()[i]])
    else:    
        distances,indices = model_nn.kneighbors(X = artist_song_features.iloc[song_index,:].values.reshape(1,-1), n_neighbors=6)
        for i in range(1,4): 
            if artist_song_features.index[indices.flatten()[i]] not in  recommended_song_list:
                recommended_song_list.append(artist_song_features.index[indices.flatten()[i]])

 

def getsongsgenre(genre,song_name):
    genre_data = song_df_normalised[song_df_normalised['playlist_genre'] == genre]
    genre_song_features=genre_data.set_index("track_name")
    genre_song_features.drop(['track_artist', 'lyrics', 'track_album_name','track_popularity',
           'playlist_name', 'playlist_genre', 'playlist_subgenre','language','sentiment','song_artist','links'],axis=1,inplace=True)
    #genre_song_features.head()
    #from scipy.sparse import csr_matrix

    genre_song_features_csr = csr_matrix(genre_song_features.values)

    #model_nn = NearestNeighbors(metric='cosine',algorithm='brute')
    model_nn.fit(genre_song_features_csr)

    temp = genre_song_features.copy()
    temp.reset_index(inplace=True)
    songsearch = song_name
    songsearch = songsearch.lower()
    song_index = temp.index[temp['track_name'] ==songsearch].tolist()[0]
    #print(song_index)

    #print(genre_song_features.index[song_index])


    distances,indices = model_nn.kneighbors(X = genre_song_features.iloc[song_index,:].values.reshape(1,-1), n_neighbors=6)

    for i in range(1,3): 
        if genre_song_features.index[indices.flatten()[i]] not in recommended_song_list:
            recommended_song_list.append(genre_song_features.index[indices.flatten()[i]])
        

def getsongsubgenre(subgenre,song_name):
    subgenre_data = song_df_normalised[song_df_normalised['playlist_subgenre'] == subgenre]
    subgenre_song_features=subgenre_data.set_index("track_name")
    subgenre_song_features.drop(['track_artist', 'lyrics', 'track_album_name','track_popularity',
           'playlist_name', 'playlist_genre', 'playlist_subgenre','language','sentiment','song_artist','links'],axis=1,inplace=True)
    #subgenre_song_features.head()
    #from scipy.sparse import csr_matrix

    subgenre_song_features_csr = csr_matrix(subgenre_song_features.values)

    #model_nn = NearestNeighbors(metric='cosine',algorithm='brute')
    model_nn.fit(subgenre_song_features_csr)

    temp = subgenre_song_features.copy()
    temp.reset_index(inplace=True)
    songsearch = song_name
    songsearch = songsearch.lower()
    song_index = temp.index[temp['track_name'] ==songsearch].tolist()[0]
    #print(song_index)

    #print(subgenre_song_features.index[song_index])


    distances,indices = model_nn.kneighbors(X = subgenre_song_features.iloc[song_index,:].values.reshape(1,-1), n_neighbors=6)      

    for i in range(1,3): 
        if subgenre_song_features.index[indices.flatten()[i]] not in recommended_song_list:
            recommended_song_list.append(subgenre_song_features.index[indices.flatten()[i]])
        
        
        

def display():
    return  recommended_song_list


def clearlist():
    recommended_song_list.clear()


def streamhistory(username, user_search,sentiment):
    import pandas as pd
    from statistics import mode
    from statistics import StatisticsError
    #print(username, songsearch,result,accurate)
    history = pd.read_csv("datasets/streaminghistory.csv")
    #user_song = [user_search]
    #user_sentiment = [sentiment]
    
    if username in history['user'].unique():
        for i in range(history.shape[0]):
            if history.at[i,'user'] == username:
                song_list = history.at[i,'song_list']
                song_list  = user_search  +","+ song_list
                sentiment_list = history.at[i,'song_sentiment']
                sentiment_list = sentiment +","+ sentiment_list     
                history.at[i,'song_list'] = song_list
                history.at[i,'song_sentiment'] = sentiment_list
                #history.to_csv("datasets/user-review.csv",index=False)
                history.to_csv("datasets/streaminghistory.csv",index=False)
    
    
    if username not in history['user'].unique():
        df2 = pd.DataFrame({'user':[username],'song_list':[user_search], 'song_sentiment':[sentiment]})
        history = history.append(df2,ignore_index=True)
        history.to_csv("datasets/streaminghistory.csv",index=False)
    

    
    sentiment_history =history[history['user'] == username]['song_sentiment'].tolist()[0]
    sentiment_history = sentiment_history.split(",")
    
    try:
        mode(sentiment_history[:3])
    except StatisticsError:
        #print('Neutral')
        sentiment_history = 'Neutral'
    else:
        #print(mode(sentiment_history[:3]))
        sentiment_history =  mode(sentiment_history[:3])
    
    return sentiment_history
    
    
    #text = "You're cool!!"
    #return text
