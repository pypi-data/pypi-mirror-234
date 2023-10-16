import json

snippet = {
    "name": "PyTorch x JCOpDL",
    "sub-menu": [{
            "name": "Import common packages",
            "snippet": [
                "import torch",
                "from torch import nn, optim",
                "from jcopdl.callback import Callback",
                "",
                "device = torch.device(\"cuda:0\" if torch.cuda.is_available() else \"cpu\")",
                "device"
            ]
        },
        {
            "name": "Dataset & Dataloader",
            "sub-menu": [{
                    "name": "Torchvision ImageFolder",
                    "snippet": [
                        "from torchvision import datasets, transforms",
                        "from torch.utils.data import DataLoader",
                        "",
                        "bs = \"______\"",
                        "crop_size = \"____\"",
                        "",
                        "train_transform = transforms.Compose([",
                        "    \"____________\",",
                        "    transforms.ToTensor()",
                        "])",
                        "",
                        "test_transform = transforms.Compose([",
                        "    \"____________\",",
                        "    transforms.ToTensor()",
                        "])",
                        "",
                        "train_set = datasets.ImageFolder(\"________\", transform=train_transform)",
                        "trainloader = DataLoader(train_set, batch_size=bs, shuffle=True)",
                        "",
                        "test_set = datasets.ImageFolder(\"________\", transform=test_transform)",
                        "testloader = DataLoader(test_set, batch_size=bs, shuffle=\"____\")",
                        "",
                        "",
                        "configs = {",
                        "    \"crop_size\": crop_size",
                        "}"
                    ]
                },
                {
                    "name": "CharRNN Dataset",
                    "snippet": [
                        "from jcopdl import transforms",
                        "from jcopdl.utils.dataloader import CharRNNDataset, CharRNNDataloader",
                        "",
                        "train_set = CharRNNDataset(\"data / train.csv\", text_col=\"_______\", label_col=\"_______\", max_len=_______)",
                        "test_set = CharRNNDataset(\"data / test.csv\", text_col=\"_______\", label_col=\"_______\", chars=train_set.chars, classes=train_set.classes, pad=train_set.pad, max_len=_______)",
                        "",
                        "transform = transforms.Compose([",
                        "    transforms.PadSequence(),",
                        "    transforms.OneHotEncode(train_set.n_chars),",
                        "    transforms.TruncateSequence(200)",
                        "])",
                        "",
                        "trainloader = CharRNNDataloader(train_set, batch_size=16, batch_transform=transform, drop_last=True)",
                        "testloader = CharRNNDataloader(test_set, batch_size=16, batch_transform=transform, drop_last=True)",
                        "",
                        "",
                        "configs = {",
                        "    \"chars\": train_set.chars,",
                        "    \"classes\": train_set.classes,",
                        "    \"pad\": train_set.pad",
                        "}"
                    ]
                }
            ]
        },
        {
            "name": "Arsitektur & Config",
            "sub-menu": [{
                    "name": "ANN Regression Example",
                    "snippet": [
                        "from torch import nn",
                        "from jcopdl.layers import linear_block",
                        "",
                        "class ANN(nn.Module):",
                        "    def __init__(self, input_size, n1, n2, output_size, dropout):",
                        "        super().__init__()",
                        "        self.fc = nn.Sequential(",
                        "            linear_block(input_size, n1, dropout=dropout),",
                        "            linear_block(n1, n2, dropout=dropout),",
                        "            linear_block(n2, output_size, activation=\"identity\")",
                        "        ),",
                        "    ",
                        "    def forward(self, x):",
                        "        return self.fc(x)",
                        "    ",
                        "",
                        "configs[\"model\"] = {",
                        "    \"input_size\": train_set.n_features,",
                        "    \"n1\": 128,",
                        "    \"n2\": 64,",
                        "    \"output_size\": 1,",
                        "    \"dropout\": 0",
                        "}",
                        "configs[\"optimizer\"] = {",
                        "    \"lr\": 0.001",
                        "}"
                    ]
                },
                {
                    "name": "ANN Classification Example",
                    "snippet": [
                        "from torch import nn",                        
                        "from jcopdl.layers import linear_block",
                        "",
                        "class ANN(nn.Module):",
                        "    def __init__(self, input_size, n1, n2, output_size, dropout):",
                        "        super().__init__()",
                        "        self.fc = nn.Sequential(",
                        "            linear_block(input_size, n1, dropout=dropout),",
                        "            linear_block(n1, n2, dropout=dropout),",
                        "            linear_block(n2, output_size, activation=\"lsoftmax\")",
                        "        ),",
                        "    ",
                        "    def forward(self, x):",
                        "        return self.fc(x)",
                        "    ",
                        "",
                        "configs[\"model\"] = {",
                        "    \"input_size\": train_set.n_features,",
                        "    \"n1\": 128,",
                        "    \"n2\": 64,",
                        "    \"output_size\": 1,",
                        "    \"dropout\": 0",
                        "}",
                        "configs[\"optimizer\"] = {",
                        "    \"lr\": 0.001",
                        "}"
                    ]
                },
                {
                    "name": "CNN Classification Example",
                    "snippet": [
                        "from torch import nn",                        
                        "from jcopdl.layers import linear_block, conv_block",
                        "",
                        "class CNN(nn.Module):",
                        "    def __init__(self, output_size, fc_dropout):",
                        "        super().__init__()",
                        "        self.conv = nn.Sequential(",
                        "            conv_block(\"___\", \"___\"),",
                        "            conv_block(\"___\", \"___\"),",
                        "            nn.Flatten()",
                        "        )",
                        "        ",
                        "        self.fc = nn.Sequential(",
                        "            linear_block(\"_____\", \"_____\", dropout=fc_dropout),",
                        "            linear_block(\"_____\", output_size, activation=\"lsoftmax\")",
                        "        )",
                        "        ",
                        "    def forward(self, x):",
                        "        return self.fc(self.conv(x))",
                        "    ",
                        "",
                        "configs[\"model\"] = {",
                        "    \"output_size\": len(train_set.classes),",
                        "    \"fc_dropout\": 0",
                        "}",
                        "configs[\"optimizer\"] = {",
                        "    \"lr\": 0.001",
                        "}"
                    ]
                },
                {
                    "name": "Many to Many RNN Example",
                    "snippet": [
                        "from torch import nn",                        
                        "from jcopdl.layers import linear_block",
                        "",
                        "class ManytoManyRNN(nn.Module):",
                        "    def __init__(self, input_size, output_size, hidden_size, num_layers, dropout):",
                        "        super().__init__()",
                        "        self.rnn = nn.RNN(input_size, hidden_size, num_layers, dropout=dropout, batch_first=True)",
                        "        self.fc = linear_block(hidden_size, output_size, activation=\"identity\")",
                        "        ",
                        "    def forward(self, x, hidden):        ",
                        "        x, hidden = self.rnn(x, hidden)",
                        "        x = self.fc(x)",
                        "        return x, hidden",
                        "",
                        "",
                        "configs[\"model\"] = {",
                        "    \"input_size\": ________,",
                        "    \"output_size\": ________,",
                        "    \"hidden_size\": 64,",
                        "    \"num_layers\": 2,",
                        "    \"dropout\": 0",
                        "}",
                        "configs[\"optimizer\"] = {",
                        "    \"lr\": 0.001",
                        "}"
                    ]
                },
                {
                    "name": "Many to One RNN Example",
                    "snippet": [
                        "from torch import nn",                        
                        "from jcopdl.layers import linear_block",
                        "",
                        "class ManyToOneRNN(nn.Module):",
                        "    def __init__(self, input_size, output_size, hidden_size, num_layers, dropout):",
                        "        super().__init__()",
                        "        self.rnn = nn.RNN(input_size, hidden_size, num_layers, dropout=dropout, batch_first=True)",
                        "        self.fc = linear_block(num_layers*hidden_size, output_size, activation=\"lsoftmax\")",
                        "        ",
                        "    def forward(self, x, hidden):        ",
                        "        x, hidden = self.rnn(x, hidden)",
                        "        n_layers, n_batch, n_hidden = hidden.shape",
                        "        last_state = hidden.permute(1, 0, 2).reshape(-1, n_layers*n_hidden) # LBH -> BLH -> BF",
                        "        x = self.fc(last_state)",
                        "        return x, hidden",
                        "",
                        "",
                        "configs[\"model\"] = {",
                        "    \"input_size\": ________,",
                        "    \"output_size\": ________,",
                        "    \"hidden_size\": 64,",
                        "    \"num_layers\": 2,",
                        "    \"dropout\": 0",
                        "}",
                        "configs[\"optimizer\"] = {",
                        "    \"lr\": 0.001",
                        "}"
                    ]
                },
                {
                    "name": "Many to Many LSTM Example",
                    "snippet": [
                        "from torch import nn",                        
                        "from jcopdl.layers import linear_block",
                        "",
                        "class ManytoManyLSTM(nn.Module):",
                        "    def __init__(self, input_size, output_size, hidden_size, num_layers, dropout):",
                        "        super().__init__()",
                        "        self.rnn = nn.LSTM(input_size, hidden_size, num_layers, dropout=dropout, batch_first=True)",
                        "        self.fc = linear_block(hidden_size, output_size, activation=\"identity\")",
                        "        ",
                        "    def forward(self, x, hidden):        ",
                        "        x, hidden = self.rnn(x, hidden)",
                        "        x = self.fc(x)",
                        "        return x, hidden",
                        "",
                        "",
                        "configs[\"model\"] = {",
                        "    \"input_size\": ________,",
                        "    \"output_size\": ________,",
                        "    \"hidden_size\": 64,",
                        "    \"num_layers\": 2,",
                        "    \"dropout\": 0",
                        "}",
                        "configs[\"optimizer\"] = {",
                        "    \"lr\": 0.001",
                        "}"
                    ]
                },
                {
                    "name": "Many to One LSTM Example",
                    "snippet": [
                        "from torch import nn",                        
                        "from jcopdl.layers import linear_block",
                        "",
                        "class ManyToOneLSTM(nn.Module):",
                        "    def __init__(self, input_size, output_size, hidden_size, num_layers, dropout):",
                        "        super().__init__()",
                        "        self.rnn = nn.LSTM(input_size, hidden_size, num_layers, dropout=dropout, batch_first=True)",
                        "        self.fc = linear_block(num_layers*2*hidden_size, output_size, activation=\"lsoftmax\")",
                        "        ",
                        "    def forward(self, x, hidden):        ",
                        "        x, (h, c) = self.rnn(x, hidden)",
                        "        state = torch.cat([h, c], dim=2)",
                        "        n_layers, n_batch, n_2hidden = state.shape",
                        "        last_state = state.permute(1, 0, 2).reshape(-1, n_layers*n_2hidden) # LBH -> BLH -> BF",
                        "        x = self.fc(last_state)",
                        "        return x, (h, c)",
                        "",
                        "",
                        "configs[\"model\"] = {",
                        "    \"input_size\": ________,",
                        "    \"output_size\": ________,",
                        "    \"hidden_size\": 64,",
                        "    \"num_layers\": 2,",
                        "    \"dropout\": 0",
                        "}",
                        "configs[\"optimizer\"] = {",
                        "    \"lr\": 0.001",
                        "}"
                    ]
                },
                {
                    "name": "Many to Many GRU Example",
                    "snippet": [
                        "from torch import nn",                        
                        "from jcopdl.layers import linear_block",
                        "",
                        "class ManytoManyGRU(nn.Module):",
                        "    def __init__(self, input_size, output_size, hidden_size, num_layers, dropout):",
                        "        super().__init__()",
                        "        self.rnn = nn.GRU(input_size, hidden_size, num_layers, dropout=dropout, batch_first=True)",
                        "        self.fc = linear_block(hidden_size, output_size, activation=\"identity\")",
                        "        ",
                        "    def forward(self, x, hidden):        ",
                        "        x, hidden = self.rnn(x, hidden)",
                        "        x = self.fc(x)",
                        "        return x, hidden",
                        "",
                        "",
                        "configs[\"model\"] = {",
                        "    \"input_size\": ________,",
                        "    \"output_size\": ________,",
                        "    \"hidden_size\": 64,",
                        "    \"num_layers\": 2,",
                        "    \"dropout\": 0",
                        "}",
                        "configs[\"optimizer\"] = {",
                        "    \"lr\": 0.001",
                        "}"
                    ]
                },
                {
                    "name": "Many to One GRU Example",
                    "snippet": [
                        "from torch import nn",                        
                        "from jcopdl.layers import linear_block",
                        "",
                        "class ManyToOneGRU(nn.Module):",
                        "    def __init__(self, input_size, output_size, hidden_size, num_layers, dropout):",
                        "        super().__init__()",
                        "        self.rnn = nn.GRU(input_size, hidden_size, num_layers, dropout=dropout, batch_first=True)",
                        "        self.fc = linear_block(num_layers*hidden_size, output_size, activation=\"lsoftmax\")",
                        "        ",
                        "    def forward(self, x, hidden):        ",
                        "        x, hidden = self.rnn(x, hidden)",
                        "        n_layers, n_batch, n_hidden = hidden.shape",
                        "        last_state = hidden.permute(1, 0, 2).reshape(-1, n_layers*n_hidden) # LBH -> BLH -> BF",
                        "        x = self.fc(last_state)",
                        "        return x, hidden",
                        "",
                        "",
                        "configs[\"model\"] = {",
                        "    \"input_size\": ________,",
                        "    \"output_size\": ________,",
                        "    \"hidden_size\": 64,",
                        "    \"num_layers\": 2,",
                        "    \"dropout\": 0",
                        "}",
                        "configs[\"optimizer\"] = {",
                        "    \"lr\": 0.001",
                        "}"
                    ]
                }
            ]
        },
        {
            "name": "Training Preparation (MCOC)",
            "snippet": [
                "model = _______(**configs[\"model\"]).to(device)",
                "criterion = _______",
                "optimizer = optim.AdamW(model.parameters(), **configs[\"optimizer\"])",
                "callback = Callback(model, configs, optimizer, outdir=\"output\")"
            ]
        },
        {
            "name": "Add Plot to Callback",
            "sub-menu": [{
                    "name": "Cost",
                    "snippet": [
                        "callback.add_plot([\"train_cost\", \"test_cost\"], scale=\"semilogy\")"
                    ]
                },
                {
                    "name": "Score",
                    "snippet": [
                        "callback.add_plot([\"train_score\", \"test_score\"], scale=\"linear\")"
                    ]
                },
                {
                    "name": "Image",
                    "snippet": [
                        "callback.add_image(\"test_predict\")"
                    ]
                }
            ]
        },
        {
            "name": "Training Loop Function",
            "sub-menu": [{
                    "name": "Basic + Cost + Acc",
                    "snippet": [
                        "from tqdm.auto import tqdm",
                        "from jcopdl.metrics import MiniBatchCost, MiniBatchAccuracy",
                        "from jcopdl.visualization import visualize_prediction_batch",
                        "",
                        "",
                        "def train_loop_fn(mode, dataloader, model, criterion, optimizer, callback, device):",
                        "    if mode == \"train\":",
                        "        model.train()",
                        "    elif mode == \"test\":",
                        "        model.eval()",
                        "    ",
                        "    cost = MiniBatchCost()",
                        "    score = MiniBatchAccuracy()",
                        "    for feature, target in tqdm(dataloader, desc=mode.title(), leave=False):",
                        "        feature, target = feature.to(device), target.to(device)",
                        "        output = model(feature)",
                        "        loss = criterion(output, target)",
                        "        ",
                        "        if mode == \"train\":",
                        "            loss.backward()",
                        "            optimizer.step()",
                        "            optimizer.zero_grad()",
                        "",
                        "        cost.add_batch(loss, feature.size(0))",
                        "        score.add_batch(output, target)",
                        "    callback.log(f\"{mode}_cost\", cost.compute())",
                        "    callback.log(f\"{mode}_score\", score.compute())",
                        "    ",
                        "    if mode == \"test\":",
                        "        preds = output.argmax(1)",
                        "        classes = dataloader.dataset.classes",
                        "        image = visualize_prediction_batch(feature, target, preds, classes)",
                        "        callback.log_image(\"test_predict\", image)"
                    ]
                },
                {
                    "name": "Basic + Cost + F1",
                    "snippet": [
                        "from tqdm.auto import tqdm",
                        "from jcopdl.metrics import MiniBatchCost, MiniBatchBinaryF1",
                        "",
                        "",
                        "def train_loop_fn(mode, dataloader, model, criterion, optimizer, callback, device):",
                        "    if mode == \"train\":",
                        "        model.train()",
                        "    elif mode == \"test\":",
                        "        model.eval()",
                        "    ",
                        "    cost = MiniBatchCost()",
                        "    score = MiniBatchBinaryF1()",
                        "    for feature, target in tqdm(dataloader, desc=mode.title(), leave=False):",
                        "        feature, target = feature.to(device), target.to(device)",
                        "        output = model(feature)",
                        "        loss = criterion(output, target)",
                        "        ",
                        "        if mode == \"train\":",
                        "            loss.backward()",
                        "            optimizer.step()",
                        "            optimizer.zero_grad()",
                        "",
                        "        cost.add_batch(loss, feature.size(0))",
                        "        score.add_batch(output, target)",
                        "    callback.log(f\"{mode}_cost\", cost.compute())",
                        "    callback.log(f\"{mode}_score\", score.compute(pos_label=1))"                   
                    ]
                },
                {
                    "name": "RNN + Cost + F1",
                    "snippet": [
                        "from tqdm.auto import tqdm",
                        "from torch.nn.utils import clip_grad_norm_",
                        "from jcopdl.metrics import MiniBatchCost, MiniBatchBinaryF1",
                        "",
                        "",
                        "def train_loop_fn(mode, dataloader, model, criterion, optimizer, callback, device):",
                        "    if mode == \"train\":",
                        "        model.train()",
                        "    elif mode == \"test\":",
                        "        model.eval()",
                        "    ",
                        "    cost = MiniBatchCost()",
                        "    score = MiniBatchBinaryF1()",
                        "    for feature, target in tqdm(dataloader, desc=mode.title(), leave=False):",
                        "        feature, target = feature.to(device), target.to(device)",
                        "        output, hidden = model(feature, None)",
                        "        loss = criterion(output, target)",
                        "        ",
                        "        if mode == \"train\":",
                        "            loss.backward()",
                        "            clip_grad_norm_(model.parameters(), 2)",
                        "            optimizer.step()",
                        "            optimizer.zero_grad()",
                        "",
                        "        cost.add_batch(loss, feature.size(0))",
                        "        score.add_batch(output, target)",
                        "    callback.log(f\"{mode}_cost\", cost.compute())",
                        "    callback.log(f\"{mode}_score\", score.compute(pos_label=1))"
                    ]
                },
                {
                    "name": "RNN + TBPTT + Cost + F1",
                    "snippet": [
                        "from tqdm.auto import tqdm",
                        "from torch.nn.utils import clip_grad_norm_",
                        "from jcopdl.metrics import MiniBatchCost, MiniBatchBinaryF1",
                        "",
                        "",
                        "def train_loop_fn(mode, dataloader, model, criterion, optimizer, callback, device):",
                        "    if mode == \"train\":",
                        "        model.train()",
                        "    elif mode == \"test\":",
                        "        model.eval()",
                        "    ",
                        "    cost = MiniBatchCost()",
                        "    score = MiniBatchBinaryF1()",
                        "    for (prior, feature), target in tqdm(dataloader, desc=mode.title(), leave=False):",
                        "        prior, feature, target = prior.to(device), feature.to(device), target.to(device)",
                        "        with torch.no_grad():",
                        "            output, hidden = model(prior, None)",
                        "        output, hidden = model(feature, hidden)",
                        "        loss = criterion(output, target)",
                        "        ",
                        "        if mode == \"train\":",
                        "            loss.backward()",
                        "            clip_grad_norm_(model.parameters(), 2)",
                        "            optimizer.step()",
                        "            optimizer.zero_grad()",
                        "",
                        "        cost.add_batch(loss, feature.size(0))",
                        "        score.add_batch(output, target)",
                        "    callback.log(f\"{mode}_cost\", cost.compute())",
                        "    callback.log(f\"{mode}_score\", score.compute(pos_label=1))"
                    ]
                }
            ]
        },
        {
            "name": "Training",
            "sub-menu": [{
                    "name": "Minimize Cost",
                    "snippet": [
                        "while True:",
                        "    train_loop_fn(\"train\", trainloader, model, criterion, optimizer, callback, device)",
                        "    with torch.no_grad():",
                        "        train_loop_fn(\"test\", testloader, model, criterion, optimizer, callback, device)",
                        "    ",
                        "    if callback.early_stopping(\"minimize\", \"test_cost\"):",
                        "        break"
                    ]
                },
                {
                    "name": "Maximize Score",
                    "snippet": [
                        "while True:",
                        "    train_loop_fn(\"train\", trainloader, model, criterion, optimizer, callback, device)",
                        "    with torch.no_grad():",
                        "        train_loop_fn(\"test\", testloader, model, criterion, optimizer, callback, device)",
                        "    ",
                        "    if callback.early_stopping(\"maximize\", \"test_score\"):",
                        "        break"
                    ]
                }
            ]
        },
        {
            "name": "Evaluation",
            "sub-menu": [{
                    "name": "Visualize Prediction",
                    "snippet": [
                        "from jcopdl.eval import evaluate_prediction",
                        "",                       
                        "with torch.no_grad():",
                        "    img_train = evaluate_prediction(trainloader, model, device)",
                        "    img_test = evaluate_prediction(testloader, model, device)"
                    ]
                },{
                    "name": "Evaluate Accuracy",
                    "snippet": [
                        "from jcopdl.eval import evaluate_accuracy",
                        "",                             
                        "with torch.no_grad():",
                        "    acc_train = evaluate_accuracy(trainloader, model, device)",
                        "    acc_test = evaluate_accuracy(testloader, model, device)"
                    ]
                },{
                    "name": "Evaluate Confusion Matrix",
                    "snippet": [
                        "from jcopdl.eval import evaluate_confusion_matrix",
                        "from jcopdl.visualization import plot_confusion_matrix",
                        "",
                        "with torch.no_grad():",
                        "    cm_train = evaluate_confusion_matrix(trainloader, model, device)",
                        "    cm_test = evaluate_confusion_matrix(testloader, model, device)",
                        "",
                        "fig_train = plot_confusion_matrix(cm_train, train_set.classes)",
                        "fig_test = plot_confusion_matrix(cm_test, test_set.classes)"
                    ]
                }
            ]
        },
        {
            "name": "Load Model",
            "sub-menu": [{
                    "name": "Continue from Checkpoint",
                    "snippet": [
                        "from jcopdl.io import load_from_checkpoint",
                        "",                       
                        "checkpoint = load_from_checkpoint(\"output/checkpoint/_________.pth\")",
                        "model, optimizer, scheduler, callback = checkpoint.model, checkpoint.optimizer, checkpoint.scheduler, checkpoint",
                        "criterion = _______"
                    ]
                },{
                    "name": "Load best model",
                    "snippet": [
                        "import torch",
                        "device = torch.device(\"cuda:0\" if torch.cuda.is_available() else \"cpu\")",
                        "",                             
                        "model = torch.load(\"output/model_best.pth\", map_location=\"cpu\").to(device)"
                    ]
                },{
                    "name": "Load config, metadata, etc",
                    "snippet": [
                        "import torch",
                        "",
                        "configs = torch.load(\"output/configs.pth\")"
                    ]
                }
            ]
        }
    ]
}

print(json.dumps(snippet, indent=4))
