import os
import os.path as osp
import sys
import torch
import transformers
import json
import logging
from few_shot_priming.config import *
from datasets import load_dataset
from datasets import Dataset,DatasetDict
from few_shot_priming.experiments import *
from sklearn.metrics import accuracy_score,f1_score
from torch.utils.data import DataLoader
from transformers import  LlamaForCausalLM, LlamaTokenizer, GenerationConfig
from typing import Union, List
from peft import (LoraConfig, get_peft_model, get_peft_model_state_dict, prepare_model_for_int8_training, set_peft_model_state_dict,)
from few_shot_priming.mylogging import *
from few_shot_priming.topic_similarity import *
def generate_prompt(instruction, input=None):
    if input:
        return f"""Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.
### Instruction:
{instruction}
### Input:
{input}
### Response:"""
    else:
        return f"""Below is an instruction that describes a task. Write a response that appropriately completes the request.
### Instruction:
{instruction}
### Response:"""


def generate_instructions(dataset):
    data = {"instruction":[], "input":[], "output":[]}
    mapper = {0:"CON", 1:"PRO"}
    for i, record in dataset.iterrows():
        topic = record["topic"]
        stance = mapper[record["stance"]]
        text = record["text"]
        data["instruction"].append(f"Find the stance of the following argument on the topic")
        data["output"].append(stance)
        data["input"].append(f"Topic: {topic}\n Argument: {text}")
    return data


def generate_and_tokenize_datasets(data, prompter, tokenizer, cutoff_len, train_on_inputs=True, add_eos_token=False):

    def generate_and_tokenize_prompt(data_point):
        full_prompt = prompter.generate_prompt(
            data_point["instruction"],
            data_point["input"],
            data_point["output"],
        )
        tokenized_full_prompt = tokenize(full_prompt, tokenizer)
        if not train_on_inputs:
            user_prompt = prompter.generate_prompt(
                data_point["instruction"], data_point["input"]
            )
            tokenized_user_prompt = tokenize(
                user_prompt, tokenizer, add_eos_token=add_eos_token, cutoff_len=cutoff_len
            )
            user_prompt_len = len(tokenized_user_prompt["input_ids"])

            if add_eos_token:
                user_prompt_len -= 1

            tokenized_full_prompt["labels"] = [
                                                  -100
                                              ] * user_prompt_len + tokenized_full_prompt["labels"][
                                                                    user_prompt_len:
                                                                    ]  # could be sped up, probably
        return tokenized_full_prompt
    train_data = data["training"].map(generate_and_tokenize_prompt)
    val_data = data["validation"].map(generate_and_tokenize_prompt)
    test_data = data["test"].map(generate_and_tokenize_prompt)
    return train_data, val_data, test_data

def prepare_dataset(dataset, prompter, tokenizer, cutoff_len, few_shot_size=None):
    huggingface_dataset = {}
    if few_shot_size:
        huggingface_dataset["training"] = dataset["training"].sample(few_shot_size)
    for split in dataset:
        huggingface_dataset[split] = generate_instructions(dataset[split])
    data = DatasetDict()
    # using your `Dict` object
    for k,v in huggingface_dataset.items():
        data[k] = Dataset.from_dict(v)
    train_data, val_data, test_data = generate_and_tokenize_datasets(data, prompter, tokenizer, cutoff_len=cutoff_len)
    return train_data, val_data, test_data

def tokenize(prompt, tokenizer, cutoff_len=256, add_eos_token=True):
    # there's probably a way to do this with the tokenizer settings
    # but again, gotta move fast
    result = tokenizer(
        prompt,
        truncation=True,
        max_length=cutoff_len,
        padding=False,
        return_tensors=None,
    )
    if (
            result["input_ids"][-1] != tokenizer.eos_token_id
            and len(result["input_ids"]) < cutoff_len
            and add_eos_token
    ):
        result["input_ids"].append(tokenizer.eos_token_id)
        result["attention_mask"].append(1)

    result["labels"] = result["input_ids"].copy()

    return result



