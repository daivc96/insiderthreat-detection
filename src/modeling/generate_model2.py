# Import libraries
import pandas as pd
import gensim
from gensim import corpora
from gensim.models import LdaModel
from gensim.models.coherencemodel import CoherenceModel

# Import nltk and download stopwords
import nltk
nltk.download("stopwords")

# Read the data
df = pd.read_csv("email1.csv")

# Preprocess the text column
# You can use any text preprocessing techniques such as tokenization, lemmatization, etc.
# Here we use a simple function to split the text into words and remove punctuation, numbers, and stopwords
def preprocess(text):
    # Get the list of stopwords for English
    stopwords = nltk.corpus.stopwords.words("english")

    # Add any custom stopwords that you want
    stopwords.extend(["custom", "word"])

    words = text.split()
    words = [word.lower() for word in words if word.isalpha() and word not in stopwords]
    return words

df["words"] = df["content"].apply(preprocess)

# Create a dictionary from the words
dictionary = corpora.Dictionary(df["words"])

# Create a corpus from the dictionary and the words
# Create a corpus from the dictionary and the words variables
corpus = [dictionary.doc2bow(words) for words in df["words"]]


corpus = [doc for doc in corpus if len(doc) > 0] # Filter out the empty documents from the corpus

# Set the number of topics and the value of alpha
num_topics = 50
alpha = 1

# Build the LDA model using gensim
lda_model = LdaModel(corpus=corpus, id2word=dictionary, num_topics=num_topics, alpha=alpha, random_state=42)

# Print the topics and the top 10 words for each topic
topics = lda_model.print_topics(num_words=10)
for topic in topics:
    print(topic)

# Evaluate the model using coherence score
# coherence_model = CoherenceModel(model=lda_model, texts=df["words"], dictionary=dictionary, coherence="c_v")
# coherence_score = coherence_model.get_coherence()
# print("Coherence score:", coherence_score)

# Get the per-document topic proportions and print them for the first 10 documents in the corpus
doc_topics = lda_model.get_document_topics(corpus)
print("Document topics:")
for doc_id, doc in enumerate(corpus): # Loop over both variables using doc_id
    # Get the topic proportions for the document
    doc_topics = lda_model.get_document_topics(doc)
    # Print the topic proportions
    print(f"Document {doc_id}:")
    for topic_id, topic_prob in doc_topics:
        print(f"Topic {topic_id}: {topic_prob:.3f}")

# Get the per-topic word distributions and print them for the first 10 topics in the model
# topic_words = lda_model.get_topic_terms(range(10))
# print("Topic words:")
# for i in range(10):
#     print(f"Topic {i}:")
#     for word_id, word_prob in topic_words[i]:
#         # Get the word from the dictionary using the word id
#         word = dictionary[word_id]
#         print(f"{word}: {word_prob:.3f}")

# Create a list of column names using the range function and string formatting
column_names = [f"topic {i+1}" for i in range(50)]

# Insert "id" as the first column name
column_names.insert(0, "id")

# Create a list of row values using the doc_topics variable that we obtained from the LDA model
row_values = []

# Get the id values from the DataFrame object
id_values = df["id"].tolist()

for doc_id, doc in enumerate(corpus): # Loop over both variables using doc_id
    # Sort the topic probabilities by topic id
    doc_topics = sorted(doc_topics, key=lambda x: x[0])
    # Extract only the topic probabilities
    doc_probs = [x[1] for x in doc_topics]
    # Replace the document index with the id value from the original file email.csv
    doc_probs.insert(0, id_values[doc_id])
    # Append the row values to the list
    row_values.append(doc_probs)

# Create a DataFrame object using the column names and row values that we created
df_matrix = pd.DataFrame(row_values, columns=column_names)

# Print the DataFrame object using the print function
print(df_matrix)
