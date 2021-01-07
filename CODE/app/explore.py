import base64
import streamlit as st
import altair as alt 
import geopandas as gpd
import graphviz as gv
import numpy as np
import pandas as pd
import plotly.express as px
from shapely import wkt
from vega_datasets import data
from app import ftformat as ft # import global format 

DATA_DIR = 'data'
STATIC_DIR = 'static'

def app():
    
    STATIC_DIR = 'static'
    DATA_DIR = 'data'
    
    # import css and declare local formatting variables
    ft.local_css(f"{STATIC_DIR}/styles/ftstyle.css")
    #main_color = "rgb(21, 125, 236, 0.9)"
    #st.write(ft.get_color_styles(main_color), unsafe_allow_html=True)

    #write titles
    st.image(f'{STATIC_DIR}/img/fryetag_logo_black_font.png')

    # read dataset
    #@st.cache
    def load_data():
        works = pd.read_csv(f'{DATA_DIR}/works.csv')
        #pob_df = pd.read_csv(os.path.join(DATA_DIR,'placeofbirth_df.csv'))
        pob_df = pd.read_csv(f'{DATA_DIR}/author-data/placeofbirth_df.csv')
        pob_df = pob_df.drop(['Unnamed: 0'], axis=1)
        pob_df['geometry'] = pob_df['coordinates.value'].apply(wkt.loads)
        geo_df = gpd.GeoDataFrame(pob_df, geometry='geometry')
        joined_authors = pd.read_csv(f'{DATA_DIR}/author-data/author_list.csv')
        return works, geo_df, joined_authors
    
    # define functions to the load the png and set a background image
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

    # set a background image
    set_png_as_page_bg(f'{STATIC_DIR}/img/fryetagbackground.png')
    
    # load the data
    works, pob_df, joined_authors = load_data()
    
    # place of birth data
    pob_df['geometry'] = pob_df['coordinates.value'].apply(wkt.loads)
    
    # create geo dataframe using the place of birth dataframe
    geo_df = gpd.GeoDataFrame(pob_df, geometry='geometry')
    
    # create a df of the top 20 works and clean up columns
    top_20 = works.groupby(['author'], as_index = False).count().sort_values(by = ['title'], ascending = False)[:20]
    top_20.rename(columns = {'title': 'Count of Works', 'author': 'Author'}, inplace = True)

    # setup a three-column format for layout purposes
    col1, col2, col3 = st.beta_columns((1,1,1))

    # register the custom Altair theme under a chosen name
    alt.themes.register('fryetag_theme', ft.fryetag_theme)

    # enable the newly registered theme
    alt.themes.enable('fryetag_theme')
    
    with col1:
        
        # some basic markup text to explain our app
        st.write(' ')
        st.write("Fryetag leverages the power of natural language processing along with the rich literature of Project Gutenberg to analytically derive the topics and word choices of the top 20 authors in the Project Gutenberg library")
        st.write(' ')
        st.write("Use our 'Explore by Author' page to explore each author's most common topics across all works in the Gutenberg library, or select an individual book.")
        st.write("Want to try to sound like one of the Gutenberg authors? Use our 'Sound Like The Author' page to test whether you can write text to sound like your favorite Gutenberg author.")
        st.write("Want to try our GPT2 text generator? Use our 'GPT2 Text Generator' page to test our random text generator and classifier.")
        
    with col2:
        
        # create a barchart based on the top 20 authors and their counts of works in Project Gutenberg
        sel_bar_hover = alt.selection_single(on='mouseover')
        single = alt.selection_single()
        
        works_bar = alt.Chart(top_20).mark_bar().encode(
            x='Count of Works', y = alt.Y('Author', sort='-x'), tooltip =['Author', 'Count of Works']
            , color = alt.condition(single, 'Count of Works', alt.value('gray'), legend = None)
        ).properties(
            width = 350
            , height = 400
        ).properties(
                title={
                    "text": "Top 20 Most Prolific Authors in Project Gutenberg",
                    "subtitle": "by number of works"
                }
        ).add_selection(
            single   
        )
        
        st.write(works_bar)
        
    with col3:
        
        # create the choropleth of author's places of birth
        
        geo_df.rename(columns = {'itemLabel.value':'Geo Author', 'placeofbirthLabel.value':'Place of Birth'}, inplace = True)
        joined_authors.rename(columns = {'counts_author':'Author', 'geo_author':'Geo Author'}, inplace = True)
        geo_df = pd.merge(geo_df, joined_authors, on='Geo Author') 
        geo_df = pd.merge(geo_df, top_20, on='Author') 
        
        px.set_mapbox_access_token(open(f'app/mapbox_token.txt').read())
        fig = px.scatter_mapbox(geo_df,
                                lat=geo_df.geometry.y,
                                lon=geo_df.geometry.x,
                                hover_name='Author',
                                color="Count of Works", 
                                size="Count of Works",
                                color_continuous_scale='RdBu',
                                size_max=10,
                                title="<b>Author City of Birth</b>",
                                hover_data = ['Count of Works','Place of Birth'],
                                zoom=1)
        
        fig.update_layout(
            font_family="Helvetica",
            font_color="gray",
            font_size = 14,
            title_font_family="Helvetica",
            title_font_color="#27332F",
            legend_title_font_color="gray",
            margin = dict(l=10, r= 30, t=65, b=0),
            width=600,
            height=500,
            title={
                'x':0.02
                , 'xanchor':"left"
            }
        )
        fig.update_xaxes(title_font_family="Helvetica")
        
        st.plotly_chart(fig)
        st.write('Note: Samuel Clemens (Mark Twain) was born in the city of Florida in the state of Missouri.')

