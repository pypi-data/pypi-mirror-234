# -*- coding:utf-8 -*-
import sys,datetime
from tqdm import tqdm
from copy import deepcopy
import numpy as np
import pandas as pd
import torch
from accelerate import Accelerator

class EpochRunner:
    def __init__(self,steprunner,quiet=False):
        self.steprunner = steprunner
        self.stage = steprunner.stage
        self.accelerator = steprunner.accelerator
        self.net = steprunner.net
        self.quiet = quiet
        
    def __call__(self,dataloader):
        n = dataloader.size  if hasattr(dataloader,'size') else len(dataloader)
        loop = tqdm(enumerate(dataloader,start=1),   ## 迭代器中的每个元素都包括一个索引（从1开始）
                    total=n,  ##这个参数指定了总共要处理多少个元素。通常，n 是一个表示数据总数的整数。
                    file=sys.stdout,  ## 进度条的输出会被写入到标准输出流（通常是终端窗口），这个参数可以让你指定输出流的文件对象。在这里，它指定了输出到标准输出。
                    disable=not self.accelerator.is_local_main_process or self.quiet,  ## 这个参数用于控制是否禁用进度条 False 为非禁用
                    ncols=100    ##进度条的显示宽度
                   )

        epoch_losses = {}
        
        for step, batch in loop: 
            with self.accelerator.accumulate(self.net):
                step_losses,step_metrics = self.steprunner(batch)   ##  得到损失和学习率
                step_log = dict(step_losses,**step_metrics)

                for k,v in step_losses.items():
                    epoch_losses[k] = epoch_losses.get(k,0.0)+v   ##  获取value  没有写0
                    
                if step<n:
                    loop.set_postfix(**step_log)   ## set_postfix(**step_log): 这是 tqdm 对象的方法，用于设置进度条的附加信息。附加信息通常用于显示一些额外的进度相关的数据，例如当前步骤的详细信息。
                    
                    if hasattr(self,'progress') and self.accelerator.is_local_main_process:
                        post_log = dict(**{'i':step,'n':n},**step_log)
                        self.progress.set_postfix(**post_log)

                elif step==n:
                    epoch_metrics = step_metrics
                    epoch_metrics.update({self.stage+"_"+name:metric_fn.compute().item() 
                                     for name,metric_fn in self.steprunner.metrics_dict.items()})
                    epoch_losses = {k:v/step for k,v in epoch_losses.items()}
                    epoch_log = dict(epoch_losses,**epoch_metrics)
                    loop.set_postfix(**epoch_log)
            
                    
                    if hasattr(self,'progress') and self.accelerator.is_local_main_process:
                        post_log = dict(**{'i':step,'n':n},**epoch_log)
                        self.progress.set_postfix(**post_log)
                    
                    for name,metric_fn in self.steprunner.metrics_dict.items():
                        metric_fn.reset()  
                else:
                    break
        return epoch_log
    

class StepRunner:
    def __init__(self, net, loss_fn=None, accelerator=None, stage = "train", metrics_dict = None, optimizer = None, lr_scheduler = None):
        self.net,self.loss_fn,self.metrics_dict,self.stage = net,loss_fn,metrics_dict,stage
        self.optimizer,self.lr_scheduler = optimizer,lr_scheduler
        self.accelerator = accelerator if accelerator is not None else Accelerator() 
        if self.stage=='train':
            self.net.train() 
        else:
            self.net.eval()
    
    def __call__(self, batch):
        
        #loss
        with self.accelerator.autocast():
            if  self.loss_fn ==None:
                loss = self.net(**batch).loss
            else :
                features,labels = batch
                preds = self.net(features)
                loss = self.loss_fn(preds,labels)
        # with self.accelerator.autocast() and self.loss_fn is not None:
        #     features,labels = batch
        #     preds = self.net(features)
        #     loss = self.loss_fn(preds,labels)
            
        #backward()
        if self.optimizer is not None and self.stage=="train":
            self.accelerator.backward(loss)
            if self.accelerator.sync_gradients:
                self.accelerator.clip_grad_norm_(self.net.parameters(), 1.0)
            self.optimizer.step()
            if self.lr_scheduler is not None:
                self.lr_scheduler.step()
            self.optimizer.zero_grad()
            
        all_loss = self.accelerator.gather(loss).sum()
        
        #losses (or plain metrics that can be averaged)
        step_losses = {self.stage+"_loss":all_loss.item()}
        
        #metrics (stateful metrics)
        step_metrics = {}
        
        if self.stage=="train":
            if self.optimizer is not None:
                step_metrics['lr'] = self.optimizer.state_dict()['param_groups'][0]['lr']
            else:
                step_metrics['lr'] = 0.0
        return step_losses,step_metrics             ## 获取损失和学习率
    
    
