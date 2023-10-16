from torch.utils.data import Dataset,DataLoader
from transformers import AutoTokenizer,AutoConfig, AutoModel,DataCollatorForSeq2Seq,PreTrainedTokenizer
from torch.utils.data import Dataset,DataLoader
from typing import List, Optional, Tuple, Union,Iterable,Dict,Any, Callable


class Chatglm2_Dataset(Dataset):
    """
    import pandas as pd
    data =[{'prompt':"content",'response':"good"}]
    df_data = pd.DataFrame(data)
    """
    def __init__(self,df,
                 prompt_col = 'prompt',
                 response_col = 'response',
                 history_col = 'history',
                 max_context_length = 1024,
                 max_target_length = 1024,
                 trust_remote_code = True,
                 model_name_or_path= 'THUDM/chatglm2-6b'
                ):
        super(Chatglm2_Dataset).__init__()
        self.__dict__.update(locals())
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name_or_path, trust_remote_code=self.trust_remote_code) # cache_dir='./' Cache to the current working directory.
        
    def __len__(self):
        return len(self.df)
    
    def get(self,index):
        data = dict(self.df.iloc[index])
        example = {}
        example['context'] = self.tokenizer.build_prompt(query = data[self.prompt_col],history = data.get(self.history_col,None))
        example['target'] = data[self.response_col]
        return example 
    
    def __getitem__(self,index):
        example = self.get(index)
        a_ids = self.tokenizer.encode(text=example['context'], 
                add_special_tokens=True, truncation=True,
                max_length=self.max_context_length)
        b_ids = self.tokenizer.encode(text=example['target'], add_special_tokens=False, truncation=True,max_length=self.max_target_length)
        input_ids = a_ids + b_ids + [self.tokenizer.eos_token_id]
        labels = [-100]*len(a_ids)+b_ids+[self.tokenizer.eos_token_id]
        return {'input_ids':input_ids,'labels':labels}
    
def Llm_DataLoader(dataset,batch_size = 1,num_workers = 2, shuffle = True,model_name_or_path = 'THUDM/chatglm2-6b',trust_remote_code =True):
    """
     function is suitable for llm like ChatGPT and Baichuan.
    """
    tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, trust_remote_code= trust_remote_code) # cache_dir='./' Cache to the current working directory.
    data_collator = DataCollatorForSeq2Seq(tokenizer,model=None,label_pad_token_id=-100,pad_to_multiple_of=None,padding=True)
    dl_train = DataLoader(dataset,batch_size = batch_size,num_workers = num_workers, shuffle = shuffle, collate_fn = data_collator)
    return dl_train