class Prompter(object):
    __slots__ = ("template", "_verbose")

    def __init__(self, template_name: str = "", verbose: bool = False):
        self._verbose = verbose
        if not template_name:
            # Enforce the default here, so the constructor can be called with '' and will not break.
            template_name = "alpaca"
        file_name = template_name
        if not osp.exists(file_name):
            raise ValueError(f"Can't read {file_name}")
        with open(file_name) as fp:
            self.template = json.load(fp)
        if self._verbose:
            print(
                f"Using prompt template {template_name}: {self.template['description']}"
            )

    def generate_prompt(
            self,
            instruction: str,
            input: Union[None, str] = None,
            label: Union[None, str] = None,
    ) -> str:
        # returns the full prompt from instruction and optional input
        # if a label (=response, =output) is provided, it's also appended.
        if input:
            res = self.template["prompt_input"].format(
                instruction=instruction, input=input
            )
        else:
            res = self.template["prompt_no_input"].format(
                instruction=instruction
            )
        if label:
            res = f"{res}{label}"
        if self._verbose:
            print(res)
        return res

    def get_response(self, output: str) -> str:
        return output.split(self.template["response_split"])[1].strip()

def train(
        train_data,
        test_data,
        tokenizer,
        model_name,
        logger,
        # model/data params
        base_model: str = "",  # the only required argument

        output_dir: str = "./lora-alpaca",
        # training hyperparams
        batch_size: int = 8,
        micro_batch_size: int = 4,
        num_epochs: int = 30,
        learning_rate: float = 3e-4,
        cutoff_len: int = 256,
        val_set_size: int = 0,
        # lora hyperparams
        lora_r: int = 8,
        lora_alpha: int = 16,
        lora_dropout: float = 0.05,
        lora_target_modules: List[str] = [
            "q_proj",
            "v_proj",
        ],
        # llm hyperparams
        train_on_inputs: bool = True,  # if False, masks out inputs in loss
        add_eos_token: bool = False,
        group_by_length: bool = False,  # faster, but produces an odd training loss curve
        # wandb params
        resume_from_checkpoint: str = None,  # either training checkpoint or final adapter
        prompt_template_name: str = "alpaca",  # The prompt template to use, will default to alpaca.
):
    if int(os.environ.get("LOCAL_RANK", 0)) == 0:
        print(
            f"Training Alpaca-LoRA model with params:\n"
            f"base_model: {base_model}\n"
            f"output_dir: {output_dir}\n"
            f"batch_size: {batch_size}\n"
            f"micro_batch_size: {micro_batch_size}\n"
            f"num_epochs: {num_epochs}\n"
            f"learning_rate: {learning_rate}\n"
            f"cutoff_len: {cutoff_len}\n"
            f"val_set_size: {val_set_size}\n"
            f"lora_r: {lora_r}\n"
            f"lora_alpha: {lora_alpha}\n"
            f"lora_dropout: {lora_dropout}\n"
            f"lora_target_modules: {lora_target_modules}\n"
            f"train_on_inputs: {train_on_inputs}\n"
            f"add_eos_token: {add_eos_token}\n"
            f"group_by_length: {group_by_length}\n"

            f"resume_from_checkpoint: {resume_from_checkpoint or False}\n"
            f"prompt template: {prompt_template_name}\n"
        )
    gradient_accumulation_steps = batch_size // micro_batch_size

    device_map = "auto"
    world_size = 1
    ddp = world_size != 1
    if ddp:
        device_map = 0
        gradient_accumulation_steps = gradient_accumulation_steps // world_size


    tokenizer.pad_token_id = (0)  # unk. we want this to be different from the eos token
    tokenizer.padding_side = "left"  # Allow batched inference
    model = LlamaForCausalLM.from_pretrained(model_name,  device_map = device_map, torch_dtype=torch.float16, )
    config = LoraConfig(r=lora_r, lora_alpha=lora_alpha, target_modules=lora_target_modules, lora_dropout=lora_dropout, bias="none", task_type="CAUSAL_LM",)


    model = get_peft_model(model, config)
    model.print_trainable_parameters()  # Be more transparent about the % of trainable params.

    if not ddp and torch.cuda.device_count() > 1:
        # keeps Trainer from trying its own DataParallelism when more than 1 gpu is available
        model.is_parallelizable = True
        model.model_parallel = True

    trainer = transformers.Trainer(
        model=model,
        train_dataset=train_data,
        eval_dataset=test_data,
        args=transformers.TrainingArguments(
            per_device_train_batch_size=micro_batch_size,
            gradient_accumulation_steps=gradient_accumulation_steps,
            warmup_steps=100,
            num_train_epochs=num_epochs,
            learning_rate=learning_rate,
            fp16=True,
            logging_steps=10,
            optim="adamw_torch",
            evaluation_strategy="steps" if val_set_size > 0 else "no",
            save_strategy="steps",
            eval_steps=200 if val_set_size > 0 else None,
            save_steps=200,
            output_dir=output_dir,
            save_total_limit=3,
            load_best_model_at_end=True if val_set_size > 0 else False,
            ddp_find_unused_parameters=False if ddp else None,
            group_by_length=group_by_length,
            report_to="wandb",
            run_name="alpaca-ta",
            do_eval=True,
        ),
        data_collator=transformers.DataCollatorForSeq2Seq(
            tokenizer, pad_to_multiple_of=8, return_tensors="pt", padding=True
        ),
    )
    model.config.use_cache = False

    old_state_dict = model.state_dict
    model.state_dict = (
        lambda self, *_, **__: get_peft_model_state_dict(
            self, old_state_dict()
        )
    ).__get__(model, type(model))

    if torch.__version__ >= "2" and sys.platform != "win32":
        model = torch.compile(model)

    trainer.train(resume_from_checkpoint=resume_from_checkpoint)
    model.save_pretrained(output_dir)


    return model


