from datetime import datetime
import os
import yaml

from pathlib import Path


root_path = Path(__file__).parent

def load_config():
    """
    Load the configuration of the experiment and the model
    :return: a dictionary containing the configuration of the experiments
    """

    conf_path = Path(root_path, "conf.yaml")
    with open(conf_path) as file:
        config = yaml.safe_load(file)
        return config

def save_config(config):
    conf_path = Path(root_path, "conf.yaml")
    with open(conf_path, "w") as file:
        yaml.dump(config, file)

def get_prompting_config():
    config = load_config()
    return config["prompt"]


def get_prompt_fine_tuning():
    """
    Load the prompting approach main configuration
    :return:
    """
    config = load_config()
    return config["prompt-fine-tuning"]

def get_prompt_fine_tuning_params():
    """
    Load the prompt params to optimize  the model
    :return: a dictionary containing the params for the few shot model
    """
    prompting_config = get_prompt_fine_tuning()
    return prompting_config["params"]

def get_prompt_fine_tuning_best_params():
    """
    Load the prompting approach best params
    :return:
    """
    prompting_config = get_prompt_fine_tuning()
    return prompting_config["best-params"]

def get_experiment_paths(experiment):
    conf = load_config()
    if experiment == "ibmsc":
        path_source = Path(root_path, conf["dataset"]["path-ibmsc-root"])
    else:
        path_source = None
    path_training = Path(root_path, conf["experiment"][experiment]["path-training"])
    path_validation = Path(root_path, conf["experiment"][experiment]["path-validation"])
    path_test = Path(root_path, conf["experiment"][experiment]["path-test"])
    return path_source, path_training, path_validation, path_test


def get_baseline_params():
    config = load_config()
    return config["baseline"]["params"]

def get_baseline_config():
    config = load_config()
    config = config["baseline"]
    return config

def get_baseline_best_params():
    config = load_config()
    return config["baseline"]["best-params"]

def get_logs(experiment=None):
    config = load_config()
    home_directory = os.path.expanduser( '~' )
    now = datetime.now()
    time_now = now.strftime("%m-%d %H:%M")
    path = config["experiment"][experiment]["path-logs"].replace("time", time_now)
    return Path(home_directory, path)

def get_results_path(experiment=None, run=""):
    config = load_config()
    home_directory = os.path.expanduser( '~' )
    now = datetime.now()
    time_now = now.strftime("%m-%d %H:%M")
    path = config["experiment"][experiment]["path-results"].replace("time", time_now)
    path = path.replace("run", run)
    return Path(home_directory, path)

def get_openai_key():
    config = load_config()
    return config["openai"]["key"]

def load_topic_similarity_params():
    config = load_config()
    return config["topic-similarity"]["params"]

def get_topic_model_path(experiment, experiment_type):
    config = load_config()
    token = f"{experiment}-{experiment_type}"
    return config["topic-similarity"]["model-path"][token]

def get_similarities_path(experiment, experiment_type, model):

    config = load_config()
    token = f"{experiment}-{experiment_type}"
    return config["topic-similarity"][f"{model}-similarity-path"][token]

def dump_bow_size(experiment, experiment_type, bow_size):
    config = load_config()
    token = f"{experiment}-{experiment_type}"
    config["topic-similarity"]["bow"][token] = bow_size
    save_config(config)

def load_bow_size(experiment, experiment_type):
    config = load_config()
    token = f"{experiment}-{experiment_type}"
    return config["topic-similarity"]["bow"][token]

def get_template_path():
    conf = load_config()
    return Path(root_path, conf["prompt-fine-tuning"]["path-template"])