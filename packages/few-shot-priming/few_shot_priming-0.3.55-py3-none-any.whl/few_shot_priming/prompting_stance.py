import logging
import random

import pandas as pd
import openprompt
import os
import openai
openai.api_key = ""

import torch
import wandb

from argparse import ArgumentParser

from joblib import Memory
from sklearn.metrics import accuracy_score
from openprompt.prompts import ManualTemplate, ManualVerbalizer
from openprompt import PromptForClassification, PromptDataLoader
from openprompt.data_utils import InputExample
from openprompt import plms
from openprompt.plms import *

from sklearn.metrics import accuracy_score, f1_score

from transformers import AdamW, get_linear_schedule_with_warmup, GPTJForCausalLM
from transformers import BertTokenizer, BertModel, T5Tokenizer, T5Model, AutoTokenizer, AutoModelForCausalLM
from transformers import DebertaModel, DebertaTokenizer, GPT2Tokenizer, GPT2Model, GPT2LMHeadModel, DebertaForSequenceClassification
from transformers import OPTConfig, OPTModel, BertForSequenceClassification, AutoModelWithLMHead, LlamaTokenizer, LlamaConfig
from transformers import set_seed

from torch.nn import CrossEntropyLoss
from transformers import GPTJConfig, GPTJForCausalLM

from torch.optim import SGD
from few_shot_priming.config import *
from few_shot_priming.experiments import *
from few_shot_priming.mylogging import *
from few_shot_priming.topic_similarity import *
from few_shot_priming.topic_similarity_sentence_transformer import *
use_cuda = torch.cuda.is_available()

plms._MODEL_CLASSES["wxjiao/alpaca-7b"]= ModelClass(**{"config": LlamaConfig, "tokenizer": LlamaTokenizer, "model": AutoModelForCausalLM,
                                           "wrapper": LMTokenizerWrapper})
plms._MODEL_CLASSES["EleutherAI/gpt-j-6B"]= ModelClass(**{"config": GPTJConfig, "tokenizer": GPT2Tokenizer, "model": GPTJForCausalLM,
                                           "wrapper": LMTokenizerWrapper})


def init_reproducible(seed):

    set_seed(seed)
    #torch.use_deterministic_algorithms(True)
    #torch.manual_seed(42)


openai.api_key = get_openai_key()



def convert_to_prompt_splits(dataset, config, sample=True):
    """
    Conver the pandas dataframes to splits as specified by the openprompt api
    :param dataset: a dictionary containing the trianing, validation, and test dataframes
    :return: a dictionary containing lists of input examples as specified by the openprompt api
    """
    prompt_splits = {}
    prompt_splits["test"] = []
    prompt_splits["training"] = []
    prompt_splits["validation"] = []
    for key in dataset.keys():
        if key == "training" and sample:
                dataset["training"] = dataset["training"].sample(config["few-shot-size"])
        for i,record in dataset[key].iterrows():
            prompt_splits[key].append(InputExample(guid= i , text_a = record["text"], text_b = record["topic"], label = record["stance"]))

    return prompt_splits

def checkpoint(model, filename):
    torch.save(model.state_dict(), filename)

def resume(model, filename):
    model.load_state_dict(torch.load(filename))

