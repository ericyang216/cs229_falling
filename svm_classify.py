import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import svm
from sklearn import preprocessing
from sklearn import metrics


# Merge nom and fail, splitting them from head or tail
def data_split(nom, fail, head=True, split=0.80):
    num_nom = nom.shape[0]
    num_fail = fail.shape[0]

    if head:
        x = pd.concat([nom.head(int(num_nom * split)), fail.head(int(num_fail * split))])
    else:
        x = pd.concat([nom.tail(int(num_nom * split)), fail.tail(int(num_fail * split))])

    y_neg = np.zeros(int(num_nom * split))
    y_pos = np.ones(int(num_fail * split))
    y = np.concatenate((y_neg, y_pos))

    # lb = preprocessing.LabelBinarizer()
    # lb.fit([1, -1])
    # y = lb.transform(y)
    # print(y)
    return x, y

# Get list of column names (features)
def filter_features(nom, fail):
    nom = nom.dropna(axis=0,thresh=5).dropna(axis=1)
    fail = nom.dropna(axis=0,thresh=5).dropna(axis=1)

    # for i in range(len(nom)):
    #     if nom[i] != fail[i]:
    #         print("Nominal and failure features don't match")
    #         exit()

    cols = list(nom)
    features = []
    for col in cols:
        if ('raw' in col or 'model' in col
            or 'date' in col
            or 'serial_number' in col
            or 'capacity_bytes' in col
            or 'failure' in col):
            continue
        else:
            features.append(col)

    return features

def evaluation_metric(y_pred, y_label, thresh=0.5):
    if(len(y_pred) != len(y_label)):
        print("Dimension mismatch: comparing predictions {} and labels {}".format(len(y_pred), len(y_label)))
        return

    true_pos = []
    true_neg = []
    false_pos = []
    false_neg = []

    for i in range(len(y_pred)):
        if y_label[i] < thresh and y_pred[i] < thresh:
            true_neg.append(i)
        elif y_label[i] > thresh and y_pred[i] > thresh:
            true_pos.append(i)
        elif y_label[i] < thresh and y_pred[i] > thresh:
            false_pos.append(i)
        elif y_label[i] > thresh and y_pred[i] < thresh:
            false_neg.append(i)

    TP = len(true_pos)
    TN = len(true_neg)
    FP = len(false_pos)
    FN = len(false_neg)

    print("TP:{} TN:{} FP:{} FN:{}".format(TP, TN, FP, FN))

    eval = \
    {
        'accuracy'  : (TP + TN) / (TP + TN + TN + FN),
        'precision' : TP / (TP + FP),
        'recall'    : TP / (TP + FN),
        'f1'        : (2*TP) / (2*TP + FP + FN),
        'roc_auc'   : roc_curve(y_pred, y_label)
    }

    return eval

def roc_curve(scores, y):
    # print(scores)
    # print(y)
    fpr, tpr, thresholds = metrics.roc_curve(y, scores, pos_label=1)
    # print(fpr)
    # print(tpr)
    # print(thresholds)
    roc_auc = metrics.auc(fpr, tpr)

    # plt.plot([0, 1], [0, 1], 'k--', lw=2)
    # plt.plot(fpr, tpr, lw=2, label='ROC curve (area = %0.2f)' % roc_auc)
    # plt.xlim([0.0, 1.0])
    # plt.ylim([0.0, 1.05])
    # plt.xlabel('False Positive Rate')
    # plt.ylabel('True Positive Rate')
    # plt.legend(loc="lower right")
    # plt.show()

    return roc_auc

if __name__ == '__main__':
    nominal_sample = pd.read_csv('/Users/eric/git/cs229/cs229_falling/2015_sample.csv')
    failure_sample = pd.read_csv('/Users/eric/git/cs229/cs229_falling/2015_failures.csv')

    future_nominal = pd.read_csv('/Users/eric/git/cs229/cs229_falling/2018_q1_sample.csv')
    future_failure = pd.read_csv('/Users/eric/git/cs229/cs229_falling/2018_q1_failures.csv')

    features = filter_features(nominal_sample, failure_sample)
    print(features)

    nominal_sample = nominal_sample[features]
    failure_sample = failure_sample[features]

    future_nominal = future_nominal[features]
    future_failure = future_failure[features]
    future_nominial = future_nominal[future_nominal['smart_1_normalized'] >= 0]
    future_failure = future_failure[future_failure['smart_1_normalized'] >= 0]
    # future_nominal[future_nominal.isnull().values]
    # future_failure[future_failure.isnull().values]

    train_x, train_y = data_split(nominal_sample, failure_sample, head=True, split=0.8)
    val_x, val_y = data_split(nominal_sample, failure_sample, head=False, split=0.2)
    future_x, future_y = data_split(future_nominal, future_failure, head=True, split=1.0)

    print(train_x.shape, train_y.shape)
    print(val_x.shape, val_y.shape)
    print(future_x.shape, future_y.shape)



    print("================ Running SVM - linear ================")
    svm_linear = svm.SVC(kernel='linear', gamma='scale', probability=True)
    svm_linear.fit(train_x, train_y)
    train_pred = svm_linear.predict_proba(train_x)[:,1]
    val_pred = svm_linear.predict_proba(val_x)[:,1]
    future_pred = svm_linear.predict_proba(future_x)[:,1]

    train_eval = evaluation_metric(train_pred, train_y)
    val_eval = evaluation_metric(val_pred, val_y)
    future_eval = evaluation_metric(future_pred, future_y)
    print("Train:\n", train_eval)
    print("Val:\n", val_eval)
    print("Future:\n", future_eval)



    print("================ Running SVM - rbf ================")
    svm_rbf = svm.SVC(kernel='rbf', gamma='scale', probability=True)
    svm_rbf.fit(train_x, train_y)

    train_pred = svm_rbf.predict_proba(train_x)[:,1]
    val_pred = svm_rbf.predict_proba(val_x)[:,1]
    future_pred = svm_rbf.predict_proba(future_x)[:,1]

    train_eval = evaluation_metric(train_pred, train_y)
    val_eval = evaluation_metric(val_pred, val_y)
    future_eval = evaluation_metric(future_pred, future_y)

    print("Train:\n", train_eval)
    print("Val:\n", val_eval)
    print("Future:\n", future_eval)


    print("================ Running SVM - poly ================")
    svm_poly = svm.SVC(kernel='poly', gamma='scale', probability=True)
    svm_poly.fit(train_x, train_y)

    train_pred = svm_poly.predict_proba(train_x)[:,1]
    val_pred = svm_poly.predict_proba(val_x)[:,1]
    future_pred = svm_poly.predict_proba(future_x)[:,1]

    train_eval = evaluation_metric(train_pred, train_y)
    val_eval = evaluation_metric(val_pred, val_y)
    future_eval = evaluation_metric(future_pred, future_y)

    print("Train:\n", train_eval)
    print("Val:\n", val_eval)
    print("Future:\n", future_eval)


    print("================ Running SVM - sig ================")
    svm_sig = svm.SVC(kernel='sigmoid', gamma='scale', probability=True)
    svm_poly.fit(train_x, train_y)

    train_pred = svm_sig.predict_proba(train_x)[:,1]
    val_pred = svm_sig.predict_proba(val_x)[:,1]
    future_pred = svm_sig.predict_proba(future_x)[:,1]

    train_eval = evaluation_metric(train_pred, train_y)
    val_eval = evaluation_metric(val_pred, val_y)
    future_eval = evaluation_metric(future_pred, future_y)

    print("Train:\n", train_eval)
    print("Val:\n", val_eval)
    print("Future:\n", future_eval)
