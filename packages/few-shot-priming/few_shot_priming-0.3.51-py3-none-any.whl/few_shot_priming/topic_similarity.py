import math

import nltk
import os
import json
import numpy as np
from contextualized_topic_models.models.ctm import CombinedTM
from contextualized_topic_models.utils.data_preparation import TopicModelDataPreparation
from contextualized_topic_models.utils.preprocessing import WhiteSpacePreprocessingStopwords
from contextualized_topic_models.evaluation.measures import CoherenceNPMI,InvertedRBO
from nltk.corpus import stopwords as stop_words
from few_shot_priming.prompting_stance import *
from few_shot_priming.experiment import *
from few_shot_priming.topic_similarity_sentence_transformer import *
from scipy.spatial.distance import cosine
from collections import defaultdict
os.environ["TOKENIZERS_PARALLELISM"] = "false"

def preprocess_dataset(df):
    stopwords = list(stop_words.words("english"))
    documents = list(df["text"])
    #documents = list(df.groupby("claims.article.rawFile", as_index = False).agg({"claims.claimCorrectedText": "\n".join})["claims.claimCorrectedText"])
    sp = WhiteSpacePreprocessingStopwords(documents, stopwords_list=stopwords)
    preprocessed_documents, unpreprocessed_corpus, vocab, retained_indices = sp.preprocess()
    return preprocessed_documents, unpreprocessed_corpus, vocab, retained_indices


def create_topic_model(df_test, topic_model_params):
    """
    Create a contexutlaized topic model and save it in mode-path as saved in conf.yaml
    :param df_test:
    :param topic_count: count of dimensions of the topic model
    :param epcohs: count of iterations to train the topic model for
    :return:
    """
    preprocessed_documents, unpreprocessed_corpus, vocab, retained_indices = preprocess_dataset(df_test)
    tp = TopicModelDataPreparation("all-mpnet-base-v2")
    training_dataset = tp.fit(text_for_contextual=unpreprocessed_corpus, text_for_bow=preprocessed_documents)
    #training_dataset = tp.transform(text_for_contextual=unpreprocessed_corpus, text_for_bow=preprocessed_documents)
    bow_size = len(tp.vocab)
    ctm = CombinedTM(bow_size=bow_size, **topic_model_params)
    ctm.fit(training_dataset)
    return ctm, bow_size

def dump_model(model,  topic_model_path):
    model.save(models_dir=topic_model_path)

def load_topic_model(topic_model_params, bow_size, topic_model_path):
    ctm = CombinedTM(bow_size=bow_size, **topic_model_params)
    models_dirs = os.listdir(topic_model_path)
    if len(models_dirs)>1:
        raise Exception("there are multiple saved models delete all but the one you want")
    ctm.load(os.path.join(topic_model_path,models_dirs[0]), epoch=topic_model_params["num_epochs"]-1)
    return ctm

def load_similarities(experiment, experiment_type, model="ctm"):
    path_similarities = get_similarities_path(experiment, experiment_type, model)
    with open(path_similarities, "r") as file:
        similarities= json.load(file)
    similarities_with_int_idices = {}
    for key in similarities:
        similarities_with_int_idices[int(key)]= {}
    for key in similarities:
        for train_key in similarities[key]:
            similarities_with_int_idices[int(key)][int(train_key)] = similarities[key][train_key]
    return similarities_with_int_idices


def save_similarities(experiment, experiment_type, similarities, model="ctm"):
    path_similarities = get_similarities_path(experiment, experiment_type, model)
    with open(path_similarities, "w") as file:
        json.dump(similarities, file )