def save_pre_trained_model():
    """
    Saving pretrained model to use huggingface transformers without internet
    """
    config = load_config()
    config = config["pre-trained-models"]
    path = Path(config["path"])
    bert_path = os.path.join(path,"bert-base-uncased")
    if not os.path.exists(bert_path):
        bert = BertForSequenceClassification.from_pretrained('bert-base-uncased')
        berttokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        bert.save_pretrained(bert_path)
        berttokenizer.save_pretrained(bert_path)


    gpt_2_path = os.path.join(path, "gpt2-xl")
    if not os.path.exists(gpt_2_path):
        gpt_2_tokenizer = GPT2Tokenizer.from_pretrained('gpt2-xl')
        gpt_2_model = GPT2Model.from_pretrained('gpt2-xl')
        gpt_2_model.save_pretrained(gpt_2_path)
        gpt_2_tokenizer.save_pretrained(gpt_2_path)

    deberta_path = os.path.join(path, "microsoft/deberta-base")
    if not os.path.exists(deberta_path):
        deberta_tokenizer = DebertaTokenizer.from_pretrained("microsoft/deberta-base")
        deberta_model = DebertaForSequenceClassification.from_pretrained("microsoft/deberta-base")
        deberta_tokenizer.save_pretrained(deberta_path)
        deberta_model.save_pretrained(deberta_path)
    alpaca_path  = os.path.join(path, "wxjiao/alpaca-7b")

    if not os.path.exists(alpaca_path) and torch.cuda.is_available():
        device = torch.device("cpu")
        alpaca_tokenizer = AutoTokenizer.from_pretrained("wxjiao/alpaca-7b")
        alpaca_model = AutoModelForCausalLM.from_pretrained("wxjiao/alpaca-7b", device_map="auto")

        alpaca_tokenizer.save_pretrained(alpaca_path)
        alpaca_model.save_pretrained(alpaca_path)
    geo_neox_path = os.path.join(path, "EleutherAI/gpt-neox-20b")
    if not os.path.exists(geo_neox_path) :

        gptneox_tokenizer = AutoTokenizer.from_pretrained("EleutherAI/gpt-neox-20b")
        gptneox_model = AutoModelForCausalLM.from_pretrained("EleutherAI/gpt-neox-20b").half().cuda()

        gptneox_tokenizer.save_pretrained(geo_neox_path)
        gptneox_model.save_pretrained(geo_neox_path)

def my_load_plm(model_name, model_path, specials_to_add = None):
    model_class = get_model_class(plm_type = model_name)
    model_config = model_class.config.from_pretrained(model_path)
    # you can change huggingface model_config here
    # if 't5'  in model_name: # remove dropout according to PPT~\ref{}
    #     model_config.dropout_rate = 0.0
    if 'gpt' in model_name: # add pad token for gpt
        specials_to_add = ["<pad>"]
        # model_config.attn_pdrop = 0.0
        # model_config.resid_pdrop = 0.0
        # model_config.embd_pdrop = 0.0
    #model = model_class.model.from_pretrained(model_path, config=model_config, device_map = 'auto').half()
    model = model_class.model.from_pretrained(model_path, config=model_config, device_map = 'auto', load_in_8bit=True, torch_dtype=torch.float16, )
    tokenizer = model_class.tokenizer.from_pretrained(model_path)
    wrapper = model_class.wrapper


    model, tokenizer = add_special_tokens(model, tokenizer, specials_to_add=specials_to_add)

    if 'opt' in model_name:
        tokenizer.add_bos_token=False
    return model, tokenizer, model_config, wrapper

def create_few_shot_model(config, experiment, offline=True):
    """
    Prepare an openprompt model based on the configuration
    :param config: a dictionary specifing the name and type of the model
    :return: an openprompt modle, a wrapper class, a tokenizer, and a template
    """
    model_name = config["model-name"]

    if offline:
        model_type = Path(config["model-path"])
    else:
        model_type = config["model-type"]
    if experiment == "vast":
        classes = [0, 1, 2]
        label_words = {0: ["con"], 1: ["pro"], 2 : ["neutral"]}
    else:
        classes = [0, 1]
        label_words = {0: ["con"], 1: ["pro"]}
    plm, tokenizer, model_config, WrapperClass = my_load_plm(model_name, model_type)

    promptTemplate = ManualTemplate(
        text = 'On the topic {"placeholder":"text_b"} the argument {"placeholder":"text_a"} has the stance {"mask"}.',
        tokenizer = tokenizer,
    )
    promptVerbalizer = ManualVerbalizer(
        classes = classes,
        label_words = label_words,
        tokenizer = tokenizer,
    )

    promptModel = PromptForClassification(template = promptTemplate, plm=plm, verbalizer=promptVerbalizer, freeze_plm=False)
    if use_cuda:
        promptModel = promptModel.cuda()
    return promptModel, WrapperClass, tokenizer, promptTemplate



