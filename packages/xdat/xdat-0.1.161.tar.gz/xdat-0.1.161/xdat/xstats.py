from collections import namedtuple
import numpy as np
from scipy import stats, linalg
from sklearn import metrics, base

ModelPredStats = namedtuple("ModelPredStats", ["r2", "r2_adj", "p_value", "corr", "mae", "rmse", "p_value_err_normal", "kappa", "matthew", "auc"])


def x_model_pred_stats(y_true, y_pred, y_alt='mean', k=None, y_score=None, is_classification=True):
    """
    Calculates various statistics on model predictions, including:
        p_value: the p_value of the test that the absolute errors of the pred are less than the absolute errors of the alt
        p_value_err_normal: the p_value of the test that the errors are normally distributed
        r2_adj: adjusted r-squared (requires the k parameter to be set)
        y_score: score array for binary (or matrix for multiclass)
        is_classification: True for classification, False for regression

    Args:
        y_true: true values
        y_pred: predicted values
        y_alt: alternative (null) model, typically mean of train data
        k: number of variables in the model (for calculating r2_adj)

    Returns: ModelPredStats
    """
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)

    if y_alt == 'mean':
        y_alt = y_true.mean()

    err_pred = np.abs(y_true - y_pred)
    err_alt = np.abs(y_true - y_alt)

    res = stats.ttest_rel(err_pred, err_alt, alternative='less')
    p_value = res.pvalue
    if p_value is np.nan:
        p_value = None

    errors = y_true - y_pred
    p_value_err_normal = None
    try:
        p_value_err_normal = stats.normaltest(errors).pvalue
    except ValueError:
        pass

    if p_value_err_normal is np.nan:
        p_value_err_normal = None

    if not is_classification:
        r2 = metrics.r2_score(y_true, y_pred)
        n = len(y_true)
        r2_adj = None
        if k is not None and n - k - 1 > 0:
            r2_adj = 1 - ((1-r2)*(n-1))/(n-k-1)

        corr = np.corrcoef(y_true, y_pred)[0, 1]
    else:
        r2 = r2_adj = corr = None

    mae = np.mean(err_pred)
    rmse = metrics.mean_squared_error(y_true, y_pred, squared=False)

    kappa = None        # good for multiclass as well
    matthew = None      # good for multiclass as well
    auc = None          # good for multiclass as well  (OvR)
    if is_classification:
        kappa = metrics.cohen_kappa_score(y_true, y_pred)
        matthew = metrics.matthews_corrcoef(y_true, y_pred)
        if y_score is not None:
            if len(y_score.shape) == 2 and y_score.shape[1] == 2:
                y_score = y_score[:, 1]

            if len(y_score.shape) == 1:
                auc = metrics.roc_auc_score(y_true, y_score)
            else:
                auc = metrics.roc_auc_score(y_true, y_score, multi_class='ovr', average='weighted')

    res = ModelPredStats(r2=r2, r2_adj=r2_adj, p_value=p_value, corr=corr, mae=mae, rmse=rmse,
        p_value_err_normal=p_value_err_normal, kappa=kappa, matthew=matthew, auc=auc)
    return res


def x_auc_values(a_lower, a_higher):
    assert len(a_lower) > 0
    assert len(a_higher) > 0
    a_true = np.array([0]*len(a_lower) + [1]*len(a_higher))
    a_actual = np.array(a_lower.tolist() + a_higher.tolist())
    auc = metrics.roc_auc_score(a_true, a_actual)
    return auc


class MahalanobisDistance(base.BaseEstimator):
    """
    Credits: https://www.machinelearningplus.com/statistics/mahalanobis-distance/
    """
    def __init__(self):
        super().__init__()
        self.mean = None
        self.cov = None
        self.inv_covmat = None

        # self.post_scaler = preprocessing.StandardScaler()

    def fit(self, X, y=None):
        self.mean = np.mean(X)
        self.cov = np.cov(X.values.T)
        self.inv_covmat = linalg.inv(self.cov)

    def transform(self, X, y=None):
        x_minus_mu = X - self.mean
        left_term = np.dot(x_minus_mu, self.inv_covmat)
        mahal = np.dot(left_term, x_minus_mu.T)
        diag = mahal.diagonal()
        return diag.reshape(-1, 1)

    def fit_transform(self, X, y=None):
        self.fit(X)
        return self.transform(X)


if __name__ == "__main__":
    from sklearn import datasets, ensemble, model_selection
    # from xdat import xproblem
    for loader in [datasets.load_breast_cancer, datasets.load_wine]:
        print(loader.__name__)
        X, y = loader(return_X_y=True)
        X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, train_size=0.5)
        clf = ensemble.RandomForestClassifier(n_estimators=1, max_depth=3)
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)
        y_score = clf.predict_proba(X_test)
        print(x_model_pred_stats(y_test, y_pred, y_score=y_score))
    print('hi')