# -*- coding: utf-8 -*-

import nltk
from nltk.sentiment.vader import  SentimentIntensityAnalyzer
import streamlit as st
import pandas as pd
import base64
from SongRecommendation import *
from ArtistSearch import *
from GenreSearch import *
from Playlist import *

def main():
    st.title("MARC")
    
    registration = pd.read_csv("datasets/registration.csv")
    history = pd.read_csv("datasets/streaminghistory.csv")
    
    st.sidebar.header("Log in/ Sign up")
    selection = st.sidebar.selectbox("Log In/ Sign Up", 
                        ['Home','Log In', 'Sign Up'])

    st.sidebar.text(selection)
    
    
    if selection == 'Home':
        st.text("Hi there! Meet MARC. MARC is here to celebrate your victories, \npump you up to survive those workouts, make chores a little less monotonous, \ncry with you when you've got to let it out, you name it, MARCs got it. \nMARC recommends you songs based on its conversation with you. With a few keyboard clicks, \nMARC hand picks the best among a plethora of songs.")
        st.text("Sign up if you're new here or log in if you already have an account!!")
    
    
    if selection == 'Log In':
        st.sidebar.info('log in tab')
        name = st.sidebar.text_input("Enter Username")
        password = st.sidebar.text_input("Enter Password",type='password')
        c = 0
        
        login = st.sidebar.checkbox("Log In!!")
        if login:
            if (name == 'devtesterMARCauthenticcationPaSSworDLJJR') and (password =='devtesterMARCauthenticcationPaSSworDLJJR'):
                st.header('Admin Panel')
                st.subheader('Registered Users:')
                df1 = registration[['username']]
                st.write(df1)
                
                admininput = st.text_input('enter user name: ')
                if admininput in history['user'].unique():
                    for i in range(history.shape[0]):
                        if history.at[i,'user'] == admininput:
                            history_list = history.at[i,'song_list']
                            df2 = pd.DataFrame({'history':[history_list]})
                            st.write(df2)
                
                
            
            elif name in registration['username'].unique():
                for i in range(registration.shape[0]):
                    if (registration.at[i,'username'] == name) and (registration.at[i,'password'] == password):
                        name = registration.at[i,'username']
                        st.sidebar.success("hello "+name)
                        c = 1
                        #username = name
                        optionfunction(name)
                if c ==0:
                    st.sidebar.error("Invalid username or password!!")
                        
                        
            elif name not in registration['username'].unique():
                    st.sidebar.error("No account, please sign up")
        
    
    elif selection == 'Sign Up':
        st.info("Sign Up tab ( Please use a unique username )")
        name = st.text_input("Enter Username")
        password = st.text_input("Enter Password",type='password')
        c = 0
        signup = st.button("Sign Up!!")
        if signup:

            
            
            if name in registration['username'].unique():
                for i in range(registration.shape[0]):
                    if registration.at[i,'username'] == name and registration.at[i,'password'] == password:
                        #st.error('Please choose anothet')
                        st.error("Account for "+name+" already exists, please login")
                        c = 1
    
            if name in registration['username'].unique():
                if c == 0:
                    st.warning('please select a different username') 
            
            else:
                if name not in registration['username'].unique():
                    df2 = pd.DataFrame({'username':[name],'password':[password]})
                    registration = registration.append(df2,ignore_index=True)
                    registration.to_csv("datasets/registration.csv",index=False)
                    st.success("Success!!")
                    st.info("Go to log in!!!")
    
    
    
def optionfunction(username):  
    intro = "Hi there! Meet MARC. MARC is here to celebrate your victories, \npump you up to survive those workouts, make chores a little less monotonous, \ncry with you when you've got to let it out, you name it, MARCs got it. \nMARC recommends you songs based on its conversation with you. With a few keyboard clicks, \nMARC hand picks the best among a plethora of songs."
    st.text(intro)
    #username = st.text_input("Whats your name?")
 
#    if username == 'devtesterMARCauthenticcationPaSSworDLJJR':
#        st.info("Suppp")
#        df = pd.read_csv("datasets/user-review.csv")
#        def filedownload(df):
#            csv = df.to_csv(index=False)
#            b64 = base64.b64encode(csv.encode()).decode()
#            href = f'<a href="data:file/csv;base64,{b64}" download="user-review.csv">Download CSV File</a>'
#            return href
        
#        st.markdown(filedownload(df), unsafe_allow_html=True)
        
#    else:
#        st.text("Nice to meet you "+str(username))
    
#   mood = st.text_input("How are you today "+str(name)+"?")
#    score = SentimentIntensityAnalyzer().polarity_scores(mood)
#    if score['compound'] >= 0.05:
#            st.success('Positive Sentiment Detected')
#            sentiment = 'Positive'
#    elif score['compound'] > -0.05 and score['compound'] < 0.05:
#            st.info('Neutral Sentiment Detected')
#            sentiment = 'Neutral'
#    elif score['compound'] <= -0.05:
#            st.error('Negative Sentiment Detected')
#            sentiment = 'Negative'
  
    
  
    st.text("Lets get you started "+str(username)+"!")
    option = st.selectbox("What would you like to do?", 
                          ['Search Artist','Play Music','Browse by genre','get playlist'])
    
    st.text(option)
    #gorecommend = st.button("go: ")
    #if gorecommend:
    if option == 'Play Music':
        songrecommender(username)
    if option == 'Search Artist':
        artistsearch()        
     
    if option == 'Browse by genre':
        genresearch()
    
    if option == 'get playlist':
        personalplaylist(username)
  
    
if __name__  == '__main__':
    main()
