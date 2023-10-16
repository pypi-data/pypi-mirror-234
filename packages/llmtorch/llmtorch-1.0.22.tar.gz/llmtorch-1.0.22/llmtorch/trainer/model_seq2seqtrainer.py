# -*- coding: utf-8 -*-
"""
Created on Thu Sep 14 11:35:02 2023

@author: a
"""
#refer :https://github.com/baichuan-inc/Baichuan2/blob/main/fine-tune/fine-tune.py

import transformers

def model_seq2seqtrainer(model,training_args,train_dataset,tokenizer):
    trainer = transformers.Seq2SeqTrainer(
    model=model, args=training_args, train_dataset=tr_ds_data, tokenizer=tokenizer)
    trainer.train()
    trainer.save_state()
    trainer.save_model(output_dir=training_args.output_dir)