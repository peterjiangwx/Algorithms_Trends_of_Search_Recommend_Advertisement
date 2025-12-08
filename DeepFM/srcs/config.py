import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
import numpy as np
from collections import defaultdict

# 配置参数
class Config:
  def __init__(self):
    # 通用参数
    self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    self.embedding_dim = 10  # FM 隐向量维度
    self.batch_size = 2048
    self.epochs = 10
    self.lr = 1e-3
    self.dropout = 0.5  # 防止过拟合
    self.weight_decay = 1e-5  # L2正则化

    # Deep组件参数
    self.hidden_dims = [400, 400, 400]  # 隐藏层维度
    self.activation = "relu"

    # 数据相关
    self.num_continuous_features = 13  # Criteo数据集连续特征数
    self.categorical_vocab_sizes = {}
    