def evaluate(model, test_data, tokenizer, logger):
    experiment = "validation"
    test_dataloader = DataLoader(test_data, batch_size=1)
    all_test_preds = []
    all_test_labels = []
    generation_config = GenerationConfig()
    for step, (test_input) in enumerate(test_dataloader):
        #log_message(logger, test_input["instruction"], level=logging.INFO)
        prompt = generate_prompt(test_input["instruction"][0], test_input["input"][0])

        inputs = tokenizer(prompt, return_tensors="pt")

        input_ids = inputs["input_ids"].cuda()
        generation_output = model.generate(
            input_ids=input_ids,
            generation_config=generation_config,
            return_dict_in_generate=True,
            output_scores=True,
            max_new_tokens=2
        )

        for s in generation_output.sequences:
            output = tokenizer.decode(s)
            log_message(logger, f"Output {output}", level=logging.INFO)
            all_test_preds.append(output.split("### Response:")[1].strip())
        all_test_labels.append(test_input["output"])
    all_test_preds = list(map( lambda x: 1 if "PRO" in x else 0, all_test_preds))
    all_test_labels = list(map( lambda x:1 if "PRO" in x else 0, all_test_labels))
    test_accuracy = accuracy_score(all_test_labels, all_test_preds)
    f1s = f1_score(all_test_labels, all_test_preds,average=None, labels=[0, 1])
    macro_f1 = f1_score(all_test_labels, all_test_preds, average="macro")
    return {f"{experiment}/accuracy": test_accuracy, f"{experiment}/macro-f1":macro_f1, f"{experiment}/con-f1":f1s[0], f"{experiment}/pro-f1":f1s[1]}

