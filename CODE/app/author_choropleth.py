import streamlit as st
import pandas as pd
import numpy as np
import datetime
import re
import joblib
import json
from dateutil import parser
import os
import plotly.graph_objects as go
import plotly.express as px
import geopandas as gpd
import booste
import streamlit.components.v1 as components
from app import ftformat as ft
from app import load_gutenberg
import base64

# streamlit run streamlit_chengb.py --server.port 5998


# st.title('Fryetag')
def app():
    is_local = False
    STATIC_DIR = 'static'
    DATA_DIR = 'data'
    ft.local_css(f'{STATIC_DIR}/styles/ftstyle.css')
    
    st.title('GPT2 Text Generator')

    @st.cache(allow_output_mutation=True)
    def load_data():
        result_df, count_df, geo_df, joined_authors = load_gutenberg.load_text_data()
        return result_df, count_df, geo_df, joined_authors

   # data_load_state = st.text('Loading data...')
    result_df, count_df, geo_df, joined_authors = load_data()
    #data_load_state.text("Done! (using st.cache)")

    with open('app/booste_api.json') as f:
        data = json.load(f)
        booste_api = data['booste_api']
        
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

    # st.subheader('Try it out')
    st.markdown("""GPT2 is the acronym for Generative Pre-trained Transformer 2.<br>
    We are leveraging OpenAI's smaller version (117 Million parameters).<br> 
    It generates then next "n" words in a work.<br>
    In this case we chose 15 next words.<br> 
    Please use this button below to see how generated text performs with our ML model
    """, unsafe_allow_html=True)
    submit = st.button('Try it out using generated sentences from GPT2!')

    if is_local:
        path = 'C:\\Users\\bchen\\Desktop\\Georgia Tech - M.S. Analytics\\CSE 6242\\Team-Breaking-Bad\\lit-nlp\\bcheng66\\trained-models'
        ldavis_path = 'C:\\Users\\bchen\\Desktop\\Georgia Tech - M.S. Analytics\\CSE 6242\\Team-Breaking-Bad\\lit-nlp\\dkim884\\LDA_htmls'
    else:
        path = f'{DATA_DIR}/trained-models'
        ldavis_path = f'{DATA_DIR}/LDA_htmls'

    for file in os.listdir(path):
        if file.endswith(".pkl") and file.startswith("voting"):
            voting_model_path = os.path.join(path, file)

    if submit:
        try:
            sample_text = result_df[result_df.author.isin(count_df.author)]\
            .text.iloc[np.random.randint(len(result_df[result_df.author.isin(count_df.author)]), size=(1))[0]][0:1000]
        except:
            sample_text = result_df[result_df.author.isin(count_df.author)]\
            .text.iloc[np.random.randint(len(result_df[result_df.author.isin(count_df.author)]), size=(1))[0]]
        out_list = booste.gpt2(booste_api, sample_text, 15)
        out_string = " ".join(out_list)
        voting_model = joblib.load(voting_model_path)
        y_pred = voting_model.predict(pd.Series([out_string]))
        st.text(out_string)
        # st.text(y_pred)
        joined_author = joined_authors[joined_authors.counts_author.isin(y_pred)]['geo_author'].values[0]
        joined_html = joined_authors[joined_authors.counts_author.isin(y_pred)]['lda_file'].values[0]
        geo_subset_df = geo_df[geo_df['itemLabel.value'] == joined_author]
        image_loc = geo_subset_df['pic.value'].values[0]
        st.image(image_loc, width = 225, caption=y_pred[0])

        author_freq = px.bar(count_df[count_df.author.isin(y_pred)], x='author',y='title_count', color="author",
                    labels={
                        "author": "Author",
                        "title_count": "Count of Works"
                    },
                    title="Project Gutenberg Top 20 Authors")
        st.plotly_chart(author_freq)

        px.set_mapbox_access_token(open('app/mapbox_token.txt').read())
        fig = px.scatter_mapbox(geo_subset_df,
                                lat=geo_subset_df.geometry.y,
                                lon=geo_subset_df.geometry.x,
                                hover_name='itemLabel.value',
                                title="Author City of Birth",
                                zoom=1)
        st.plotly_chart(fig)
        st.markdown("""Note: Samuel Clemens (Mark Twain) was born in the city of Florida in the state of Missouri.
        """, unsafe_allow_html=True)
        html_name = os.path.join(ldavis_path, joined_html)
        HtmlFile = open(html_name, 'r', encoding='utf-8')
        html_string = HtmlFile.read()
        components.html(html_string, height=1000, width=1000, scrolling=True)
    else:
        author_freq = px.bar(count_df, x='author',y='title_count',  color="author",
                    labels={
                        "author": "Author",
                        "title_count": "Count of Works"
                    },
                    title="Project Gutenberg Top 20 Authors")
        st.plotly_chart(author_freq)

        px.set_mapbox_access_token(open('app/mapbox_token.txt').read())
        fig = px.scatter_mapbox(geo_df,
                                lat=geo_df.geometry.y,
                                lon=geo_df.geometry.x,
                                hover_name='itemLabel.value',
                                title="Author City of Birth",
                                zoom=1)
        st.plotly_chart(fig)
        st.markdown("""Note: Samuel Clemens (Mark Twain) was born in the city of Florida in the state of Missouri.
        """, unsafe_allow_html=True)
