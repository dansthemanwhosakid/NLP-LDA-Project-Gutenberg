## Georgia Tech NLP Classification and Clustering Project

The [Fryetag Final Report](https://github.com/dansthemanwhosakid/NLP-LDA-Project-Gutenberg/blob/main/DOC/team083report.pdf) contains a thorough explanation of the project and details the steps taken in the group's approach in classifying and clustering thousands of books from University of Michigan's Project Gutenberg dataset. 

The [Fryetag Poster](https://github.com/dansthemanwhosakid/NLP-LDA-Project-Gutenberg/blob/main/DOC/team083poster.pdf) is a summary of the project. 

### FryeTag
An app for visualizing and analyzing plots and characters in books, screenplays
and more.

### DESCRIPTION

The package consists of all files apart from data (downloaded during installation) that are necessary to run FryeTag. 
FryeTag is a unique tool that helps users visualize large unstructured datasets, namely books. There are three notebooks contained in this folder.
`01_authors_pipeline.ipynb` cleans text from the Project Gutenberg dataset. It then extracts the names of the top 20 most prolific authors.
a resulting dataframe is created which contains the name of the author, title of the book(s), and text for each book. The results dataframe is cleaned further and readied for processing.
SPARQL is used to find author's place of birth and coordinates for our map, which are saved into a dataframe.
A CSV file is then created wich will hold the count of books per author, geographic coordinates, and LDA files.
Train test split is then used on the authors with a voting classifier to classify who wrote a subset of text. This is pickled and saved in the trained-models folder.

In the next file, `02_LDA_top_20_authors.ipynb`, the results dataframe is loaded. A custom stopwords file is imported and the results are tokenized.
LDA visualizations are then generated and the LDA_html files are saved.

Lastly, `03_LDA_per_book.ipynb` does roughly the same thing as `02_LDA_top_20_authors.ipynb`, but on each book written by an author. 
The previous file was run on all works by a given author.

### INSTALLATION
1. Download the Gutenberg dataset by going to https://web.eecs.umich.edu/~lahiri/gutenberg_dataset.html and clicking “Link to Dataset”
2. Move the Gutenberg folder to the CODE folder
3. cd to the CODE folder
4. Create a virtual environment and actiavate it according to your preference (e.g. conda, pyenv, etc.)
5. Install from the requirements.txt
    a. pip install -r requirements.txt --user (conda)
    b. pip install -r requirements.txt (pyenv)
6. Download the data folder from http://52.3.206.37:8002/data.zip 
7. Unzip and move the data folder to the CODE folder
    a. Alternative Option: To create the data folder for the streamlit app from scratch: run the Jupyter Notebooks .ipynb files in sequential order. Warning: this process will take around 6 hours.
      i. 01_authors_pipeline.ipynb
      ii. 02_LDA_top_20_authors.ipynb
      iii. 03_LDA_per_book.ipynb
7. Please sign up for a free API Key at booste.io https://www.booste.io/pretrained-models/python3#key (Does not work on Firefox. Will work on Chrome. If you are having issues consider changing your browser.)
8. Create 'booste_api.json' within app/ folder with key as "booste_api" and value as the copied API key as a string such as below
    a. {"booste_api":"put key here"}
9. Please sign up for a free Mapbox account at mapbox https://account.mapbox.com/
10. Copy the default access token and create 'mapbox_token.txt' and paste value in txt file within app/ folder
11. streamlit run fryetag.py --server.port 8501
12. In your browser, go to http://localhost:8501
    a. Note: the user can specify the port when passing the --server.port parameter just make sure the localhost address is aligned


### EXECUTION
If not already in the lit-nlp dir, cd there. Then run "streamlit run fryetag.py"

1. In your browser, go to http://localhost:8501
2. The landing page gives you an overview of the top authors in 
   Project Gutenberg and their places of birth
3. Click on 'Explore by Author' in the left sidbar. select authors and titles as
   you like to see the top 10 clusters of words from their works
4. Click on 'Sound Like the Author' in the left sidebar. Enter in some text.
   One fun idea is to put in "Elementary, my dear Watson." and press ctrl+Enter.
   You sound like Sir Arthur Conan Doyle! Have fun trying out sounding like
   other of the top authors.
5. Click on 'GPT2 text generator' in the left sidebar. Click on the 'Try it out
   using generated sentences from GPT2!' button. This takes a few seconds to
   run, so just be patient. Under the button, you will see a phrase that should
   resemble something the author might have said based on their works.

INSTALL RUN THROUGH (demo is if you are cloning the repo) https://youtu.be/XR-F7NCmFlI