def run_instructiona_fine_tuning_strategy(config, params, experiment, validate, logger, sampling_strategy, similarity):
    all_test_preds = []
    all_test_labels = []
    cutoff_len = 256
    few_shot_size = config["few-shot-size"]
    path_template = get_template_path()
    model_name = config["model-name"]
    tokenizer_name = config["tokenizer-name"]
    prompter = Prompter(path_template)
    tokenizer = LlamaTokenizer.from_pretrained(tokenizer_name)
    dataset = load_splits(experiment, oversample=False)
    if validate:
        experiment_type = "validation"
    else:
        experiment_type = "test"
    test_dataloader = DataLoader(dataset[experiment_type], batch_size=1)
    generation_config = GenerationConfig()
    if sampling_strategy:
        similarities = load_similarities(experiment, experiment_type, similarity)
    new_dataset = {}
    train_data, val_data, test_data = prepare_dataset(dataset, prompter, tokenizer, cutoff_len)
    if validate:
        test_data = val_data
    test_index = 0

    for _, record in dataset[experiment_type].iterrows():
        log_message(logger, f"sampling few shots for {record['text']}", level=logging.INFO)
        if sampling_strategy == "similar":

            few_shots, scores = sample_similar(record["id"], similarities, dataset["training"], few_shot_size)
            log_message(logger, f"most similar is {few_shots.iloc[0]['text']}", level=logging.INFO)
        else:
            few_shots, scores = sample_diverse(record["id"], similarities, dataset["training"], few_shot_size)
        new_dataset["training"] = few_shots
        new_dataset["test"] = pd.DataFrame({})
        new_dataset["validation"] = pd.DataFrame({})
        train_data, _, _ = prepare_dataset(new_dataset, prompter, tokenizer, cutoff_len)

        model = train(train_data, test_data, tokenizer, model_name, logger, batch_size=params["batch-size"], num_epochs=params["epochs"], output_dir=config["model-path-fine-tuned"])
        test_input = test_data[test_index]
        prompt = generate_prompt(test_input["instruction"], test_input["input"])
        inputs = tokenizer(prompt, return_tensors="pt")
        input_ids = inputs["input_ids"].cuda()

        generation_output = model.generate(
            input_ids=input_ids,
            generation_config=generation_config,
            return_dict_in_generate=True,
            output_scores=True,
            max_new_tokens=2
        )

        for s in generation_output.sequences:
            output = tokenizer.decode(s)
            log_message(logger, f"Output {output}", level=logging.INFO)
            all_test_preds.append(output.split("### Response:")[1].strip())
        all_test_labels.append(test_input["output"])
        test_index = test_index + 1
    all_test_preds = list(map( lambda x: 1 if "PRO" in x else 0, all_test_preds))
    all_test_labels = list(map( lambda x:1 if "PRO" in x else 0, all_test_labels))
    test_accuracy = accuracy_score(all_test_labels, all_test_preds)
    f1s = f1_score(all_test_labels, all_test_preds,average=None, labels=[0, 1])
    macro_f1 = f1_score(all_test_labels, all_test_preds, average="macro")
    metrics = {f"{experiment}/accuracy": test_accuracy, f"{experiment}/macro-f1":macro_f1, f"{experiment}/con-f1":f1s[0], f"{experiment}/pro-f1":f1s[1]}
    log_metrics(logger, metrics, level=logging.WARNING)


def run_instructional_fine_tuning(config, params, experiment, validate, logger):
    cutoff_len= 256
    path_template = get_template_path()
    model_name = config["model-name"]
    tokenizer_name = config["tokenizer-name"]
    prompter = Prompter(path_template)
    tokenizer = LlamaTokenizer.from_pretrained(tokenizer_name)
    dataset = load_splits(experiment, oversample=False)
    train_data, val_data, test_data = prepare_dataset(dataset, prompter, tokenizer, cutoff_len, few_shot_size=16)
    if validate:
        test_data = val_data

    model = train(train_data, test_data, tokenizer, model_name, logger, batch_size=params["batch-size"], num_epochs=params["epochs"], output_dir=config["model-path-fine-tuned"])
    model = None
    metrics = evaluate(model    , test_data, tokenizer, logger)
    log_metrics(logger, metrics, level=logging.WARNING)