def build_chat_input(messages: List[dict], 
                      max_new_tokens = 2048,
                      model_max_length = 4096,
                      user_token_id = 195,
                      assistant_token_id = 196,
                      eos_token_id = 2,
                     trust_remote_code=True,
                     model_name_or_path= 'baichuan-inc/Baichuan2-13B-Chat'
                     ):
        tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, use_fast=False, trust_remote_code=True)
        max_new_tokens = max_new_tokens
        max_input_tokens = model_max_length - max_new_tokens
        max_input_tokens = max(model_max_length // 2, max_input_tokens)
        total_input, round_input = [], []
        total_label, round_label =[],[]
        for i, message in enumerate(messages[::-1]):
            content_tokens = tokenizer.encode(message["content"])
            if message["role"] == "user":
                round_input = [user_token_id]+ content_tokens+ round_input
                round_label = [-100]+[-100 for _ in content_tokens]+ round_label
                if (total_input and len(total_input) + len(round_input) > max_input_tokens):
                    break
                else:
                    total_input = round_input + total_input
                    total_label = round_label + total_label
                    if len(total_input) >= max_input_tokens:
                        break
                    else:
                        round_input = []
                        round_label = []
            elif message["role"] == "assistant":
                round_input = [assistant_token_id]+ content_tokens+ [eos_token_id]+ round_input
                round_label = [-100]+ content_tokens+ [eos_token_id]+ round_label

            else:
                raise ValueError(f"message role not supported yet: {message['role']}")
        total_input = total_input[-max_input_tokens:]  # truncate left
        total_label = total_label[-max_input_tokens:]
        total_input.append(assistant_token_id)
        total_label.append(-100)
        return total_input,total_label
    
class Baichuan_Dataset(Dataset):
    """
    import pandas as pd
    data =[{'content':"good day",'response':"good"}]
    df_data = pd.DataFrame(data)
    """
    def __init__(self,df,
                ):
        self.df = df 
        
    def __len__(self):
        return len(self.df)
        
    def get_samples(self,index):
        samples = []
        d = dict(self.df.iloc[index])
        samples.append(d)
        return samples
    
    def get_messages(self,index):
        samples = self.get_samples(index)
        messages = []
        for i,d in enumerate(samples):
            if i==0:
                messages.append({'role':'user','content':d['content']}) ##  The prompt format is preprocessed before input.
            else:
                messages.append({'role':'user','content':d['content']})
            
            messages.append({'role':'assistant','content':d['response']})
        return messages
        
    def __getitem__(self,index):
        messages = self.get_messages(index)
        input_ids, labels = build_chat_input(messages)
        return {'input_ids':input_ids,'labels':labels}
    
def make_context(query,target,tokenizer: PreTrainedTokenizer,
    history: List[Tuple[str, str]] = None,
    system: str = "你好，我是一名智能助手，有什么能帮您！",
    max_window_size: int = 6144,
    chat_format: str = "chatml",
    ):
    if history is None:
        history = []
    
    if chat_format == "chatml":
        im_start, im_end = "<|im_start|>", "<|im_end|>"
        im_start_tokens = [tokenizer.im_start_id]
        im_end_tokens = [tokenizer.im_end_id]
        nl_tokens = tokenizer.encode("\n")

        def _tokenize_str(role, content):
            return f"{role}\n{content}", tokenizer.encode(
                role, allowed_special=set()
            ) + nl_tokens + tokenizer.encode(content, allowed_special=set())

        system_text, system_tokens_part = _tokenize_str("system", system)
        system_tokens = im_start_tokens + system_tokens_part + im_end_tokens

        raw_text = ""
        context_tokens = []

        for turn_query, turn_response in reversed(history):
            query_text, query_tokens_part = _tokenize_str("user", turn_query)
            query_tokens = im_start_tokens + query_tokens_part + im_end_tokens
            response_text, response_tokens_part = _tokenize_str(
                "assistant", turn_response
            )
            response_tokens = im_start_tokens + response_tokens_part + im_end_tokens

            next_context_tokens = nl_tokens + query_tokens + nl_tokens + response_tokens
            prev_chat = (
                f"\n{im_start}{query_text}{im_end}\n{im_start}{response_text}{im_end}"
            )

            current_context_size = (
                len(system_tokens) + len(next_context_tokens) + len(context_tokens)
            )
            if current_context_size < max_window_size:
                context_tokens = next_context_tokens + context_tokens
                raw_text = prev_chat + raw_text
            else:
                break

        context_tokens = system_tokens + context_tokens
        raw_text = f"{im_start}{system_text}{im_end}" + raw_text
        context_tokens += (
            nl_tokens
            + im_start_tokens
            + _tokenize_str("user", query)[1]
            + im_end_tokens
            + nl_tokens
            + im_start_tokens
            + tokenizer.encode("assistant")
            + nl_tokens
        )
        raw_text += f"\n{im_start}user\n{query}{im_end}\n{im_start}assistant\n"

    elif chat_format == "raw":
        raw_text = query
        context_tokens = tokenizer.encode(raw_text)
    else:
        raise NotImplementedError(f"Unknown chat format {chat_format!r}")
        
    target_ids = tokenizer.encode(text=target) 
    input_ids = context_tokens + target_ids + tokenizer.encode('<|im_end|><|endoftext|>')
    labels = [-100]*len(context_tokens)+target_ids+tokenizer.encode('<|im_end|><|endoftext|>')
    
    if max_window_size is not None:
        input_ids = input_ids[-max_window_size:]
        if labels is not None:
            labels = labels[-max_window_size:]

    return {'input_ids': input_ids, 'labels': labels}

class Qwen_Dataset(Dataset):
    """
    import pandas as pd
    data =[{'prompt':"content",'response':"good"}]
    df_data = pd.DataFrame(data)
    """
    def __init__(self,df,
                 prompt_col = 'prompt',
                 response_col = 'response',
                 history_col = 'history',
                 max_window_size = 1024,
                 trust_remote_code = True,
                 model_name_or_path= 'Qwen/Qwen-7B-Chat'
                ):
        super(Qwen_Dataset).__init__()
        self.__dict__.update(locals())
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name_or_path, trust_remote_code=self.trust_remote_code) # cache_dir='./' Cache to the current working directory.
        
    def __len__(self):
        return len(self.df)
    
    def get(self,index):
        ## convert dict
        data = dict(self.df.iloc[index])
        example = {}
        example['context'] = data[self.prompt_col]
        example['target'] = data[self.response_col]
        return example 
    
    def __getitem__(self,index):
        example = self.get(index)
        query = example['context']
        target = example['target']
        result = make_context(query,target,tokenizer= self.tokenizer,max_window_size= self.max_window_size)
        return result
    
