import torch
import numpy as np
from scipy.sparse import coo_matrix
from sklearn.metrics import f1_score


class MiniBatchBinaryConfusionMatrix():
    def __init__(self):
        self.y_true = []
        self.y_pred = []
    
    def add_batch(self, batch_preds, batch_targets):
        """
        batch_preds: (N, F)
        batch_targets: (N,)
        """
        assert batch_preds.ndim == 2
        self.y_pred.append(batch_preds)
        self.y_true.append(batch_targets)
        
    def compute(self):
        """
         |0_|1_|
        0|__|__|
        1|__|__|
        """
        yp = torch.cat(self.y_pred).argmax(1)
        yt = torch.cat(self.y_true)
        
        fn = ((yt == 1) & (yp == 0)).sum().item()
        tp = ((yt == 1) & (yp == 1)).sum().item()
        fp = ((yt == 0) & (yp == 1)).sum().item()
        tn = ((yt == 0) & (yp == 0)).sum().item()       
        return np.array([[tn, fp], [fn, tp]])
    

class MiniBatchConfusionMatrix():
    def __init__(self):
        self.y_true = []
        self.y_pred = []
    
    def add_batch(self, batch_preds, batch_targets):
        """
        batch_preds: (N, F)
        batch_targets: (N,)
        """
        assert batch_preds.ndim == 2
        self.y_pred.append(batch_preds)
        self.y_true.append(batch_targets)
        
    def compute(self):
        """
         |0_|1_|2_|
        0|__|__|__|
        1|__|__|__|
        2|__|__|__|
        """
        yp = torch.cat(self.y_pred).argmax(1).cpu().numpy()
        yt = torch.cat(self.y_true).cpu().numpy()

        sample_weight = np.ones(yt.shape[0], dtype=np.int64)
        cm = coo_matrix((sample_weight, (yt, yp)), dtype=np.int64)
        return cm.toarray()

    
class MiniBatchBinaryF1():
    def __init__(self):
        self.y_true = []
        self.y_pred = []
    
    def add_batch(self, batch_preds, batch_targets):
        """
        batch_preds: (N, F)
        batch_targets: (N,)
        """
        assert batch_preds.ndim == 2
        self.y_pred.append(batch_preds)
        self.y_true.append(batch_targets)
        
    def compute(self, pos_label=1):
        yp = torch.cat(self.y_pred).argmax(1)
        yt = torch.cat(self.y_true)
        
        neg_label = 0 if pos_label else 1        
        fn = ((yt == pos_label) & (yp == neg_label)).sum().item()
        tp = ((yt == pos_label) & (yp == pos_label)).sum().item()
        fp = ((yt == neg_label) & (yp == pos_label)).sum().item()
        return tp / (tp + (fp + fn)/2)
    

class MiniBatchF1Macro():
    def __init__(self):
        self.y_true = []
        self.y_pred = []
    
    def add_batch(self, batch_preds, batch_targets):
        """
        batch_preds: (N, F)
        batch_targets: (N,)
        """
        assert batch_preds.ndim == 2
        self.y_pred.append(batch_preds)
        self.y_true.append(batch_targets)
        
    def compute(self):
        yp = torch.cat(self.y_pred).argmax(1)
        yt = torch.cat(self.y_true)
        return f1_score(yt, yp, average="macro") 
    

class MiniBatchF1Weighted():
    def __init__(self):
        self.y_true = []
        self.y_pred = []
    
    def add_batch(self, batch_preds, batch_targets):
        """
        batch_preds: (N, F)
        batch_targets: (N,)
        """
        assert batch_preds.ndim == 2
        self.y_pred.append(batch_preds)
        self.y_true.append(batch_targets)
        
    def compute(self):
        yp = torch.cat(self.y_pred).argmax(1)
        yt = torch.cat(self.y_true)
        return f1_score(yt, yp, average="weighted")
    

class MiniBatchF1Micro():
    def __init__(self):
        self.y_true = []
        self.y_pred = []
    
    def add_batch(self, batch_preds, batch_targets):
        """
        batch_preds: (N, F)
        batch_targets: (N,)
        """
        assert batch_preds.ndim == 2
        self.y_pred.append(batch_preds)
        self.y_true.append(batch_targets)
        
    def compute(self):
        yp = torch.cat(self.y_pred).argmax(1)
        yt = torch.cat(self.y_true)
        return f1_score(yt, yp, average="micro")    


class MiniBatchBinaryPrecision():
    def __init__(self):
        self.y_true = []
        self.y_pred = []
    
    def add_batch(self, batch_preds, batch_targets):
        """
        batch_preds: (N, F)
        batch_targets: (N,)
        """
        assert batch_preds.ndim == 2
        self.y_pred.append(batch_preds)
        self.y_true.append(batch_targets)
        
    def compute(self, pos_label=1):
        yp = torch.cat(self.y_pred).argmax(1)
        yt = torch.cat(self.y_true)
        
        neg_label = 0 if pos_label else 1        
        tp = ((yt == pos_label) & (yp == pos_label)).sum().item()
        fp = ((yt == neg_label) & (yp == pos_label)).sum().item()
        return tp / (tp + fp)
    
    
class MiniBatchBinaryRecall():
    def __init__(self):
        self.y_true = []
        self.y_pred = []
    
    def add_batch(self, batch_preds, batch_targets):
        """
        batch_preds: (N, F)
        batch_targets: (N,)
        """
        assert batch_preds.ndim == 2
        self.y_pred.append(batch_preds)
        self.y_true.append(batch_targets)
        
    def compute(self, pos_label=1):
        yp = torch.cat(self.y_pred).argmax(1)
        yt = torch.cat(self.y_true)
        
        neg_label = 0 if pos_label else 1        
        fn = ((yt == pos_label) & (yp == neg_label)).sum().item()
        tp = ((yt == pos_label) & (yp == pos_label)).sum().item()
        return tp / (tp + fn)
    
    
class MiniBatchAccuracy():
    def __init__(self):
        self.y_true = []
        self.y_pred = []
    
    def add_batch(self, batch_preds, batch_targets):
        """
        batch_preds: (N, F)
        batch_targets: (N,)
        """
        assert batch_preds.ndim == 2
        self.y_pred.append(batch_preds)
        self.y_true.append(batch_targets)
        
    def compute(self):
        yp = torch.cat(self.y_pred).argmax(1)
        yt = torch.cat(self.y_true)
        return (yp == yt).sum().item() / yp.size(0)


class MiniBatchCost():
    def __init__(self):
        self.cost = 0
        self.total_data = 0

    def add_batch(self, batch_loss, n_data):
        """
        batch_preds: (N, F)
        batch_targets: (N,)
        """
        self.cost += batch_loss.item() * n_data
        self.total_data += n_data
        
    def compute(self):
        return self.cost / self.total_data