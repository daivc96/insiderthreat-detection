# user activity modeling based on email

# Import packages
import pandas as pd
import numpy as np
import gensim
import gensim.corpora as corpora
from gensim.models import CoherenceModel
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Load data
data = pd.read_csv("email_data.csv") # The paper does not provide the data source, so this is a hypothetical file name

# Preprocess data
def preprocess(data):
    # Convert to lowercase and remove punctuation
    data = data.str.lower().str.replace("[^\w\s]", "")
    # Tokenize and remove stopwords
    stop_words = stopwords.words("english")
    data = data.apply(lambda x: [word for word in x.split() if word not in stop_words])
    # Lemmatize
    lemmatizer = WordNetLemmatizer()
    data = data.apply(lambda x: [lemmatizer.lemmatize(word) for word in x])
    return data

data = preprocess(data["email_content"])

# Create dictionary and corpus
dictionary = corpora.Dictionary(data)
corpus = [dictionary.doc2bow(text) for text in data]

# Build LDA model with 10 topics
lda_model = gensim.models.LdaMulticore(corpus=corpus,
                                       id2word=dictionary,
                                       num_topics=10,
                                       random_state=100,
                                       chunksize=100,
                                       passes=10,
                                       per_word_topics=True)

# Print the topics
for idx, topic in lda_model.print_topics(-1):
    print("Topic: {} \nWords: {}".format(idx, topic))
