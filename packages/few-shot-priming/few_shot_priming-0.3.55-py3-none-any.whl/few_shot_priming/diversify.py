import json
import sys
import numpy as np
import pandas as pd
from sentence_transformers import *
from sklearn.neighbors import NearestCentroid
from sklearn.cluster import AgglomerativeClustering
from few_shot_priming.config import *
from few_shot_priming.experiments import *
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


def sample_diverse_examples(experiment, experiment_type, k):
    if experiment_type=="validation":
        validate=True
    else:
        validate=False
    dataset = load_splits(experiment, oversample=False, validate=validate)
    df_training = dataset["training"]
    embeddings, ids, topics = get_embeddings(df_training)
    labels, centroids = cluster(embeddings, ids, n_clusters=k)
    centroid_ids = [centroid[0] for centroid in centroids]
    df_diverse= df_training[df_training["id"].isin(centroid_ids)]
    return df_diverse

def save_diverse_examples(experiment, experiment_type):
    path = get_diverse_example_path(experiment, experiment_type)
    all_diverse_samples = []
    for k in [4, 8, 16, 32, 64, 128, 256]:
        df_diverse = sample_diverse_examples(experiment, experiment_type, k)
        df_diverse["k"]=k
        all_diverse_samples.append(df_diverse)
    df_all_diverse_examples = pd.concat(all_diverse_samples)
    df_all_diverse_examples.to_csv(path, sep="\t")

def sample_diverse(experiment, experiment_type, k):
    path = get_diverse_example_path(experiment, experiment_type)
    df_diverse_examples = pd.read_csv(path, sep="\t")
    return df_diverse_examples[df_diverse_examples["k"]==k]