def run_experiment_prompt_fine_tuning(config=None, experiment="ibmsc", params=None, offline=False, validate=True,
                                      splits=None, logger = None, save=False, sampling_strategy=None, similarity=None):
    """
    Run a validation experiment or a test experiment
    :param validate: a boolean flag specifying whether to run a validation or  test experiment
    :return:
    """
    #if offline:
    #    save_pre_trained_model()




    log_memory_usage(logger, "begining")
    batch_size = params["batch-size"]
    lr = params["learning-rate"]
    epochs_num = params["epochs"]
    if not splits:
        splits = load_splits(experiment, oversample=False, validate=validate)
        #splits["validation"] = splits["validation"].sample(16) # REEEEEEMEBEr
        prompt_dataset = convert_to_prompt_splits(splits, config)
    else:
        prompt_dataset = convert_to_prompt_splits(splits, config, sample=False)

    log_memory_usage(logger, "loaded-split")
    promptModel, WrapperClass, tokenizer, promptTemplate = create_few_shot_model(config, experiment=experiment, offline=offline)
    log_memory_usage(logger, "created model and tokenizer")
    train_data_loader = PromptDataLoader(dataset = prompt_dataset["training"], tokenizer=tokenizer, template=promptTemplate,
        tokenizer_wrapper_class=WrapperClass, batch_size=batch_size, truncate_method="head", max_seq_length=256, decoder_max_length=3)
    log_memory_usage(logger, "created training data loadert")
    if validate:
        experiment_type = "validate"
        test_data_loader = PromptDataLoader(dataset = prompt_dataset["validation"], tokenizer = tokenizer, template = promptTemplate,
            tokenizer_wrapper_class=WrapperClass, batch_size=batch_size, truncate_method="head", max_seq_length=256, decoder_max_length=3)
        log_memory_usage(logger, "created validation data loadert")
    else:
        experiment_type = "test"
        test_data_loader = PromptDataLoader(dataset = prompt_dataset["test"], tokenizer = tokenizer, template = promptTemplate,
            tokenizer_wrapper_class=WrapperClass, batch_size=batch_size, truncate_method="head", max_seq_length=256, decoder_max_length=3)
        log_memory_usage(logger, "created test data loadert")

    loss_func = CrossEntropyLoss()
    no_decay = ['bias', 'LayerNorm.weight']
    optimizer_grouped_parameters = [
        {'params': [p for n, p in promptModel.named_parameters() if not any(nd in n for nd in no_decay)], 'weight_decay': 0.01},
        {'params': [p for n, p in promptModel.named_parameters() if any(nd in n for nd in no_decay)], 'weight_decay': 0.01}
    ]
    path_model_fine_tuned = config["model-path-fine-tuned"]

    optimizer = AdamW(optimizer_grouped_parameters, lr=float(lr))
    #optimizer = SGD(promptModel.parameters(), lr=float(lr))

    log_memory_usage(logger, "created optimizer")
    metrics = {}
    best_accuracy =  0
    best_f1 = 0
    best_epoch = 0
    best_metrics = None
    for epoch in range(epochs_num):
        tot_loss = 0
        for step, inputs in enumerate(train_data_loader):
            if use_cuda:
                inputs = inputs.cuda()
            promptModel.train()

            logits = promptModel(inputs)
            log_memory_usage(logger, "inference on inputs")
            labels = inputs["label"]
            loss = loss_func(logits, labels)
            log_memory_usage(logger, "loss = loss_func(logits, labels)")
            loss.backward()
            log_memory_usage(logger, "loss.backward()")
            tot_loss += loss.item()
            optimizer.step()
            optimizer.zero_grad()
            if step % 100 == 1:
                log_message(logger, "Epoch {}, average loss: {}".format(epoch, tot_loss/(step+1)), level=logging.INFO)
            metrics["train/loss"] = tot_loss/(step+1)
            wandb.log(metrics)
        promptModel.eval()
        test_loss = 0
        all_test_labels = []
        all_test_preds = []
        for step, test_inputs in enumerate(test_data_loader):
            if use_cuda:
                test_inputs = test_inputs.cuda()
            test_logits = promptModel(test_inputs)
            test_labels = test_inputs["label"]
            all_test_labels.extend(test_labels.cpu().tolist())
            all_test_preds.extend(torch.argmax(test_logits, dim = -1).cpu().tolist())
            loss = loss_func(test_logits, test_labels)
            test_loss += loss.item()
            metrics[f"{experiment_type}/loss"] = test_loss/(step+1)
            wandb.log(metrics)
        accuracy = accuracy_score(all_test_labels, all_test_preds)
        metrics[f"{experiment_type}/accuracy"] = accuracy
        if experiment == "vast":
            f1s = f1_score(all_test_labels, all_test_preds, average=None, labels=[0, 1, 2])
            neutral_f1 = f1s[2]
            metrics[f"{experiment_type}/neutral-f1"] = neutral_f1
        else:
            f1s = f1_score(all_test_labels, all_test_preds, average=None, labels=[0, 1])

        con_f1 = f1s[0]
        pro_f1 = f1s[1]

        macro_f1 = f1_score(all_test_labels, all_test_preds, average="macro")
        metrics[f"{experiment_type}/pro-f1"] = pro_f1
        metrics[f"{experiment_type}/con-f1"] = con_f1

        metrics[f"{experiment_type}/macro-f1"] = macro_f1
        if macro_f1 > best_f1:
            best_metrics = metrics
            best_f1 = macro_f1
            best_epoch = epoch
            torch.save({"model_state_dict":promptModel.state_dict()}, path_model_fine_tuned)
        metrics[f"{experiment_type}/epoch"] = best_epoch
    log_message(logger, f"best epoch is {best_epoch}", level=logging.WARNING)
    log_metrics(logger, best_metrics, level=logging.WARNING)
    metrics["score"] = best_metrics[f"{experiment_type}/accuracy"]
    wandb.log(metrics)
    return metrics["score"]


