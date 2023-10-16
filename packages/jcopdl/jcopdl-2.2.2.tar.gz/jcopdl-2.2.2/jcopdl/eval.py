from tqdm.auto import tqdm
from jcopdl.metrics import MiniBatchConfusionMatrix, MiniBatchAccuracy
from jcopdl.visualization import visualize_prediction_batch

__all__ = [
    "evaluate_confusion_matrix",
    "evaluate_accuracy",
    "evaluate_prediction"
]


def evaluate_confusion_matrix(dataloader, model, device, desc=""):
    model.eval()
    metric = MiniBatchConfusionMatrix()
    for feature, target in tqdm(dataloader, desc=desc.title(), leave=False):
        feature, target = feature.to(device), target.to(device)
        output = model(feature)
        metric.add_batch(output, target)
    return metric.compute()


def evaluate_accuracy(dataloader, model, device, desc=""):
    model.eval()
    metric = MiniBatchAccuracy()
    for feature, target in tqdm(dataloader, desc=desc.title(), leave=False):
        feature, target = feature.to(device), target.to(device)
        output = model(feature)
        metric.add_batch(output, target)
    return metric.compute()


def evaluate_prediction(dataloader, model, device, viz_transform=None):
    model.eval()
    feature, target = next(iter(dataloader))
    feature, target = feature.to(device), target.to(device)
    output = model(feature)
    
    preds = output.argmax(1)
    classes = dataloader.dataset.classes
    if viz_transform is not None:
        feature = viz_transform(feature)
    image = visualize_prediction_batch(feature, target, preds, classes)
    return image
