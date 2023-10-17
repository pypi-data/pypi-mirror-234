from itertools import permutations
from statistics import stdev
from few_shot_priming.prompting_stance import *

def analzye_few_shots_order(params=None, offline=False, validate=True):
    """
    run a few shot experiment using different permutations of the same samples and calculates the standard deviation
    of the validation accuracy
    :param params: parameters of the model to be run which as a dictionary
    :param offline: whether an access to internet is available or not
    :param validate: a boolean that indicates whether the experiment is a validation or test
    :return:
    """
    splits = load_splits()
    df_training = splits["training"]
    few_shot_size = params["few-shot-size"]
    df_few_shots = sample_few_shots(df_training, few_shot_size)
    index = range(few_shot_size)
    print(index)
    all_permutations = permutations(index)
    all_scores = []
    for permutation in all_permutations:
        permutation = list(permutation)
        df_sorted_few_shots = df_few_shots.iloc[list(permutation)]
        new_splits={}
        new_splits["training"] = df_sorted_few_shots
        new_splits["test"] = splits["test"]
        new_splits["validation"] = splits["validation"]
        score = run_experiment_prompting(params, offline, validate, new_splits)
        all_scores.append(score)
    print(f"standard deviation is {stdev(all_scores)}")
    return all_scores