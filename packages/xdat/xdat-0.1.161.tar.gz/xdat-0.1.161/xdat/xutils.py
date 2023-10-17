import datetime as dt
import gc

import numpy as np
import pandas as pd
from sklearn import tree, ensemble
from . import xpd, xnp, xplt, xparallel, xplots

MIN_TIME = dt.datetime.min.time()


def x_monkey_patch(aggressive=False):
    xpd.monkey_patch(aggressive=aggressive)
    xnp.monkey_patch()
    xplt.monkey_patch()


def split_X_y(df, target):
    df = df.copy()
    y = df[target]
    del df[target]
    return df, y


def date_to_datetime(d):
    return dt.datetime.combine(d, MIN_TIME)


def x_convert_rf_classifier_to_reg(clf):
    """
    Warning: this function KILLS clf (can't use it after)
    """
    assert len(clf.classes_) == 2, 'only supported for binary situation'

    X = np.zeros((1, clf.n_features_in_))
    y = np.zeros(1)
    reg = ensemble.RandomForestRegressor(n_estimators=clf.n_estimators)
    reg.fit(X, y)
    reg.estimators_ = clf.estimators_.copy()
    estimators2 = []
    for est in reg.estimators_:
        def pred_prob(xx, **kwargs):
            return est.predict_proba(xx)[:, 1]
        est.predict = pred_prob
        tr = tree.DecisionTreeRegressor()
        tr.fit(X, y)

        tr.tree_ = est.tree_
        vals = tr.tree_.value
        for i0 in range(vals.shape[0]):
            for i1 in range(vals.shape[1]):
                sum_val = vals[i0, i1].sum()
                for i2 in range(vals.shape[2]):
                    vals[i0, i1, i2] = vals[i0, i1, 1] / sum_val

        estimators2.append(tr)
    reg.estimators_ = estimators2
    return reg


def x_update_rf_trees(clf, trees):
    clf.estimators_ = trees
    clf.n_estimators = len(trees)
    return clf


def x_shrink_rf(clf_big, X, n_iter=100, plot=True):
    """
    Given clf_big (random forest), finds a smaller forest with similar predictions
    Warning: this KILLS clf_big
    """

    print(f"calculating original prediction (on large model)")
    pred_orig = clf_big.predict_proba(X)[:,1]

    trees = clf_big.estimators_
    print(f"making pred for {len(trees)}")

    def get_tiny_pred(clf):
        clf_tiny = x_update_rf_trees(clf, [clf])
        return clf_tiny.predict_proba(X.to_numpy())[:, 1]

    preds = xparallel.x_on_iter(trees, get_tiny_pred)
    preds = np.array(preds)
    gc.collect()

    print(f"Searching for best trees...")
    def calc_err(pred_orig, pred_try):
        err_try = np.abs(pred_orig - pred_try)
        mean_err_try = err_try.mean()
        max_err_try = err_try.max()
        score_try = np.sqrt(mean_err_try * max_err_try)
        return score_try, mean_err_try, max_err_try

    indexes = []
    bests = []
    scores = []
    for i in range(n_iter):
        def calc_scores(idx):
            idxs_try = indexes + [idx]
            pred_try = preds[idxs_try].mean(axis=0)
            score_try, mean_err_try, max_err_try = calc_err(pred_orig, pred_try)
            return score_try, mean_err_try, max_err_try, tuple(idxs_try)

        best_score, best_mean, best_max, best_idxs = xparallel.x_reduce(list(range(len(trees))), calc_scores, reduce_func=min, backend='threading')

        bests.append([best_score, best_mean, best_max, best_idxs])
        indexes = list(best_idxs)
        print(f'{i}) score={best_score:.6f}, mean={best_mean:.6f}, max={best_max:.6f}')
        scores.append({'score': best_score, 'mean': best_mean, 'max': best_max})

    best_score, best_mean, best_max, best_idxs = bests[-1]
    trees_small = [trees[idx] for idx in best_idxs]
    clf_small = x_update_rf_trees(clf_big, trees_small)

    df_scores = pd.DataFrame(scores)

    del preds, trees
    gc.collect()

    if plot:
        pred_small = clf_small.predict_proba(X)[:, -1]
        err = np.abs(pred_orig - pred_small)
        xplots.plt.hist(err, bins=25)
        xplots.post_plot(title='Train error (difference between large & small model predictions')

    return clf_small, df_scores

