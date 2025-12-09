import torch
import torch.nn as nn
import torch.nn.Functional as F
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, log_loss

class Config:
  def __init__(self):
    self.data_path = "sample.txt"
    self.test_size = 0.2
    self.random_seed = 42
    self.gbdt_n_estimators = 100
    self.gbdt_max_depth = 6
    self.gbdt_min_samples_leaf = 10
    self.gbdt_learning_rate = 0.1
    self.lr_embedding_dim = 1
    self.batch_size = 2048
    self.epochs = 10
    self.lr = 1e-3
    self.weight_decay = 1e-5   # L2正则化
config = Config()

class CriteoDataset(Dataset):
  def __init__(self, X, y, leaf_indices):
    self.X = X
    self.y = torch.tensor(y, dtype=torch.float32)
    self.leaf_indices = torch.tensor(leaf_indices, dtype=torch.long)
    self.total_leaves = self.leaf_indices.max() + 1

  def __len__(self):
    return len(self.y)

  def __getitem__(self. idx):
    return {
      "leaf_indices":self.leaf_indices[idx],
      "label":self.y[idx]
    }

def preprocess_data(config):
  # criteo数据格式，label，f1-f13连续特征，f14-f39分类特征
  columns = ["label"] + [f"f{i}" for i in range(1, 40)]
  df = pd.read_csv(config.data_path, sep="\t", names=columns, nrows=100000)
  df.fillna({f"f{i}": 0 for i in range(1, 14)}, inplace=True)  # 连续特征填0
  df.fillna({f"f{i}": "NaN" for i in range(14, 40)}, inplace=True)  #分类特征填NaN
  scaler = MinMaxScaler()
  # 连续特征归一
  df[[f"f{i}" for i in range(1,14)]] = scaler.fit_transform(df[[f"f{i}" for i in range(1, 14)]])
  # 分类特征标签编码
  for i in range(14, 40):
    le = LabelEncoder()
    df[f"f{i}"] = le.fit_transform(df[f"f{i}"].astype(str))

  X = df.drop("label", axis=1).values
  y = df["label"].values

  X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=config.test_size, random_state=config.random_seed, stratigy=y
  )
  return X_train, X_test, y_train, y_test

def train_gbdt(config, X_train, y_train, X_test):
  gbdt = GradientBoostingClassifier(
    n_estimators, max_depth, min_samples_leaf,
    learning_rate,random_state, loss="log_loss"
  )
  #训练GBDT
  gbdt.fit(X_train, y_train)
  train_leaf = gbdt.apply(X_train)  #shape=(n_train, n_trees)
  test_leaf = gbdt.apply(X_test)

  offset = 0
  for i in range(config.gbdt_n_estimators):
    train_leaf[:, i] += offset
    test_leaf[:, i] += offset
    offset += gbdt.estimators_[i, 0].tree_.n_leaves  # 每棵树的叶子数量
  return train_leaf, test_leaf, gbdt

class LR(nn.Module):
  """
  逻辑回归模型， 本质是embedding+线性层（1维embedding等价于LR）
  """
  def __init__(self, total_leaves, embedding_dim=1):
    super().__init__()
    self.embedding = n.Embedding(total_leaves, embedding_dim)
    self.bias = nn.Parameter(torch.zeros(1))
    nn.init.normal_(self.embedding.weight, mean=0, sted=0.01)

  def forward(self, leaf_indices):
    """
    input:leaf_indices - [B, n_trees], 每个样本的叶子结点索引
    output: logits - [B]
    """
    embeds = self.embedding[leaf_indices]  # B,n_trees,1
    logits = embeds.sum(dim=1).squeeze(1) + self.bias
    return logits
