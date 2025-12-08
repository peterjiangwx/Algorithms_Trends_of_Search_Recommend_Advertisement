class CTRDataset(Dataset):
  def __init__(self, data_path, config):
    self.config = config
    self.data = self._load_data(data_path)
    self.categorical_features = list(config.categorical_vocab_sizes.keys())
  def _load_data(self, path):
    data = []
    with open(path, "r", encoding="utf-8") as f:
      next(f)  # 跳过表头
      for line in f:
        parts = line.strip().split("\t")
        label = int(parts[0])
        continuous_features = list(map(float, parts[1:self.config.num_continuous_features+1]))
        categorical_features = parts[self.config.num_continuous_features + 1:]
        data.append({
          "continuous":continuous_features,
          "categorical":categorical_features,
          "label":label
        })
    return data
  def __len__(self):
    return len(self.data)

  def __getitem__(self, idx):
    sample = self.data[idx]
    continuous = torch.tensor(sample["continuous"], dtype=tensor.float32)
    continuous = (continuous - continuous.min()) / (continuous.max() - continuous.min + 1e-8)

    categorical = []
    for i, feat in enumerate(sample["categorical"]):
      feat_name = self.categorical_features[i]
      vocab_size = self.config.categorical_vocab_sizes[feat_name]
      idx = int(feat) if int(feat) < vocab_size else 1  # 1为oov的索引
      categorical.append(idx)
    categorical = torch.tensor(categorical, dtype = torch.long)
    label = torch.tensor(sample["label"], dtype = torch.float32)
    return {
      "continuous":continuous,
      "categorical":categorical,
      "label":label
    }

def create_dataloader(train_path, test_path, config):
  train_dataset = CTRDataset(train_path, config)
  test_dataset = CTRDataset(test_path, config)
  train_loader = DataLoader(
    train_dataset, batch_size=config.batch_size, shuffle=True,
    num_workers=4, pin_memory=True
  )
  test_loader = DataLoader(
    test_dataset, batch_size=config.batch_size, shuffle=False,
    num_workers=4, pin_memory=True
  )
  return train_loader, test_loader

class FM(nn.Module):
  def __init__()