def predict_three_labels(resulting_string):
    resulted_string_truncated = resulting_string[-15:].lower()
    if "pro" in resulted_string_truncated or "support" in resulted_string_truncated or "positive" in resulted_string_truncated:
        return 1
    elif "con" in resulted_string_truncated or "against" in resulted_string_truncated or "negative" in resulted_string_truncated:
        return 0
    else:
        return 2

def predict_two_labels(resulting_string):

    resulted_string_truncated = resulting_string[-15:].lower()
    print(resulted_string_truncated)
    if "pro" in resulted_string_truncated or "support" in resulted_string_truncated or "positive" in resulted_string_truncated:
        return 1
    else:
        return 0

def chunker(seq, size):
    for pos in range(0, len(seq), size):
        print(pos, pos+size)
        if pos + size > len(seq):
            yield seq.iloc[pos:len(seq)]
        else:
            yield seq.iloc[pos:pos + size]

memory = Memory("cachedir")
@memory.cache
def prompt_openai(model, prompt):
    response = openai.Completion.create(model=model,
                                        prompt=prompt,
                                        max_tokens= 3,temperature=0)
    resulted_string_truncated = response["choices"][0]["text"]
    return resulted_string_truncated



def format_examples(dataset, tokenizer, labels_text_map, token_limit, logger):

    examples = ""
    for i, train_record in dataset.iterrows():
        sentence = train_record["text"].lower()
        tokens = tokenizer.encode(sentence)

        if len(tokens) > token_limit:
            sentence = tokenizer.decode(tokens[:token_limit])
        topic = train_record["topic"].lower()
        stance = train_record["stance"]
        log_message(logger, f"{topic} {stance}", level=logging.INFO)
        label = labels_text_map[stance]
        idx = random.randint(0, len(label)-1)
        template = f"On the topic '{topic}' the argument '{sentence}' has the stance {label[idx]}.\n"
        examples = examples + template

    return examples


