# __author__ = "Vo Chanh Dai"
# __doc__ = "This code performs topic modeling on email data using LDA"

# Import libraries
import pandas as pd
import gensim
from gensim import corpora
from gensim.models import LdaModel
from gensim.models.coherencemodel import CoherenceModel
import time
# Import nltk and download stopwords
import nltk
nltk.download("stopwords")

start_time = time.time()

# Read the data
source_file = "../../data/processed/email_truncated.csv"
df = pd.read_csv(source_file)

# Preprocess the text column
# Split the text into words and remove punctuation, numbers, and stopwords


def preprocess(text):
    # Get the list of stopwords for English
    stopwords = nltk.corpus.stopwords.words("english")

    # Add some custom stopwords
    # stopwords.extend(["custom", "word"])

    words = text.split()
    words = [word.lower()
             for word in words if word.isalpha() and word not in stopwords]
    return words


df["words"] = df["content"].apply(preprocess)

# Create a dictionary from the words
dictionary = corpora.Dictionary(df["words"])

# Create a corpus from the dictionary and the words variables
corpus = [dictionary.doc2bow(words) for words in df["words"]]

# Filter out the empty documents from the corpus and the id values
corpus = [doc for doc in corpus if len(doc) > 0]
id_values = [id for id, doc in zip(df["id"], corpus) if len(doc) > 0]

# Set the number of topics and the value of alpha
num_topics = 50
alpha = 1

# Build the LDA model using gensim
lda_model = LdaModel(corpus=corpus, id2word=dictionary,
                     num_topics=num_topics, alpha=alpha)

# Create a list of tuples containing the topic number and the list of words with their weights
topics = [(topic[0], topic[1].split("+")) for topic in lda_model.print_topics(num_words=10)]

# Create a list of lists containing the topic number and the probability for each document
doc_topics = [lda_model.get_document_topics(doc) for doc in corpus]

# Create a list of column names using the range function and string formatting
column_names = [f"topic_{i+1}" for i in range(50)]

# Insert "id" as the first column name
column_names.insert(0, "id")

# Create a list of row values using the doc_topics variable that were obtained from the LDA model
row_values = [[id_values[doc_id]] + [x[1]
                                     for x in sorted(doc_topics)] for doc_id, doc_topics in enumerate(doc_topics)]

# Create a DataFrame object using the column names and row values
df_matrix = pd.DataFrame(row_values, columns=column_names)

# Read the new dataframe from the csv file
df_true_positive = pd.read_csv("../../data/processed/true_positive_r6.2.csv")
# Merge the two dataframes on the id column using an outer join
final_df = pd.merge(df_matrix, df_true_positive, on="id", how="left")
final_df["target"] = final_df["target"].fillna(0)

# Write the dataframe to csv file
final_df.to_csv(
    "../../data/model_data/2_ua_modeling_on_email_content.csv", index=False)
# Print a confirmation message
print("The dataframe has been saved to csv file.")

end_time=time.time()
print(end_time-start_time)