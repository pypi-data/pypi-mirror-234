import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer, util
from gensim.corpora import Dictionary
from gensim.models import LdaModel
from nltk import word_tokenize
from nltk.corpus import stopwords
from scipy.spatial.distance import cosine

def calc_similarity_sentence_transformer(df_test, df_training):
    model = SentenceTransformer('all-mpnet-base-v2')
    test_text = df_test["text"]
    training_text = df_training["text"]
    test_embeddings = model.encode(test_text)
    training_embeddings = model.encode(training_text)
    cosine_scores = util.cos_sim(test_embeddings, training_embeddings)
    return np.absolute(cosine_scores)

def remove_stopwords_and_tokenize(text):
    my_stopwords = set(stopwords.words("english"))
    tokens = word_tokenize(text)  # tokenize
    tokens = [t for t in tokens if not t in my_stopwords]  # Remove stopwords
    tokens = [t for t in tokens if len(t) > 1]  # Remove short tokens
    return tokens

def calc_similarity_lda(df_test, df_training):
    test_text = []
    test_tokens=[]
    training_text = []
    training_tokens = []
    for i,record in df_test.iterrows():
        text= record["text"]
        tokens=remove_stopwords_and_tokenize(text)
        test_text.append(text)
        test_tokens.append(tokens)

    for i, record in df_training.iterrows():
        text = record["text"]
        tokens = remove_stopwords_and_tokenize(text)
        training_text.append(text)
        training_tokens.append(tokens)

    dictionary = Dictionary(test_tokens)
    #dictionary.filter_extremes(no_below=20, no_above=0.2)
    test_corpus = [dictionary.doc2bow(doc) for doc in test_tokens]
    train_corpus = [dictionary.doc2bow(doc) for doc in training_tokens]
    num_topics = 20
    lda_model = LdaModel(corpus=test_corpus, id2word=dictionary, num_topics=num_topics, random_state=100,
                         chunksize=200, passes=1000)
    similarities = np.zeros(((len(test_corpus)), len(train_corpus)))

    for i, doc_test in enumerate(test_corpus):
        for j, doc_training in enumerate(train_corpus):
            distribution_test = lda_model[doc_test]
            distribution_test_vector = np.zeros(num_topics)
            distribution_training_vector = np.zeros(num_topics)
            for entry in distribution_test:
                distribution_test_vector[entry[0]] = entry[1]
            distribution_training = lda_model[doc_training]
            for entry in distribution_training:
                distribution_training_vector[entry[0]] = entry[1]
            similarities[i,j] = cosine(distribution_test_vector, distribution_training_vector)

    return similarities