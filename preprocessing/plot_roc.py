import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
sns.set()
import torch
from utils.utils import load_dataset, load_obj
from sklearn.metrics import roc_curve, auc
from models.ssd.utils import find_jaccard_overlap
from utils.evaluate import *

base_path = "/home/salvacarrion/Documents/Programming/Python/Projects/yolo4math/models/yolov3"
predictions = load_obj(base_path + "/predictions.pkl")
confusion_matrix = load_obj(base_path + "/confusion_matrix.pkl")
stats = load_dataset(base_path + "/stats.json")


det_boxes = predictions['det_boxes']
det_labels = predictions['det_labels']
det_scores = predictions['det_scores']
true_boxes = predictions['true_boxes']
true_labels = predictions['true_labels']


# det_labels = ignore_bg(det_labels)
# true_labels = ignore_bg(true_labels)

pred_class, pred_score, pred_iou, true_class = match_classes(det_boxes, det_labels, det_scores, true_boxes, true_labels, n_classes=2)
pred_correctness = (pred_class == true_class) * (pred_iou > 0.5)

# Set background at index 0
pred_class += 1
true_class += 1

# Compute ROC curve and ROC area for each class
fpr = dict()
tpr = dict()
roc_auc = dict()
for c in range(1, 3):
    y = pred_correctness[true_class == c]  # Correctness of predictions from class c
    y_scores = pred_score[true_class == c]
    fpr[c], tpr[c], _ = roc_curve(y.cpu().data.numpy(), y_scores.cpu().data.numpy())
    roc_auc[c] = auc(fpr[c], tpr[c])

# Plot ROC curve
plt.figure()
for i, cls in enumerate(['Embedded', 'Isolated'], 1):
    plt.plot(fpr[i], tpr[i], label="ROC curve for '{0}' (area = {1:0.2f})"
                                   ''.format(cls, roc_auc[i]))

plt.plot([0, 1], [0, 1], 'k--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC curve')
plt.legend(loc="lower right")
plt.savefig('roc-curve-yolov3.eps')
plt.show()

asdasd =3
