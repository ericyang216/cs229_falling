#helper functions
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn.metrics import roc_curve, precision_recall_curve, auc
from sklearn.metrics import mean_squared_error
from sklearn.metrics import confusion_matrix

import numpy as np

def weighted_evaluation_metrics(y_pred, y_label, sample_weights, thresh=0.5):
    y_pred_ = 1*(y_pred>thresh)
    fpr, tpr, thresholds = roc_curve(y_label, y_pred, pos_label=1, sample_weight=sample_weights)

    eval = \
    {
        'accuracy'  : accuracy_score(y_label, y_pred_), 
        'precision' : precision_score(y_label, y_pred_, pos_label=1, sample_weight=sample_weights),
        'recall'    : recall_score(y_label, y_pred_, pos_label=1, sample_weight=sample_weights),
        'f1'        : f1_score(y_label, y_pred_, pos_label=1, sample_weight=sample_weights),
        'confusion' : confusion_matrix(y_label, y_pred_, sample_weight=sample_weights),
        'roc_auc'   : auc(fpr, tpr),
        'fpr'       : fpr,
        'tpr'       : tpr,
        'thresholds': thresholds,
    }

    return eval

def evaluation_metrics(y_pred, y_label, thresh=0.5):
    #thresh = np.median(y_pred)
    #print(thresh)
    y_pred_ = 1*(y_pred>thresh)
    fpr, tpr, thresholds = roc_curve(y_label, y_pred, pos_label=1)

    eval = \
    {
        'accuracy'  : accuracy_score(y_label, y_pred_), 
        'precision' : precision_score(y_label, y_pred_, pos_label=1),
        'recall'    : recall_score(y_label, y_pred_, pos_label=1),
        'f1'        : f1_score(y_label, y_pred_, pos_label=1),
        'confusion' : confusion_matrix(y_label, y_pred_),
        'roc_auc'   : auc(fpr, tpr),
        'fpr'       : fpr,
        'tpr'       : tpr,
        'thresholds': thresholds,
    }

    return eval

if __name__=='__main__':
    pass