def run_experiment_prompting(config=None, experiment="ibmsc", offline=False, validate=True, splits=None, logger=None, openai=False, sampling_strategy=None, similarity=None):


    few_shot_size = config["few-shot-size"]
    batch_size = config["batch-size"]
    labels_text_map = {0: ["con", "negative", "against"], 1: ["pro", "positive", "support" ],  2: ["neutral"] }
    if not splits:
        splits = load_splits(experiment, oversample=False, validate=validate)
    else:
        training_dataset = splits["training"]
    if validate:
        experiment_type = "validation"
    else:
        experiment_type = "test"
    test_dataset = splits[experiment_type]

    #test_dataset = test_dataset.sample(16)
    if not openai:
        #save_pre_trained_model()
        if offline:
            model_name = config["model-path"]
        else:
            model_name = config["model-name"]
        log_message(logger, f"{model_name} loaded", logging.INFO)
        if "alpaca" in model_name:
            tokenizer = LlamaTokenizer.from_pretrained(model_name)
        else:
            tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name, device_map = 'auto')
        model_is_on_cuda = next(model.parameters()).is_cuda
        log_message(logger,f"model is on cuda {model_is_on_cuda}", logging.INFO)
        if use_cuda and not model_is_on_cuda:
            model= model.cuda()
    template_size = 30
    model_input_limit = config["model-input-limit"]
    token_limit = model_input_limit//(few_shot_size+1)
    token_limit = token_limit - template_size
    print(token_limit)
    predictions = []

    labels = []

    if sampling_strategy:
        log_message(logger, f"sapling strategy {sampling_strategy}", logging.INFO)
        similarities = load_similarities(experiment=experiment, experiment_type=experiment_type, model=similarity)
    #i = 0
    for i, record in test_dataset.iterrows():
        print(i)
        prompt = "Given are the following examples:\n"
        if not sampling_strategy:
            training_dataset = splits["training"].sample(few_shot_size)
            training_dataset.sort_values("topic", inplace=True)
        elif sampling_strategy == "similar":
            training_dataset = sample_few_shots(record["id"], splits["training"], few_shot_size, similarities, similar=True)
            print(training_dataset.shape[0])
        else:
            training_dataset = sample_few_shots(record["id"], splits["training"], few_shot_size, similarities, similar=False)

        examples = format_examples(training_dataset, tokenizer, labels_text_map, token_limit, logger)
        prompt =  prompt + examples + "Find the stance of the following argument: \n"


        sentence = record["text"].lower()
        topic = record["topic"].lower()
        label = record["stance"]
        template_no_stance = f"On the topic '{topic}' the argument '{sentence}' has the stance"
        prompt_to_predict = prompt + template_no_stance
        log_message(logger, prompt_to_predict, level=logging.INFO)
        labels.append(label)
        if openai:

            completion = prompt_openai("text-davinci-003", prompt_to_predict)
            log_message(logger, completion, logging.INFO)
            resulted_string_truncated = completion[-15:].lower()
        else:
            seq = tokenizer.encode(prompt_to_predict, return_tensors="pt")
            if use_cuda:
                seq = seq.cuda()
            generated = model.generate(seq, max_new_tokens=1, )
            resulting_string = tokenizer.decode(generated.tolist()[0])
            log_message(logger, resulting_string, level=logging.INFO)
            resulted_string_truncated = resulting_string[-15:].lower()
        if "pro" in resulted_string_truncated or "support" in resulted_string_truncated or "positive" in resulted_string_truncated:
            predictions.append(1)
        elif "con" in resulted_string_truncated or "against" in resulted_string_truncated or "negative" in resulted_string_truncated:
            predictions.append(0)
        else:
            predictions.append(2)
        #i = i + 1

    log_message(logger, f"predictions {predictions}", level=logging.WARNING)
    log_message(logger, f"labels {labels}", level=logging.WARNING)
    accuracy = accuracy_score(labels, predictions)
    metrics = {}
    if experiment == "vast":
        f1s = f1_score(labels, predictions, average=None, labels=[0, 1, 2])
        neutral_f1 = f1s[2]
        metrics[f"{experiment_type}/neutral-f1"] = neutral_f1
    else:
        f1s = f1_score(labels, predictions, average=None, labels=[0, 1])
    con_f1 = f1s[0]
    pro_f1 = f1s[1]

    macro_f1 = f1_score(labels, predictions, average="macro")

    metrics[f"{experiment_type}/pro-f1"] = pro_f1
    metrics[f"{experiment_type}/con-f1"] = con_f1

    metrics[f"{experiment_type}/macro-f1"] = macro_f1
    metrics[f"{experiment_type}/accuracy"] = accuracy

    log_metrics(logger, metrics, level=logging.WARNING)
    return metrics
