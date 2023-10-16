import tqdm
from few_shot_priming.config import *
from few_shot_priming.experiments import *
from few_shot_priming.topic_similarity import *
from collections  import defaultdict
import fkassim.FastKassim as fkassim
import dask.dataframe as ddf
import numpy as np

def calc_syntactic_similarity(df_test, df_training):
    print(df_test.shape[0])
    #df_test = df_test.sample(10)
    #df_training = df_test
    similarities = np.zeros(((len(df_test),len(df_training))))
    FastKassim = fkassim.FastKassim(fkassim.FastKassim.LTK)
    print("parsing training")
    parsed_training = [FastKassim.parse_document(doc) for doc in df_training["text"].values]
    print("parsing test")
    parsed_test = [FastKassim.parse_document(doc) for doc in df_test["text"].values]
    similarities = defaultdict(dict)
    i=0
    j=0
    for _, test_record in df_test.iterrows():
        for _, train_record in df_training.iterrows():
            test_text = parsed_test[i]
            training_text = parsed_training[j]
            similarities[test_record["id"]][train_record["id"]] = FastKassim.compute_similarity_preparsed(test_text, training_text)
            j = j + 1
        i = i + 1
        j = 0
    return similarities

def evaluate_syntax_similarity(experiment, experiment_type, arguments_to_check):


    splits = load_splits(experiment, oversample=False)
    df_validation = splits[experiment_type]
    df_training = splits["training"]
    all_similar_examples = []
    similarities = load_similarities("ibmsc", experiment_type,"parse-tree-kernel")
    for i in range(0, arguments_to_check):
        i = np.random.randint(0,len(df_validation))
        examples_sorted, syntax_scores = sample_similar(i, similarities, df_training, df_training.shape[0])
        examples_sorted["parse-tree-kernel-score"] = syntax_scores
        queries = [df_validation["text"].iloc[i] for _ in range(0,len(df_training))]
        queries_topic = [df_validation["topic"].iloc[i] for _ in range(0,len(df_training))]
        examples_sorted["query-text"] = queries
        examples_sorted["query-topic"] = queries_topic
        all_similar_examples.append(examples_sorted.reset_index())
    df_sorted_examples = pd.concat(all_similar_examples)
    df_sorted_examples.to_csv("~/parse-tree-kernel_similarity_evaluation.csv", sep="\t", columns=["query-text", "query-topic", "text", "parse-tree-kernel-score"
                                                                                            ])