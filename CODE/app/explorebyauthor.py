import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import altair as alt 
from app import ftformat as ft # import global format 
import graphviz as gv
from vega_datasets import data
import streamlit.components.v1 as components 
import geopandas as gpd
from shapely import wkt
import base64

DATA_DIR = 'data'
STATIC_DIR = 'static'

def app():

    STATIC_DIR = 'static'
    DATA_DIR = 'data'
    LDA_HTML_DIR = 'data/LDA_htmls'
    
    # import css and declare local formatting variables
    ft.local_css(f"{STATIC_DIR}/styles/ftstyle.css")
    main_color = "rgb(21, 125, 236, 0.9)"

    #write titles
    #st.image('logo.png')
    st.title('Explore by Author')
    
    
    # read dataset
    @st.cache
    def load_data():
        works = pd.read_csv(f'{DATA_DIR}/works.csv')
        authorbirthplaces = pd.read_csv(f'{DATA_DIR}/author-data/placeofbirth_df.csv')
        joined_authors = pd.read_csv(f'{DATA_DIR}/author-data/author_list.csv')
        return works, authorbirthplaces, joined_authors
    
    # define functions to load a png and make it a background image
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

    # set the background image
    set_png_as_page_bg(f'{STATIC_DIR}/img/fryetagbackground.png')
    
    # load the data
    works, pob_df, joined_authors = load_data()
    
    # create a df of the top 20 works
    top_20 = works.groupby(['author'], as_index = False).count().sort_values(by = ['title'], ascending = False)[:20]
    
    # create two columns for layout purposes
    col1, col2 = st.beta_columns((1,3))
    
    with col1:
    
        # create a list of a unique set of the top_20 authors, then sort alphabetically and make a selectbox for it
        authors = list(set(list(top_20['author'])))
        authors.sort()
        author_select = st.selectbox('Please select an author' , authors)

        # take the selected author and mutate the string to fit within a variety of later formats needed for string output
        author_split = author_select.split(" ",1)
        author_first = author_split[0].lower()
        author_last_sentence = author_split[1]
        author_last = author_split[1].lower()
        
        # create list of authors works, sort the list, then create a drop-down selectbox for them
        authors_works = list(set(list(works[works.author == author_select]['title'])))
        authors_works.sort()
        authors_works.insert(0,"All of {0}'s works in the PG collection".format(author_last_sentence))
        title_select = st.selectbox('Select a title' , authors_works)
        
        # show author's image
        pob_df = pob_df.rename(columns = {'itemLabel.value':'geo_author'})
        author_join = joined_authors[joined_authors.counts_author == author_select]['geo_author'].values[0]
        author_image = pob_df[pob_df['geo_author'] == author_join]['pic.value'].values[0]
        st.image(author_image, width = 225)
        
    with col2:

        # instatiate a source string that we'll use to load our HTML
        src = str 
         
        # if we're selecting the all option, just use the author's file and render the HTML
        if title_select == authors_works[0]:
            author_cleaned = author_select.lower().replace(" ","_").replace("'","_")
            src = f'{LDA_HTML_DIR}/{author_cleaned}_LDA.html'
            st.subheader("{0}'s Most Common Topics".format(author_select))
            st.write('Hover over a topic or word to interact')
            
            # open the file
            try: 
                with open(src, 'r') as f:
                    html_string = f.read()

                # render as an html component
                components.html(html_string,
                        height=1000, width = 1600
                    )
            except:
                st.write("Sorry, we seem to have misplaced {0}'s topics. Maybe they're under that stack of books over there...".format(author_last_sentence))
         
        # if we're selecting a particular work, use the particular work's file path and render the HTML
        elif title_select != authors_works[0]:
            author_cleaned = author_select.lower().replace(" ","_").replace("'","")
            work_cleaned = title_select.lower().replace(";","").replace("   "," ").replace("$","").replace("_","").replace("'","").replace(",","").replace("!","").replace("-","").replace("&","").replace("(","").replace(")","").replace(" ","_")
            src = f'{LDA_HTML_DIR}/ALL_LDA_htmls/{author_cleaned}/{work_cleaned}.html'
            st.subheader("The Most Common Topics of {0} by {1}".format(title_select, author_select))
            st.write('Hover over a topic or word to interact')
            
            # open the file
            try: 
                with open(src, 'r') as f:
                    html_string = f.read()

                # render as an html component
                components.html(html_string,
                        height=1000, width = 1600
                    )
            except:
                st.write("Sorry, we seem to have misplaced {0}'s details. Maybe they're under that stack of books over there...".format(title_select))
            
        
        
        
        
        
