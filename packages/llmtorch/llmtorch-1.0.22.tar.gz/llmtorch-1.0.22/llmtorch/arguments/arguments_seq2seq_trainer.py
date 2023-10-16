# -*- coding: utf-8 -*-
"""
Created on Thu Sep 14 11:35:02 2023

@author: a
"""

import os
import math
import pathlib
from typing import Any, Dict, List, Optional, Tuple, Union
from dataclasses import dataclass, field
import json
import sys

import torch
from torch.utils.data import Dataset
import transformers
#from transformers.training_args import TrainingArguments
from transformers.training_args_seq2seq import Seq2SeqTrainingArguments 

@dataclass
class ModelArguments:
    model_name_or_path: Optional[str] = field(default="THUDM/chatglm2-6b")


@dataclass
class DataArguments:
    data_path: str = field(default=None, metadata={"help": "Path to the training data."})


@dataclass
class Seq2SeqTrainingArguments(transformers.Seq2SeqTrainingArguments):
    cache_dir: Optional[str] = field(default=None)
    optim: str = field(default="adamw_torch")
    model_max_length: int = field(
        default=512,
        metadata={
            "help": "Maximum sequence length. Sequences will be right padded (and possibly truncated)."
        },
    )
    use_lora: bool = field(default=False)
    
    
#  parser = transformers.HfArgumentParser(
#         (ModelArguments, DataArguments, TrainingArguments)
#     )

def _parse_args(parser: transformers.HfArgumentParser, args: Optional[Dict[str, Any]] = None) -> Tuple[Any]:
    if args is not None:
        return parser.parse_dict(args)
    elif len(sys.argv) == 2 and sys.argv[1].endswith(".yaml"):
        return parser.parse_yaml_file(os.path.abspath(sys.argv[1]))
    elif len(sys.argv) == 2 and sys.argv[1].endswith(".json"):
        return parser.parse_json_file(os.path.abspath(sys.argv[1]))
    else:
        return parser.parse_args_into_dataclasses()
    


def parse_train_args(
    args: Optional[Dict[str, Any]] = None) -> Tuple[
    ModelArguments,
    DataArguments,
    Seq2SeqTrainingArguments]:
    parser = transformers.HfArgumentParser((
        ModelArguments,
        DataArguments,
        Seq2SeqTrainingArguments
    ))
    return _parse_args(parser, args)

def get_train_args_seq(
    args: Optional[Dict[str, Any]] = None) -> Tuple[
    ModelArguments,
    DataArguments,
    Seq2SeqTrainingArguments]:
    model_args, data_args, training_args = parse_train_args(args)
    return model_args, data_args, training_args