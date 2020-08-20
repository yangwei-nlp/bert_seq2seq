import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import torch
from models.seq2seq_model import Seq2SeqModel

def load_bert(vocab_path, model_name="roberta", model_class="seq2seq", target_size=0):
    """
    model_path: 模型位置
    这是个统一的接口，用来加载模型的
    model_class : seq2seq or encoder
    """
    if model_class == "seq2seq":
        bert_model = Seq2SeqModel(vocab_path, model_name=model_name)
        return bert_model

def load_model_params(model, pretrain_model_path):
    checkpoint = torch.load(pretrain_model_path)
    # 模型刚开始训练的时候, 需要载入预训练的BERT
    checkpoint = {k[5:]: v for k, v in checkpoint.items()
                                        if k[:4] == "bert" and "pooler" not in k}
    # k[:4] == "bert" and "pooler" not in k：意思是将原生BERT层参数提取出来，基于下游任务cls的参数不要了
    model.load_state_dict(checkpoint, strict=False)
    torch.cuda.empty_cache()
    print("{} loaded!".format(pretrain_model_path))
    return checkpoint

def load_recent_model(model, recent_model_path):
    checkpoint = torch.load(recent_model_path)
    model.load_state_dict(checkpoint)
    torch.cuda.empty_cache()
    print(str(recent_model_path) + " loaded!")


