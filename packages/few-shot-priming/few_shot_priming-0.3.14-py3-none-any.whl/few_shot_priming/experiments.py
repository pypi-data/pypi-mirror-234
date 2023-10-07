import pandas as pd
import os
from few_shot_priming.config import *
from few_shot_priming.topic_similarity import *

def save_splits():
    """
    Save the splits of the experiments by sampling a validation set from the training set with exclusive topic sets
    :return:
    """
    path_source, path_training, path_validation, path_test = get_experiment_paths()
    df_arguments = pd.read_csv(path_source, sep=",", encoding="utf-8")
    df_training = df_arguments[df_arguments["split"] == "train"]
    df_test = df_arguments[df_arguments["split"] == "test"]
    training_topics = df_training["topicTarget"].sample(12).unique()
    training_topics = training_topics[:10]
    df_sampled_training = df_training[df_training["topicTarget"].isin(training_topics)]
    df_validation = df_training[~df_training["topicTarget"].isin(training_topics)]
    df_sampled_training.to_csv(path_training, sep=",", encoding="utf-8", index=False)
    df_validation.to_csv(path_validation, sep=",", encoding="utf-8", index=False)
    df_test.to_csv(path_test, sep=",", encoding="utf-8", index=False)


def oversample_dataset(df, experiment):
    if experiment == "ibmsc":
        pro_claims = df[df["claims.stance"]=="PRO"]
        con_claims = df[df["claims.stance"]=="CON"]
        count_of_con_to_sample = pro_claims.shape[0] - con_claims.shape[0]
        pro_claims_to_add = con_claims.sample(count_of_con_to_sample)
        return pd.concat([df, pro_claims_to_add])
    else:
        pro_claims = df[df["label"]==1]
        con_claims = df[df["label"]==0]
        neutral_claims = df[df["label"]==2]
        count_of_pro_to_sample = con_claims.shape[0] - pro_claims.shape[0]
        count_of_neutral_to_sample = con_claims.shape[0] - neutral_claims.shape[0]
        pro_claims_to_add = pro_claims.sample(count_of_pro_to_sample)
        neural_claims_to_add = neutral_claims.sample(count_of_neutral_to_sample, replace=True)
        return pd.concat([df, pro_claims_to_add, neural_claims_to_add])

def adapt_ibmsc(df):
    labels = {"PRO": 1, "CON":0}
    df["stance"] = df["claims.stance"].apply(lambda x: labels[x])
    df = df [["topicText", "claims.claimCorrectedText", "stance", "claims.claimId"]]
    df.rename(columns={"topicText" : "topic", "claims.claimCorrectedText": "text", "claims.claimId": "id"}, inplace=True)
    return df[["topic", "stance", "text", "id"]]

def adapt_vast(df):
    df = df [["topic_str", "text_s", "label", "new_id"]]
    df.rename(columns={"topic_str":"topic", "text_s": "text", "label": "stance", "new_id":"id"}, inplace=True)
    #df["topic"] = df["topic"].apply(lambda topic: " ".join(topic))
    return df[["topic", "stance", "text", "id"]]

def load_splits(experiment, oversample=True, validate=True, best_split=False, adapt=True):
    """
    Load the splits of the experiments and return it in a dictionary of pandas dataframes
    :return: a dictionary containing the training, validation, and test splits
    """
    if experiment == "ibmsc":
        dataset_id="claims.claimId"
    else:
        dataset_id = "new_id"
    path_source, path_training, path_validation, path_test = get_experiment_paths(experiment)
    if experiment == "ibmsc" and not os.path.exists(path_validation):
        save_splits()
    df_training = pd.read_csv(path_training, sep=",", encoding="utf-8")
    df_validation = pd.read_csv(path_validation, sep=",", encoding="utf-8")
    df_test = pd.read_csv(path_test, sep=",", encoding="utf-8")
    if not validate and experiment =="ibmsc":
        df_training = pd.concat([df_training, df_validation])
    dataset = {"training": df_training, "validation": df_validation, "test": df_test}

    if best_split:
        df_trianing = dataset["training"]
        print(df_trianing["best-split"].value_counts())
        df_trianing["best-split"] = df_trianing["best-split"].astype(bool)
        df_training = df_trianing[df_trianing["best-split"]]

        dataset["training"] = df_training

    elif oversample:
        dataset["training"] = oversample_dataset(dataset["training"], experiment)
    else:
        pass
    for split in dataset:
        dataset[split].sort_values(by=dataset_id, inplace=True)
    if adapt:
        for split in dataset:
            if experiment == "ibmsc":
                dataset[split] = adapt_ibmsc(dataset[split])
            else:
                dataset[split] = adapt_vast(dataset[split])
    return dataset


def sample_few_shots(test_instance_index, df_training, size, similarities, similar=True):
    """
    Sample few shots from the training dataframe. The few shots can be filtered by using a specific boolean functions and sorted
    :param df_training: a dataframe containing the whole training split
    :param size: the size of the few shots to use for training
    :param filter: a boolean function that takes a record of the trianing split and decided whether to include or not
    :param sort_criteria: a dicionary specifing the name of the column and the sorting order used to sort the few shot examples
    :return: a dataframe containing the sampled few shots
    """

    if similar:
        examples, scores = sample_similar(test_instance_index, similarities, df_training, size)
    else:
        examples, socres = sample_diverse(test_instance_index, similarities, df_training, size)
    return examples
