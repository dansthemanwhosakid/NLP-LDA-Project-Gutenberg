import base64
import datetime
from dateutil import parser
from io import StringIO
import joblib
import json
import os
import re
import altair as alt 
import booste
import geopandas as gpd
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
import streamlit.components.v1 as components 
from app import ftformat as ft # import global format 
from app import load_gutenberg

DATA_DIR = 'data'
STATIC_DIR = 'static'

def app():
    
    STATIC_DIR = 'static'
    DATA_DIR = 'data'
    LDA_HTML_DIR = 'data/LDA_htmls'
    voting_model_path = f'{DATA_DIR}/trained-models/voting-clf_model.pkl'
    
    # import css and declare local formatting variables
    ft.local_css(f"{STATIC_DIR}/styles/ftstyle.css")
    main_color = "rgb(21, 125, 236, 0.9)"
    #st.write(ft.get_color_styles(main_color), unsafe_allow_html=True)
    
    # read dataset
    @st.cache(allow_output_mutation=True)
    def load_data():
        #works = pd.read_csv(f'{DATA_DIR}/works.csv')
        #authorbirthplaces = pd.read_csv(f'{DATA_DIR}/placeofbirth_df.csv')
        result_df, count_df, geo_df, joined_authors = load_gutenberg.load_text_data()
        return result_df, count_df, geo_df, joined_authors
    
    # functions to help load a background image
    def get_base64_of_bin_file(bin_file):
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    
    def set_png_as_page_bg(png_file):
        bin_str = get_base64_of_bin_file(png_file)
        page_bg_img = '''
        <style>
        body {
        background-image: url("data:image/png;base64,%s");
        background-size: cover;
        }
        </style>
        ''' % bin_str
    
        st.markdown(page_bg_img, unsafe_allow_html=True)
        return

    # load the background image
    set_png_as_page_bg(f'{STATIC_DIR}/img/fryetagbackground.png')
    
    # write titles and logos 
    #st.image('FryeTag Logo (Basic) 2.png')
    st.title('Sound Like The Author')
    st.header('Think you can sound like your favorite author?')
    st.write('Try typing your own text to see if you can sound like your favorite author using our fryetag model.')
    
    # create columns for layout
    col1, col2 = st.beta_columns((1,2))
    
    # create column 1
    with col1:
        
        # create list of methods to select from, then create a selectbox to choose from
        #methods = ['Your Own Text', 'Fryetag Random Sentence Generator']
        #method_select = st.selectbox('Choose a Method:' , methods)
        
        # instatiate a predicted author string
        predicted_author = None
        
        # if statement to check which method was selected
        #if method_select == methods[0]:
        txtinput = st.text_area('Type a sentence or short paragraph here, then press Ctrl + Enter','')

        if len(txtinput) > 0:
            voting_model = joblib.load(voting_model_path)
            predicted_author = list(voting_model.predict(pd.Series([txtinput])))[0]

        # if the predicted_author is filled in, then create the output to tell the user who they sound like
        if predicted_author:
            author_split = predicted_author.split(" ",1)
            author_first = author_split[0].lower()
            author_last_sentence = author_split[1]
            author_last_lower = author_split[1].lower()
            st.write('You sound a lot like {0}! Want to sound even more like {1}? Try regaling your friends with the topics and words to the right.'.format(predicted_author, author_last_sentence))
        
    with col2:
        
        # if there's a predicted author, create an html source string and display the html file for that author (from all works, not a specific work)
        if predicted_author:
            
            author_cleaned = predicted_author.lower().replace(" ","_").replace("'","_")
            src = f'{LDA_HTML_DIR}/{author_cleaned}_LDA.html'

            # open the file
            with open(src, 'r') as f:
                html_string = f.read()

            # render as an html component
            components.html(html_string,
                    height=1000, width = 1600
                )
        
    
   
