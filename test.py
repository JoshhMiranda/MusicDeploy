# -*- coding: utf-8 -*-
"""
Created on Tue May  4 21:15:40 2021

@author: Josh
"""

import streamlit as st
import pandas as pd
from OOPapproach import *
import base64


def main():
    intro = " Hi! I'm MARC, short for Music Analysis and Recommender Chatbot \n (well, my devs are still working on the chatbot, so you can call me MAR)\n Would you mind spending a few minutes to test me out?"
    st.text(intro)
    username = st.text_input("Whats your name?")
    
    if username == 'devtesterMARCauthenticcationPaSSworDLJJR':
        df = pd.read_csv("datasets/user-review.csv")
        def filedownload(df):
            csv = df.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()
            href = f'<a href="data:file/csv;base64,{b64}" download="user-review.csv">Download CSV File</a>'
            return href
        
        st.markdown(filedownload(df), unsafe_allow_html=True)
        
    else:
        st.text("Nice to meet you "+str(username))
    
    userinput = st.text_input("Enter a song you would like to get recommendations for: ")
    userinput = userinput.lower()
    st.text("your song is: "+userinput)
    
    
    song_df_normalised = pd.read_csv("datasets/song_df_normalised.csv")
    
    try:
        song_name =song_df_normalised[song_df_normalised['track_name'].str.contains(userinput)]['track_name'].tolist()[0]
    
    except IndexError:
        #print("Sorry!! We couldnt get any results for", userinput, " :( ")
        string = "Sorry!! We couldnt get any results for"+ str(userinput) +" :("
        st.error(string)
        result = 'fail'
        accurate= 'no'
        user_review(username, userinput,result,accurate)
    
    else:
        result='success'
        st.text("song from dataset: "+song_name)
        
        artist_name = song_df_normalised[song_df_normalised['track_name'] == song_name]['track_artist'].tolist()[0]
        st.text("artist name:"+artist_name)    
        
        genre = song_df_normalised[song_df_normalised['track_name'] == song_name]['playlist_genre'].tolist()[0]
        #st.text("genre of song:"+genre)
        
        subgenre = song_df_normalised[song_df_normalised['track_name'] == song_name]['playlist_subgenre'].tolist()[0]
        #st.text("subgenre of song:"+subgenre)
        
        
        recommend = st.button("click for receommendations ")
        if recommend:
            getartistsongs(artist_name,song_name)
            
            
            getsongsgenre(genre,song_name)
            getsongsubgenre(subgenre,song_name)
        
            getsimilarsongs(song_name)
            output = display()
            outputlist = list(set(output))
        
            for i in range(1,len(output)):
                st.text(str(i)+" : "+output[i])
        
            clearlist()
        
        songsearch = userinput
        accurate = st.radio("Were the recommendations accurate?",['yes','no'])
        if accurate == "yes":
            st.success("Awesome")
        if accurate == 'no':
            st.error("Oh no!! We're sorry to hear that")
            
        thankyou = st.button("THANK YOU!!")
        if thankyou:
            final = user_review(username, userinput,result,accurate)
            st.text(final)
     
        
if __name__  == '__main__':
    main()
