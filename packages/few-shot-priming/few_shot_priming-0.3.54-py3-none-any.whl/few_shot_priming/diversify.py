import json
import sys
import numpy as np
from sentence_transformers import *
from sklearn.neighbors import NearestCentroid
from sklearn.cluster import AgglomerativeClustering


def get_embeddings(df_training):
    model = SentenceTransformer('all-mpnet-base-v2')
    training_text = df_training["text"]
    topics = df_training["topic"].values.tolist()
    training_embeddings = model.encode(training_text.values.tolist())
    ids = df_training["id"].values.tolist()
    return training_embeddings, ids, topics

def save_embeddings(embeddings, ids, topics, path):
    ids = np.reshape(ids, (len(ids),1))
    vectors_with_ids = np.hstack((ids, embeddings))
    np.savetxt(path+"/embeddings.txt",vectors_with_ids, delimiter=",")
    with open(path+"/topics.json", "w") as file:
        json.dump(topics, file)



def load_embeddings(path):
    vectors = np.genfromtxt(path+"/embeddings.txt", delimiter=",")
    with open(path+"/topics.json", "r") as file:
        topics = json.load(file)
    return vectors[:,1:], np.uint32(vectors[:,0]), topics

def cluster(vectors, ids, **args):
    clustering = AgglomerativeClustering(**args).fit(vectors)
    labels = clustering.labels_

    clf = NearestCentroid()
    clf.fit(vectors, labels)
    samples = []

    for centriod in clf.centroids_:
        max_distance = sys.maxsize
        centroid_id=-1
        for i, vector in enumerate(vectors):
            if (np.linalg.norm(centriod-vector))<max_distance:
                max_distance = np.linalg.norm(centriod-vector)
                centroid_id= i
        samples.append((ids[centroid_id], labels[centroid_id]))

    return labels, samples