def evaluate_model(experiment, experiment_type, arguments_to_check, baseline=False):
    """
    :param model: contextual topic model to be evaluated

    """
    similarities = load_similarities(experiment, experiment_type)
    if experiment_type =="validation":
        validate=True
    else:
        validate=False
    splits = load_splits(experiment, validate=validate, oversample=False)
    df_validation = splits[experiment_type]
    df_training = splits["training"]
    if baseline:
        sentence_transformer_similarities = load_similarities(experiment, experiment_type, model="sentence-transformer")
        #lda_similarities = calc_similarity_lda(df_validation, df_training)
    all_similar_examples = []
    arguments_to_check = df_validation.sample(arguments_to_check)
    for i, argument_record in arguments_to_check.iterrows():
        i = np.random.randint(0,len(df_validation))

        examples_sorted, ctm_scores = sample_similar(argument_record["id"], similarities, df_training, df_training.shape[0])
        examples_sorted.rename(columns={"text":"ctm-text", "topic":"ctm-topic"}, inplace=True)
        examples_sorted["ctm-score"] = ctm_scores
        sentence_transformer_examples, sentence_transformer_score = sample_similar(argument_record["id"], sentence_transformer_similarities, df_training, df_training.shape[0])
        sentence_transformer_examples.rename(columns={"text":"sentence-transformer-text", "topic":"sentence-transformer-topic"}, inplace=True)
        sentence_transformer_examples["sentence-transformer-score"] = sentence_transformer_score
        # lda_examples, lda_scores = sample_similar(i, lda_similarities, df_training, df_training.shape[0])
        # lda_examples.rename(columns={"text":"lda-text", "topic":"lda-topic"},inplace=True)
        # lda_examples["lda-score"] = lda_scores
        queries = [argument_record["text"] for _ in range(0,len(df_training))]
        queries_topic = [argument_record["topic"] for _ in range(0,len(df_training))]
        examples_sorted["query-text"] = queries
        examples_sorted["query-topic"] = queries_topic
        all_similar_examples.append(pd.concat([examples_sorted.reset_index(), sentence_transformer_examples.reset_index()], axis=1))

    df_sorted_examples = pd.concat(all_similar_examples)
    df_sorted_examples.to_csv(f"~/contexutal_topic_model_{experiment_type}_evaluation.csv", sep="\t", columns=["query-text", "query-topic",
                                                                    "ctm-text", "ctm-topic", "ctm-score", "sentence-transformer-text",
                                                                                            "sentence-transformer-topic", "sentence-transformer-score"])



def calc_all_similarity(df_train, df_test, model):
    df_all = pd.concat([df_test, df_train])
    preprocessed_all_documents, unpreprocessed_all_corpus, _, retained_indices= preprocess_dataset(df_all)
    preprocessed_training_documents, unpreprocessed_training_corpus,_, _= preprocess_dataset(df_train)
    tp = TopicModelDataPreparation("all-mpnet-base-v2")
    tp.fit(text_for_contextual=unpreprocessed_training_corpus, text_for_bow=preprocessed_training_documents)
    dataset = tp.transform(text_for_contextual=unpreprocessed_all_corpus, text_for_bow=preprocessed_all_documents)
    vectors = model.get_doc_topic_distribution(dataset, n_samples=20)
    remvoed_indices = [index for index in range(0, len(df_all)) if index not in retained_indices]
    removed_vector = np.ones_like(vectors[0])
    for index in remvoed_indices:
        vectors= np.vstack([vectors[0:index], removed_vector, vectors[index:]])
    test_vectors = vectors[:df_test.shape[0]]
    training_vectors = vectors[df_test.shape[0]:]
    similarities = defaultdict(dict)
    test_indices = df_test["id"].values.tolist()
    training_indices = df_train["id"].values.tolist()
    for i, test_vector in enumerate(test_vectors):
        test_index = test_indices[i]
        for j, training_vector in enumerate(training_vectors):
            train_index = training_indices[j]
            if (test_vector == removed_vector).all() or (training_vector == removed_vector).all():
                similarities[test_index][train_index] = 0
            else:
                similarities[test_index][train_index] = 1 - cosine(test_vector, training_vector)
    return similarities

def sample_similar(test_index, similarities, df_training, few_shot_size):
    test_hashmap = similarities[test_index]
    items = sorted(test_hashmap.items(),key=lambda x: -x[1])
    most_similar = items[:few_shot_size]
    most_similar_indices = [x[0] for x in most_similar]
    most_similar_dict = dict(most_similar)
    df_few_shots=df_training[df_training["id"].isin(most_similar_indices)]
    df_few_shots["score"] = df_few_shots["id"].apply(lambda x: most_similar_dict[x])
    df_few_shots.sort_values("score", inplace=True, ascending=False)
    return df_few_shots, df_few_shots["score"]

def sample_diverse(test_index, similarities, df_training, few_shot_size):
    indices = np.argsort(similarities[test_index, :])
    all_training_size = len(indices)
    step = math.floor(all_training_size/few_shot_size)
    indices_of_indices = range(0,all_training_size,step)
    diverse_indices = indices[indices_of_indices]
    diverse_indices = diverse_indices[:few_shot_size]
    return df_training.iloc[diverse_indices],  similarities[test_index, diverse_indices]