Context = Union[str, List[int]]

TEMPLATE_MAPPING = {
    'default': {
        'prefix': ['{{system}}\n\n'],
        'prompt': ['### Human:\n', '{{query}}\n\n', '### Assistant:\n'],
        'chat_sep': ['\n\n'],
        'suffix': [['eos_token_id']],
    },
    'default-generation': {
        'prefix': [],
        'prompt': ['{{query}}'],
        'suffix': [['eos_token_id']],
    },
    'chatml': {
        'prefix': ['<|im_start|>system\n{{system}}<|im_end|>\n'],
        'prompt':
        ['<|im_start|>user\n{{query}}<|im_end|>\n<|im_start|>assistant\n'],
        'chat_sep': ['<|im_end|>\n'],
        'suffix': ['<|im_end|><|endoftext|>'],
    },
    'baichuan': {
        'prefix': [],
        'prompt': [[195], '{{query}}', [196]],
        'chat_sep': [],
        'suffix': [['eos_token_id']],
    },
    'chatglm2': {
        'prefix': [[64790, 64792]],
        'prompt': ['[Round {{round}}]\n\n问：{{query}}\n\n答：'],
        'chat_sep': ['\n\n'],
        'suffix': [['eos_token_id']],
    },
    'llama': {
        'prefix': [['bos_token_id'],
                   '[INST] <<SYS>>\n{{system}}\n<</SYS>>\n\n'],
        'prompt': ['{{query}} [/INST] '],
        'chat_sep': [' ', ['eos_token_id', 'bos_token_id'], '[INST] '],
        'suffix': [['eos_token_id']],
    },
    'openbuddy-llama': {
        'prefix': ['{{system}}\n\n'],
        'prompt': ['User: {{query}}\nAssistant: '],
        'chat_sep': ['\n'],
        'suffix': [['eos_token_id']],
    },
    'internlm': {
        'prefix': ['<s>'],
        'prompt': ['<|User|>:{{query}}<eoh>\n<|Bot|>:'],
        'chat_sep': ['<eoa>\n'],
        'suffix': ['<eoa></s>'],
    }
}

class data_preprocess:
    def __init__(self,template_type, tokenizer, query, response, history=None, max_length=2048):
        self.template_type = template_type
        self.tokenizer = tokenizer
        self.query = query
        self.response = response
        self.history =history
        self.max_length = max_length
        self.DEFAULT_SYSTEM = 'you are a helpful assistant!'
        self.History = List[Tuple[str, str]]
        self.TEMPLATE_MAPPING = TEMPLATE_MAPPING
    
    def concat_context_list(self,
        context_list: List[Context],
        new_context_list: List[Context],
        placeholder_list: List[str],
        system: Optional[str] = None,
        query: Optional[str] = None,
        round: Optional[str] = None,
        ) -> None:
        for context in context_list:
            if isinstance(context, str):
                for (old_str,
                     new_str) in zip(['{{system}}', '{{query}}', '{{round}}'],
                                     [system, query, round]):
                    if new_str is not None and old_str in context:
                        placeholder_list.append(new_str)
            new_context_list.append(context)
    def simplify_context_list(self,context_list: List[Context]) -> List[Context]:
        ## str to list
        res: List[Context] = []
        temp: List[str] = []
        for c in context_list:
            if isinstance(c, str):
                temp.append(c)
            else:
                if len(temp) > 0:
                    res.append(''.join(temp))
                    temp.clear()
                res.append(c)
        if len(temp) > 0:
            res.append(''.join(temp))
        return res
    
    def _encode(self,tokenizer: PreTrainedTokenizer, context_list: List[Context],
            placeholder_list: List[str]) -> List[int]:
        input_ids: List[int] = []
        placeholder_it = iter(placeholder_list)
        for context in context_list:
            if isinstance(context, list):
                for c in context:
                    if isinstance(c, str):
                        token = getattr(tokenizer, c)
                        assert token is not None
                    else:
                        token = c
                    input_ids.append(token)
            elif isinstance(context, str):
                for old_str in ['{{system}}', '{{query}}', '{{round}}']:
                    if old_str in context:
                        new_str = next(placeholder_it)
                        context = context.replace(old_str, new_str)
                input_ids += tokenizer(
                    context, return_attention_mask=False,
                    add_special_tokens=False)['input_ids']
        return input_ids
    
    def _preprocess(self) -> Dict[str, List[int]]:
        template_type=self.template_type
        tokenizer=self.tokenizer
        query = self.query
        response = self.response
        history =self.history
        system =self.DEFAULT_SYSTEM
        max_length = self.max_length
    
        if history is None:
            history = []

        template_config = self.TEMPLATE_MAPPING[template_type]
        if system is None:
            system = self.DEFAULT_SYSTEM

        total_context_list: List[Context] = []
        placeholder_list: List[str] = []
        self.concat_context_list(
            template_config['prefix'],
            total_context_list,
            placeholder_list,
            system=system)
    
        for i, (q, r) in enumerate(history):
            assert 'chat_sep' in template_config, 'not support multi-round chat'
            self.concat_context_list(
                [*template_config['prompt'], r, *template_config['chat_sep']],
                total_context_list,
                placeholder_list,
                query=q,
                round=str(i + 1))
        self.concat_context_list(
            template_config['prompt'],
            total_context_list,
            placeholder_list,
            query=query,
            round=str(len(history) + 1))

        total_context_list = self.simplify_context_list(total_context_list)
        input_ids = self._encode(tokenizer, total_context_list, placeholder_list)

        labels = None
        if response is not None:
            labels = [-100] * len(input_ids)
            tgt_input_ids = self._encode(tokenizer, [response], [])
            tgt_input_ids += self._encode(tokenizer, template_config['suffix'], [])
            input_ids += tgt_input_ids
            labels += tgt_input_ids

        if max_length is not None:
            input_ids = input_ids[-max_length:]
            if labels is not None:
                labels = labels[-max_length:]

        return {'input_ids': input_ids, 'labels': labels}