class LlmModel(torch.nn.Module):
    
    StepRunner,EpochRunner = StepRunner,EpochRunner
    
    def __init__(self,net,loss_fn,optimizer=None,metrics_dict=None,lr_scheduler = None,**kwargs):
        
        """
        net,
        loss_fn = None,  or  function definition：loss = torch.nn.CrossEntropyLoss()
        optimizer=optimizer
        """
        super().__init__()
        self.net,self.loss_fn,self.metrics_dict = net, loss_fn, torch.nn.ModuleDict(metrics_dict) 
        self.optimizer = optimizer if optimizer is not None else torch.optim.Adam(
            self.net.parameters(), lr=3e-4)
        self.lr_scheduler = lr_scheduler
        self.kwargs = kwargs
        self.from_scratch = True
        
#     def save_ckpt(self, ckpt_path=None, accelerator= None):
#         accelerator = accelerator if accelerator is not None else self.accelerator
#         net_dict = accelerator.get_state_dict(self.net)
#         accelerator.save(net_dict,ckpt_path if ckpt_path is not None else self.ckpt_path)
    ## add ckpt
    def save_ckpt(self, ckpt_path='None', accelerator = None):
        unwrap_net = accelerator.unwrap_model(self.net)
        unwrap_net.save_pretrained(ckpt_path)
      
    def load_ckpt(self, ckpt_path=None):
        self.net.load_state_dict(
            torch.load(ckpt_path if ckpt_path is not None else self.ckpt_path,
            map_location='cpu'))
        self.from_scratch = False

    def forward(self, x):
        return self.net.forward(x)
    
    def fit(self, train_data, val_data=None, epochs=10, ckpt_path='checkpoint',
            patience=5, monitor="val_loss", mode="min", callbacks=None, 
            plot=True,  wandb=False, quiet=None, 
            mixed_precision='no', cpu=False, gradient_accumulation_steps=1):              ## 将 gradient_accumulation_steps 设置为 4，那么模型将在累积了 4 个小批量数据的梯度之后，才会执行一次权重更新
        """
        train_data = dl_train,
        val_data = dl_val,
        epochs=50,
        plot=True,
        ckpt_path = 'chatglm2_qlora'
        """
        from .utils import colorful,is_jupyter
        self.__dict__.update(locals())  ##将当前作用域中的所有局部变量添加到对象的属性字典中
        
        self.accelerator = Accelerator(mixed_precision=mixed_precision,cpu=cpu,
            gradient_accumulation_steps=gradient_accumulation_steps)
        
        device = str(self.accelerator.device)
        device_type = 'cpu'  if 'cpu' in device else ('gpu' if 'cuda' in device else 'other')
        self.accelerator.print(
            colorful("<<<<<< "+device_type +" "+ device +" is used >>>>>>"))
    
        self.net,self.loss_fn,self.metrics_dict,self.optimizer,self.lr_scheduler= self.accelerator.prepare(
            self.net,self.loss_fn,self.metrics_dict,self.optimizer,self.lr_scheduler)

        for key in self.kwargs:
            self.kwargs[key] = self.accelerator.prepare(self.kwargs[key])
        
        train_dataloader,val_dataloader = self.accelerator.prepare(train_data,val_data)
        train_dataloader.size = train_data.size if hasattr(train_data,'size') else len(train_data)
        train_dataloader.size = min(train_dataloader.size,len(train_dataloader))
        
        if val_data:
            val_dataloader.size = val_data.size if hasattr(val_data,'size') else len(val_data)
            val_dataloader.size = min(val_dataloader.size,len(val_dataloader))
        
        self.history = {}
        callbacks = callbacks if callbacks is not None else []
        
        if bool(plot):
            from .kerascallbacks import VisProgress,VisMetric
            callbacks = [VisMetric(),VisProgress()]+callbacks
            
            
        if wandb!=False:
            from .kerascallbacks import WandbCallback
            project = wandb if isinstance(wandb,str) else 'llmtorch'
            callbacks.append(WandbCallback(project=project))
            
            
        self.callbacks = [self.accelerator.prepare(x) for x in callbacks]
        
        if self.accelerator.is_local_main_process:    ###  画训练的可视化图
            [cb.on_fit_start(model = self) for cb in self.callbacks if hasattr(cb,'on_fit_start')]
                
        start_epoch = 1 if self.from_scratch else 0
        
        if bool(plot) or quiet is None:
            quiet = True
        
        quiet_fn = (lambda epoch:quiet) if isinstance(quiet,bool) else (
            (lambda epoch:epoch>quiet) if isinstance(quiet,int) else quiet)
        
        for epoch in range(start_epoch,epochs+1):
            should_quiet = quiet_fn(epoch)  
        
            if not should_quiet:   ## True
                nowtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                self.accelerator.print("\n"+"=========="*8 + "%s"%nowtime)
                self.accelerator.print("Epoch {0} / {1}".format(epoch, epochs)+"\n")

            # 1，train -------------------------------------------------  ## 获取损失和学习率
            train_step_runner = self.StepRunner(
                    net = self.net,
                    loss_fn = self.loss_fn,
                    accelerator = self.accelerator,
                    stage="train",
                    metrics_dict=deepcopy(self.metrics_dict),
                    optimizer = self.optimizer if epoch>0 else None,
                    lr_scheduler = self.lr_scheduler if epoch>0 else None,
                    **self.kwargs
            )

            train_epoch_runner = self.EpochRunner(train_step_runner,should_quiet)
            train_metrics = {'epoch':epoch}
            train_metrics.update(train_epoch_runner(train_dataloader))

            for name, metric in train_metrics.items():
                self.history[name] = self.history.get(name, []) + [metric]

            if self.accelerator.is_local_main_process:   ###  画训练的可视化图
                [cb.on_train_epoch_end(model = self) for cb in self.callbacks 
                 if hasattr(cb,'on_train_epoch_end')]
                
            # 2，validate -------------------------------------------------
            if val_dataloader is not None:
                val_step_runner = self.StepRunner(
                    net = self.net,
                    loss_fn = self.loss_fn,
                    accelerator = self.accelerator,
                    stage="val",
                    metrics_dict= deepcopy(self.metrics_dict),
                    **self.kwargs
                )
                val_epoch_runner = self.EpochRunner(val_step_runner,should_quiet)
                with torch.no_grad():
                    val_metrics = val_epoch_runner(val_dataloader)

                for name, metric in val_metrics.items():
                    self.history[name] = self.history.get(name, []) + [metric]
                
            if self.accelerator.is_local_main_process:   ###  画训练的可视化图
                [cb.on_validation_epoch_end(model = self) for cb in self.callbacks 
                 if hasattr(cb,'on_validation_epoch_end')]

            # 3，early-stopping -------------------------------------------------
            self.accelerator.wait_for_everyone()
            arr_scores = self.history[monitor]
            best_score_idx = np.argmax(arr_scores) if mode=="max" else np.argmin(arr_scores)

            if best_score_idx==len(arr_scores)-1 and self.accelerator.is_local_main_process:
                self.save_ckpt(ckpt_path,accelerator = self.accelerator)
                if not should_quiet:
                    self.accelerator.print(colorful("<<<<<< reach best {0} : {1} >>>>>>".format(
                        monitor,arr_scores[best_score_idx])))

            if len(arr_scores)-best_score_idx>patience:
                break
                
        if self.accelerator.is_local_main_process:   
            dfhistory = pd.DataFrame(self.history)
#             [cb.on_fit_end(model = self) for cb in self.callbacks 
#                  if hasattr(cb,'on_fit_end')]
            if epoch<epochs:
                self.accelerator.print(colorful(
                        "<<<<<< {} without improvement in {} epoch,""early stopping >>>>>> \n"
                    ).format(monitor,patience))
#             self.net = self.accelerator.unwrap_model(self.net)
#             self.net.cpu()
#             self.load_ckpt(ckpt_path)
            return dfhistory