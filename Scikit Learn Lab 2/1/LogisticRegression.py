
# coding: utf-8

# In[18]:


from sklearn.datasets import load_digits
from sklearn.metrics import roc_curve, auc
import numpy as np
from sklearn.preprocessing import label_binarize
from sklearn.multiclass import OneVsRestClassifier
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.grid_search import GridSearchCV
digits = load_digits()
x = digits.data
y = digits.target
y = label_binarize(y, classes=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
n_classes = y.shape[1]
for i in range(0,5):
    print()
    print("round:",i)
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=.2, random_state=0)
    classifier = LogisticRegression()
    from sklearn.grid_search import GridSearchCV
    parameters = {'C':list(np.power(10.0, np.arange(-10, 3)))
            ,'penalty':['l1','l2']
            ,'max_iter':[100,1000,10000]
            ,'fit_intercept':[True,False]
            ,'tol':[1e-1,1e-2,1e-3,1e-4]}
    LRclf = GridSearchCV(classifier, parameters)
    y_score = LRclf.fit(X_train, y_train.argmax(axis=1))
    y_score1 = y_score.predict_proba(X_test)
    y_score = y_score.predict(X_test)
    fpr = dict()
    tpr = dict()
    roc_auc = dict()
    for i in range(n_classes):
        fpr[i], tpr[i], _ = roc_curve(y_test[:, i], y_score1[:, i])
        roc_auc[i] = auc(fpr[i], tpr[i])
    fpr["micro"], tpr["micro"], _ = roc_curve(y_test.ravel(), y_score1.ravel())
    roc_auc["micro"] = auc(fpr["micro"], tpr["micro"])
    roc_auc[1]

    import matplotlib.pyplot as plt
    from itertools import cycle
    colors = cycle(['aqua', 'darkorange', 'cornflowerblue'])
    for i, color in zip(range(n_classes), colors):
        plt.plot(fpr[i], tpr[i], color=color, lw=2,
                 label='ROC curve of class {0} (area = {1:0.2f})'
                 ''.format(i, roc_auc[i]))

    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver operating characteristic example')
    plt.legend(loc="lower right")
    plt.show()

    from sklearn.metrics import classification_report
    X_train, X_test, y_train, y_test = train_test_split(x, digits.target, test_size=.2, random_state=0)
    y_score = LRclf.fit(X_train, y_train).predict(X_test)
    print("Detailed classification report:")
    print()
    print("The model is trained on the full development set.")
    print("The scores are computed on the full evaluation set.")
    print()
    print(classification_report(y_test, y_score))
    print()


    from sklearn.metrics import confusion_matrix
    matrix = confusion_matrix(y_test, y_score)
    print(matrix)


    score = LRclf.score(X_test, y_test)
    print(score)


    LRclf.best_params_

    LRclf.best_estimator_

    LRclf.best_score_