import torch
class Llm_Dataset(Dataset):
    """
    import pandas as pd
    data =[{'query':"content",'response':"good"}]
    df_data = pd.DataFrame(data)
    """
    def __init__(self, df,
                 tokenizer,
                 template_type = 'chatglm2',
                 max_length = 2048,
                 history=None
                ):
        self.tokenizer = tokenizer
        self.df = df
        self.template_type = template_type
        self.max_length = max_length
        self.history = history

    def __len__(self):
        # 返回数据集的大小
        return len(self.df)

    def __getitem__(self, index):
        # 根据 idx 返回一个数据样本和其标签
        query = dict(self.df.iloc[index])['query']
        response = dict(self.df.iloc[index])['response']
        data_class  = data_preprocess(self.template_type, self.tokenizer, query, response,self.history,self.max_length)
        return data_class._preprocess()
    
class Chatglm2_Dataset_Trainer(Dataset):
    """
    ## apply to Trainer  model
    import pandas as pd
    data =[{'prompt':"content",'response':"good"}]
    df = pd.DataFrame(data)
    """
    def __init__(self,df,
                 prompt_col = 'prompt',
                 response_col = 'response',
                 history_col = 'history',
                 max_context_length = 100,  ## 如果太多，可能无法加载
                 max_target_length = 100,   ## 如果太多，可能无法加载
                 trust_remote_code = True,
                 model_name_or_path= 'THUDM/chatglm2-6b'
                ):
        super(Chatglm2_Dataset_Trainer).__init__()
        self.__dict__.update(locals())
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name_or_path, trust_remote_code=self.trust_remote_code) # cache_dir='./' Cache to the current working directory.
        self.ignore_index = -100
        
    def __len__(self):
        return len(self.df)
    
    def get(self,index):
        data = dict(self.df.iloc[index])
        example = {}
        example['context'] = self.tokenizer.build_prompt(query = data[self.prompt_col],history = data.get(self.history_col,None))
        example['target'] = data[self.response_col]
        return example 
    
    def __getitem__(self,index):
        example = self.get(index)
        a_ids = self.tokenizer.encode(text=example['context'], 
                add_special_tokens=True, truncation=True,
                max_length=self.max_context_length)
        b_ids = self.tokenizer.encode(text=example['target'], add_special_tokens=False, truncation=True,max_length=self.max_target_length)
        input_ids = a_ids + b_ids + [self.tokenizer.eos_token_id]
        labels = [-100]*len(a_ids)+b_ids+[self.tokenizer.eos_token_id]
        ## add part
        input_ids += [self.tokenizer.pad_token_id] * (self.max_context_length - len(input_ids))
        labels += [self.ignore_index] * (self.max_target_length - len(labels))
        input_ids = torch.LongTensor(input_ids)
        labels = torch.LongTensor(labels)
        attention_mask = (input_ids != self.tokenizer.pad_token_id).to(torch.int)
        return {
            "input_ids": input_ids,
            "labels": labels,
            "attention_mask": attention_mask,
        }
    
    
    
