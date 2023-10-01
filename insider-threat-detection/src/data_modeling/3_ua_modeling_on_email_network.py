# Import packages
import pandas as pd
import numpy as np
import networkx as nx
from sklearn.metrics.pairwise import cosine_similarity

# Load data
# The paper does not provide the data source, so this is a hypothetical file name
data = pd.read_csv("../../data/processed/email_truncated.csv")

# Create a list of unique users
users = data["user"].unique()

# Initialize an empty dictionary to store the networks
networks = {}

# Loop over each user
for user in users:
    # Filter the data for the user
    user_data = data[data["user"] == user]
    # Create an empty graph
    G = nx.Graph()
    # Add nodes for the user and their contacts
    G.add_nodes_from([user] + user_data["from"].unique().tolist())
    # Loop over each contact
    for contact in user_data["from"].unique():
        # Filter the data for the contact
        contact_data = user_data[user_data["from"] == contact]
        # Add an edge between the user and the contact with weight equal to the number of e-mails exchanged
        G.add_edge(user, contact, weight=len(contact_data))
    # Store the graph in the dictionary with the user as the key
    networks[user] = G

# Initialize an empty dataframe to store the features
features = pd.DataFrame()

# Loop over each user and their network
for user, G in networks.items():
    # Compute degree centrality for each node
    deg_cen = nx.degree_centrality(G)
    # Compute betweenness centrality for each node
    bet_cen = nx.betweenness_centrality(G)
    # Compute closeness centrality for each node
    clo_cen = nx.closeness_centrality(G)
    # Compute eigenvector centrality for each node
    eig_cen = nx.eigenvector_centrality(G)
    # Compute Katz centrality for each node
    katz_cen = nx.katz_centrality(G)
    # Compute PageRank for each node
    pagerank = nx.pagerank(G)
    # Compute clustering coefficient for each node
    clus_coef = nx.clustering(G)
    # Compute average neighbor degree for each node
    avg_nei_deg = nx.average_neighbor_degree(G)
    # Compute square clustering for each node
    sq_clus = nx.square_clustering(G)
    # Compute core number for each node
    core_num = nx.core_number(G)

    # Create a feature vector for the user by aggregating the values of each metric across all nodes

    feature_vector = [user,
                      np.mean(list(deg_cen.values())),
                      np.mean(list(bet_cen.values())),
                      np.mean(list(clo_cen.values())),
                      np.mean(list(eig_cen.values())),
                      np.mean(list(katz_cen.values())),
                      np.mean(list(pagerank.values())),
                      np.mean(list(clus_coef.values())),
                      np.mean(list(avg_nei_deg.values())),
                      np.mean(list(sq_clus.values())),
                      np.mean(list(core_num.values()))]
    # print(feature_vector)
    # Append the feature vector to the dataframe
    # features = features.append(pd.Series(feature_vector), ignore_index=True)
    # features = pd.concat([features, pd.DataFrame(pd.Series(feature_vector))], ignore_index=True)
    # features = pd.concat([features, pd.Series(feature_vector)], ignore_index=True)
    features = pd.concat([features, pd.Series(feature_vector).to_frame().T], ignore_index=True)

# Rename the columns of the dataframe
features.columns = ["user",
                    "degree_centrality",
                    "betweenness_centrality",
                    "closeness_centrality",
                    "eigenvector_centrality",
                    "katz_centrality",
                    "pagerank",
                    "clustering_coefficient",
                    "average_neighbor_degree",
                    "square_clustering",
                    "core_number"]

# Compute cosine similarity between feature vectors of different users
similarity_matrix = cosine_similarity(features.drop("user", axis=1))

print(features)

# Print the similarity matrix
print(similarity_matrix)
