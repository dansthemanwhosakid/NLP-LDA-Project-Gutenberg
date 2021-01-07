DATA_DIR = 'data'
def load_text_data():
    import pandas as pd
    from shapely import wkt
    import geopandas as gpd
    import os
    is_local = False
    if is_local:
        fpath = 'C:\\Users\\bchen\\Desktop\\Georgia Tech - M.S. Analytics\\CSE 6242\\Team-Breaking-Bad\\lit-nlp\\bcheng66\\author-data'
    else:
        fpath = 'data/author-data'
    result_df = pd.read_csv(os.path.join(fpath,'result_df.csv'))
    counts = result_df.author.value_counts().nlargest(20)
    counts_df = pd.DataFrame({'author':counts.index, 'title_count':counts.values})
    pob_df = pd.read_csv(os.path.join(fpath,'placeofbirth_df.csv'))
    pob_df = pob_df.drop(['Unnamed: 0'], axis=1)
    pob_df['geometry'] = pob_df['coordinates.value'].apply(wkt.loads)
    geo_df = gpd.GeoDataFrame(pob_df, geometry='geometry')
    joined_authors = pd.read_csv(os.path.join(fpath,'author_list.csv'))
    return result_df, counts_df, geo_df, joined_authors
