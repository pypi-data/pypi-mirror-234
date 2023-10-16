import torch
import pandas as pd
from torch.utils.data import Dataset, DataLoader


class CharRNNDataset(Dataset):
    """
    CharRNN Dataset for PyTorch
    
    Process a csv file with:
    - a column of string
    - a column of label for the string
    For example:
        __________________________
        text     | label
        --------------------------
        C1D2F3G4 | pop
        D1G2F1C4 | jazz
        ...      | ...
        __________________________

    == Arguments ==
    csv_path: string
        the dataset

    chars: string or list[char]
        list of unique characters in the dataset. If None, would be derived from dataset (may be computatioally expensive)

    classes: list
        list of prediction classes. If None, would be derived from dataset

    text_col: str
        column header in the csv_path for the text column

    label_col: str
        column header in the csv_path for the label column        

    pad: char
        a character to be used as the padding token

    max_len: str
        exclude data with more than max_len characters. If None, all data is used
    """    
    def __init__(self, csv_path, chars=None, classes=None, ascending=False, text_col='text', label_col="label", pad="-", max_len=None):
        df = pd.read_csv(csv_path)
        assert text_col in df.columns
        assert label_col in df.columns
        df = df.reindex(df[text_col].str.len().sort_values(ascending=ascending).index)        

        self.pad = pad
        
        if classes is None:
            classes = sorted(df[label_col].unique().tolist())
        self.classes = classes
        self.n_classes = len(classes)        
        self.class2idx = dict(zip(classes, range(len(classes))))
        
        if chars is None:
            chars = sorted(set("".join(df[text_col].to_list())))
        if chars[0] != pad:
            chars = [pad] + chars
        self.chars = chars
        self.n_chars = len(chars)
        self.char2idx = dict(zip(chars, range(len(chars))))
        
        self.X = [self.encode_string(row) for row in df[text_col]]
        self.y = [self.encode_class(row) for row in df[label_col]]
        
        if max_len is not None:
            if ascending:
                for i, data in enumerate(self.X):
                    if len(data) > max_len:
                        break
                self.X = self.X[:i]
                self.y = self.y[:i]
            else:
                for i, data in enumerate(self.X):
                    if len(data) < max_len:
                        break
                self.X = self.X[i:]
                self.y = self.y[i:]

    def __getitem__(self, index):        
        return self.X[index], self.y[index]

    def __len__(self):
        return len(self.X)
    
    def encode_string(self, text):
        return [self.char2idx[char] for char in text]
    
    def encode_class(self, class_str):
        return self.class2idx[class_str]
    
    def decode_class(self, class_id):
        return self.classes[class_id]
    

class CharRNNDataloader(DataLoader):
    """
    CharRNN Dataloader for PyTorch

    == Arguments ==
    dataset: CharRNNDataset
        the CharRNN dataset object

    batch_size: int
        how many item to sample in each batch

    shuffle: bool
        if True, random sampling is used, sequential sampling is used otherwise.
        It will be neglected when class_sample_weight is provided.

    batch_tranform: transforms.Compose
        list of sequential transformation applied at batch level

    sampler: Sampler or Iterable
        defines the strategy to draw samples from the dataset. Can be any ``Iterable`` with ``__len__`` implemented.
        If specified, :attr:`shuffle` must not be specified.
    
    drop_last: bool
        If True, drop the last incomplete batch

    num_workers: int
        how many subprocesses to use for data loading.
        0 means that the data will be loaded in the main process.
    """        
    def __init__(self, dataset, batch_size=1, shuffle=False, batch_transform=None, sampler=None, drop_last=True, num_workers=0):
        self.transform = batch_transform
        super().__init__(dataset, batch_size, shuffle, sampler=sampler, collate_fn=self.collate, num_workers=num_workers, drop_last=drop_last)

    def collate(self, batch):
        Xb, yb = zip(*batch)
        
        yb = torch.LongTensor(yb)
        
        if self.transform is not None:
            Xb = self.transform(Xb)                
        return Xb, yb
