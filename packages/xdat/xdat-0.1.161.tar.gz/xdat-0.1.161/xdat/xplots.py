from contextlib import contextmanager
import datetime as dt
import pandas as pd
import seaborn as sns
import numpy as np
import arviz as az

from sklearn import linear_model
from sklearn import metrics
from scipy import stats
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
from matplotlib.pyplot import subplots
import matplotlib
from matplotlib.colors import to_rgba
from ds_utils.metrics import plot_confusion_matrix as _plot_confusion_matrix, visualize_accuracy_grouped_by_probability
from sklearn.tree import plot_tree
from venn import venn
from scriptine import path

from . import xproblem, xpd, xsettings, xcalc, xstats, xpptx


FORMATTER_TIME = mdates.DateFormatter('%H:%M')
FORMATTER_PERC = mticker.PercentFormatter(xmax=1.0)
FORMATTER_INT = int


def merge_titles(title1, title2):
    title1 = title1 or ''
    title2 = title2 or ''

    if not title1:
        return title2

    if not title2:
        return title1

    if title1.endswith('\n'):
        return f"{title1}{title2}"

    if title1.endswith(': '):
        return f"{title1}{title2}"

    if title1.endswith(':'):
        return f"{title1} {title2}"

    return f"{title1}: {title2}"


def merge_title_desc(title, desc, as_xpptx):
    if as_xpptx and not as_xpptx.fake:
        return title, desc

    if not desc:
        if '(' in title:
            idx = title.find('(')
            title, desc = title[:idx], title[idx-1:]

    title = merge_titles(title, desc)
    return title, ''


def plot_gini(a, num_bins=101, xlabel='samples', ylabel='values', title='', figsize=(8,8)):
    """
    Credit: https://stackoverflow.com/questions/39512260/calculating-gini-coefficient-in-python-numpy
    """
    a = pd.Series(a)
    a = a.dropna()
    np.sort(a)
    gini_val = xcalc.x_calc_gini(a, presorted=True)

    def G(v):
        bins = np.linspace(0., 100., num_bins)
        total = float(np.sum(v))
        yvals = []
        for b in bins:
            bin_vals = v[v <= np.percentile(v, b)]
            bin_fraction = (np.sum(bin_vals) / total) * 100.0
            yvals.append(bin_fraction)

        return bins, yvals

    bins, result = G(a)
    plt.figure(figsize=figsize)
    # plt.subplot(2, 1, 1)
    plt.plot(bins, result, label="observed")
    plt.plot(bins, bins, '--', label="perfect eq.")
    plt.xlabel(f"fraction of {xlabel}")
    plt.ylabel(f"fraction of {ylabel}")
    title2 = merge_titles(title, f"GINI={gini_val:.4f}")
    plt.title(title2)
    plt.legend()
    # plt.subplot(2, 1, 2)
    # plt.hist(a, bins=20)
    plt.tight_layout()
    plt.show()


def plot_beta_prob_dists(df, n_col=None, success_col=None, fail_col=None, label_on=None, title='', xlabel='probability of success'):
    pre_plot()
    for _, row in df.iterrows():
        success = None
        fail = None
        if success_col:
            success = row[success_col]
        if fail_col:
            fail = row[fail_col]
        if n_col:
            n = row[n_col]
            if success is not None:
                fail = n - success
            elif fail is not None:
                success = n - fail

        assert success is not None
        assert fail is not None
        n = success + fail

        label = ''
        if label_on:
            label = row[label_on]
        label = f"{label} ({success:.0f}/{n:.0f})"

        rv = stats.beta(success+1, fail+1)
        x = np.linspace(0.001, 0.999, 1000)
        plt.plot(x, rv.pdf(x), lw=1, label=label)

    post_plot(title=title, ylabel=False, xlabel=xlabel)


def plot_feature_importances(folds, title='', top_k=None, show=True, as_xpptx=None, also_text=False):
    df = xproblem.calc_feature_importances(folds, flat=True)
    if df is None:
        return

    fis = df.groupby('feature_name')['feature_importance'].mean()
    fis = fis.sort_values(ascending=False)
    if top_k:
        fis = fis[:top_k]
        df = df[df.feature_name.isin(fis.index.values)]

    df = xpd.x_sort_on_lookup(df, 'feature_name', fis, ascending=True)

    sns.catplot(data=df, y='feature_name', x='feature_importance', height=6, aspect=1.5).set(title=title)
    post_plot(xlim=[0, None], show=show, as_xpptx=as_xpptx)

    if also_text:
        print(fis.to_string())


def plot_roc_curve(y_true, y_score, title='', show=True, as_xpptx=None):
    auc = metrics.roc_auc_score(y_true, y_score)
    fper, tper, thresholds = metrics.roc_curve(y_true, y_score)
    plt.plot(fper, tper, color='orange', label='ROC')
    plt.fill_between(fper, tper, color='orange', alpha=0.1)
    plt.plot([0, 1], [0, 1], color='darkblue', linestyle='--')

    xlabel = 'False Positive Rate'
    ylabel = 'True Positive Rate'
    desc = f'ROC Curve (AUC={auc:.3f})'

    if as_xpptx is None or as_xpptx.fake:
        if title:
            title = f"{title}\n{desc}"
        else:
            title = desc

        desc = ''

    post_plot(title=title, desc=desc, xlim=[0, None], xlabel=xlabel, ylabel=ylabel, show=show, as_xpptx=as_xpptx)

    return auc


def plot_confusion_matrix(y_true, y_pred, y_score=None, labels=None, classes=None, title='', show=True, as_xpptx=None):
    auc = metrics.roc_auc_score(y_true, y_score) if y_score is not None else None

    y_true = pd.Series(y_true)
    classes = classes or sorted(y_true.unique())

    if labels:
        replace_dict = {k:v for k,v in zip(classes, labels)}
        y_true = xpd.x_replace(y_true, valid_vals='all', replace_vals=replace_dict)
        y_pred = xpd.x_replace(y_pred, valid_vals='all', replace_vals=replace_dict)

        classes = [replace_dict[k] for k in classes]

    counts = sorted([(l, c) for l, c in y_true.value_counts().items()])
    counts_str = ", ".join([f"{l}={c}" for l, c in counts])

    _plot_confusion_matrix(y_true, y_pred, labels=classes, cbar=False)

    desc = f"Counts: {counts_str} (total={len(y_true)})"
    if auc is not None:
        desc = f"{desc} AUC={auc:.3f}"

    title, desc = merge_title_desc(title, desc, as_xpptx)
    post_plot(title=title, legend=False, show=show, as_xpptx=as_xpptx, desc=desc)


def plot_model_reg_pred(df, target='target', title='', df_train=None, as_xpptx=None, show=True):
    with plot_wrapper(title=title, legend_loc='lower right', as_xpptx=as_xpptx, show=show):
        plot_multi(df, kind='reg', x=target, y='pred', show=False)

        if 'pred_conf' in df.columns:
            df = df.sort_values(target)
            plt.fill_between(df[target], df['pred_conf'].apply(min), df['pred_conf'].apply(max), alpha=0.3, color='xkcd:sky blue', label='predicted')

        if 'pred_low' in df.columns and 'pred_high' in df.columns:
            df = df.sort_values(target)
            plt.fill_between(df[target], df['pred_low'], df['pred_high'], alpha=0.3, color='xkcd:sky blue', label='predicted')

        plt.plot([df[target].min(), df[target].max()], [df[target].min(), df[target].max()], color='xkcd:red', ls='--', label='actual')

        if df_train is not None:
            xmin = max(df_train[target].min(), df[target].min())
            xmax = min(df_train[target].max(), df[target].max())
            plt.axvspan(xmin=xmin, xmax=xmax, color='gray', alpha=0.1, label='training zone')


def plot_model_scores(y_true, y_score, bins=25, title='', show=True, as_xpptx=None):
    """
    Useful of comparing model scores for the different targets
    """

    df = pd.DataFrame({'Target': y_true, 'Model Score': y_score})
    sns.histplot(data=df, x='Model Score', hue='Target', element="step", common_norm=False, stat='percent', bins=bins)

    title2 = 'Histogram of model scores'
    if title:
        title2 = f"{title}: {title2}"

    post_plot(title=title2, legend=False, show=show, as_xpptx=as_xpptx)


def plot_model_accuracy_binned(df, title=''):
    df = df.copy()
    df['correct'] = df.pred == df.target
    df['bin'] = df.prob_1.apply(lambda p: float(str(p)[:3]))
    g = df.groupby('bin')
    df_bins = g.mean()['correct'].reset_index()
    plt.bar(df_bins['bin'], df_bins['correct'], align='edge', width=0.08)

    title2 = 'Model accuracy by score (binned)'
    if title:
        title2 = f"{title}: {title2}"

    plt.title(title2)

    plt.tight_layout()
    plt.show()

def plot_score_comparison(scores: dict, key_label='Dataset', score_label='Model Score', bins=25, title=''):
    """
    Useful for comparing the scores of various datasets:
    > plot_score_comparison({'train': train_scores, 'test': test_scores, 'blind': blind_scores)
    """

    rows = []
    for k, scores in scores.items():
        for score in scores:
            rows.append({key_label: k, score_label: score})

    df = pd.DataFrame(rows)
    sns.histplot(data=df, x=score_label, hue=key_label, element="step", common_norm=False, stat='percent', bins=bins)

    title2 = f'Histogram of model scores per {key_label}'
    if title:
        title2 = f"{title}: {title2}"

    plt.title(title2)
    plt.tight_layout()
    plt.show()


def plot_model_scores_ratios(y_true, y_score, bins=25, ratio_of=1):
    df = pd.DataFrame({'target': y_true, 'score': y_score})
    s_min = y_score.min()
    s_max = y_score.max()
    s_range = s_max - s_min
    borders = np.linspace(s_min, s_max+s_range*.0001, bins+1)

    rows = []
    for s_start, s_end in zip(borders[:-1], borders[1:]):
        s_mid = (s_start + s_end) / 2
        df_g = df[(df.score >= s_start) & (df.score < s_end)]
        if len(df_g) == 0:
            continue

        r = (df_g.target == ratio_of).sum() / len(df_g)
        rows.append({'s_start': df_g.score.min(), 's_end': df_g.score.max(), 'ratio': r})

    df_rows = pd.DataFrame(rows)

    for row in df_rows.itertuples():
        plt.plot([row.s_start, row.s_end], [row.ratio, row.ratio], color='black')

    plt.title('Histogram of model scores')
    plt.tight_layout()
    plt.show()


def plot_corr_heatmap(df, title='Correlation Heatmap', fontsize=12, pad=12, cmap='BrBG', figsize=(15,15), show=True):
    """
    Credits: https://medium.com/@szabo.bibor/how-to-create-a-seaborn-correlation-heatmap-in-python-834c0686b88e
    """

    df = df.copy()
    for col in df.columns:
        try:
            df[col] = df[col].astype(float)
        except ValueError:
            del df[col]

    df_corr = df.corr()
    plt.subplots(figsize=figsize)
    mask = np.triu(np.ones_like(df_corr, dtype=bool))

    hm = sns.heatmap(df_corr, vmin=-1, vmax=1, annot=True, cmap=cmap, mask=mask)
    hm.set_title(title, fontdict={'fontsize': fontsize}, pad=pad)
    plt.tight_layout()
    if show:
        plt.show()


def plot_funnel(vals, labels, figsize=(8,5), title='', pct_kind='abs'):
    # credits: https://www.dontusethiscode.com/blog/2023-03-29_matplotlib-funnel-chart.html
    s = pd.Series(
        data=vals,
        index=labels
    )

    fig, ax = subplots(figsize=figsize)

    sorted_s = s.sort_values()

    bc = ax.barh(
        sorted_s.index,
        sorted_s,
        left=(sorted_s.max() - sorted_s) / 2 - sorted_s.max() / 2, lw=0
    )

    bc_rev = list(reversed(bc))
    for prev, cur in zip(bc_rev[:-1], bc_rev[1:]):
        prev_x0, prev_y0, prev_x1, prev_y1 = prev.get_corners()[::2, :].flat
        cur_x0, cur_y0, cur_x1, cur_y1 = cur.get_corners()[::2, :].flat

        ax.fill_betweenx(
            [prev_y0, cur_y1],
            x1=[prev_x0, cur_x0],
            x2=[prev_x1, cur_x1],
            color=prev.get_facecolor(),
            alpha=.4,
            ec='face'
        )

    for rect, (name, value) in zip(bc, sorted_s.items()):
        ax.text(
            s=f'{name.title()}\n{value:,}',
            x=rect.get_x() + (rect.get_width() / 2),
            y=rect.get_y() + (rect.get_height() / 2),
            ha='center',
            va='center',
            color='xkcd:white',
            backgroundcolor='xkcd:dark blue'
        )

    def formatter():
        def _formatter(x, pos):
            label = f'{locs[pos]}\n'
            if pct_kind == 'abs':
                label = f'{label}{pcts.loc[locs[pos]] * 100:.0f}%'
            elif pct_kind == 'diff' and not np.isnan(pct_diffs.loc[locs[pos]]):
                label = f'{label}{pct_diffs.loc[locs[pos]] * 100:.0f}%'
            return label

        locs = [t.get_text() for t in ax.get_yticklabels()]
        pcts = s / s.max()
        pct_diffs = s / s.shift()
        return _formatter

    ax.yaxis.set_major_formatter(formatter())
    ax.margins(x=0, y=0)
    ax.spines[:].set_visible(False)
    ax.yaxis.set_tick_params(labelright=True, labelleft=False, left=False)
    ax.xaxis.set_tick_params(bottom=False, labelbottom=False)
    if title:
        ax.set_title(title, y=1.05)
    plt.tight_layout()
    plt.show()


def plot_pie(vals=None, counts=None, title='', sort_by_index=False, figsize=(6, 5), colors=None, show=True, with_numbers=True, specific_order=None, cmap=None):
    name = ''
    if vals is not None:
        vals = pd.Series(vals)
        counts = vals.value_counts()
        if hasattr(vals, 'name') and vals.name is not None:
            name = f"{vals.name}, "

    assert counts is not None, "either vals or counts must be provided"
    if sort_by_index:
        counts = counts.sort_index()
    else:
        counts = counts.sort_values(ascending=False)

    if specific_order is not None:
        so = [i for i in specific_order if i in counts]
        counts = counts[so]

    numbers = counts.values
    labels = counts.index.values
    actual_labels = labels
    if with_numbers:
        actual_labels = [f"{k} ({v})" for k, v in counts.items()]

    if colors:
        actual_colors = []
        for label in labels:
            actual_colors.append(mcolors.to_rgb(colors[label]))

    else:
        if cmap:
            color_idxs = np.linspace(0, 255, len(labels)).astype(int)
            mpl_cmap = matplotlib.colormaps[cmap]
            actual_colors = [mpl_cmap(idx) for idx in color_idxs]
        else:
            actual_colors = [xsettings.x_get_color(l) for l in labels]

    plt.figure(figsize=figsize)
    plt.pie(numbers, labels=actual_labels, autopct='%1.1f%%', shadow=False, startangle=0, colors=actual_colors)

    title2 = merge_titles(title, f"{name}total count={counts.sum()}")
    plt.title(title2)

    plt.tight_layout()
    if show:
        plt.show()

    return counts


def plot_counts(df, on, sort_by_counts=True, title=''):
    counts = df[on].value_counts()
    counts = counts.sort_values(ascending=False)
    plt.clf()
    title2 = merge_titles(title, f"Counts on {on}")
    plt.title(title2)
    x = np.arange(len(counts)) if sort_by_counts else counts.index.values
    plt.scatter(x, counts.values, s=2)
    plt.ylabel('counts')
    if sort_by_counts:
        plt.xlabel(f"{on} sorted by counts ({len(counts)} cases)")
        plt.tick_params(
            axis='x',  # changes apply to the x-axis
            which='both',  # both major and minor ticks are affected
            bottom=False,  # ticks along the bottom edge are off
            top=False,  # ticks along the top edge are off
            labelbottom=False)  # labels along the bottom edge are off

    else:
        plt.xlabel(f"{on}")

    plt.tight_layout()
    plt.show()
    return


def plot_bar_do(df, x_col, y_cols, total_width=0.6, colors=None, bar_label=None):
    if isinstance(y_cols, str):
        y_cols = [y_cols]

    ax = plt.gca()
    x = np.arange(len(df))
    n = len(y_cols)
    width = total_width / n
    for idx, y in enumerate(y_cols):
        start = total_width / 2 - width/2
        offset = idx * width

        actual_color = None
        if isinstance(colors, dict):
            actual_color = colors[y]
        elif isinstance(colors, list):
            actual_color = colors[idx]

        bars = ax.bar(x - start + offset, df[y], width, label=xsettings.x_get_desc(y), color=actual_color)

        if bar_label is not None:
            fmt = None
            if isinstance(bar_label, str) or callable(bar_label):
                fmt = bar_label

            ax.bar_label(bars, fmt=fmt)

    ax.set_xticks(x, df[x_col])


def big_scatter(df, x, y, colors='fire', title='', show=True, show_axis=True, figsize=(12, 12), plot_dim=(1000, 1000)):
    import datashader as ds
    import colorcet as cc

    fig, axes = plt.subplots(figsize=figsize)
    # a = ds.Canvas().points(df, 'x', 'y')
    # tf.shade(a)
    # plt.plot([-15, 15], [-15, 15], color='blue')
    # plt.show()

    cvs = ds.Canvas(plot_width=plot_dim[0], plot_height=plot_dim[1])
    agg = cvs.points(df, x, y)

    if colors == 'fire':
        img = ds.tf.set_background(ds.tf.shade(agg, cmap=cc.fire), "black")
    elif colors == 'bw':
        img = ds.tf.set_background(ds.tf.shade(agg, cmap=cc.b_cyclic_grey_15_85_c0_s25), "black")
    else:
        raise ValueError(colors)

    img2 = img.to_pil()
    plt.imshow(img2, extent=(img[x].min(), img[x].max(), img[y].min(), img[y].max()))

    if not show_axis:
        plt.axis('off')

    plt.tight_layout()

    if title:
        plt.title(title)

    if show:
        plt.show()


@contextmanager
def plot_wrapper(title='', legend=True, legend_loc='best', xlim=None, ylim=None, xlabel=None, ylabel=None, x_rotation=None, tight_layout=True, show=True, y_auc=False, x_axis_fmt=None, y_axis_fmt=None, add_date=False, desc='', as_xpptx=None, figsize=(7, 5)):
    fig, ax = pre_plot(figsize=figsize)
    yield fig, ax
    post_plot(title=title, legend=legend, legend_loc=legend_loc, xlim=xlim, ylim=ylim, xlabel=xlabel, ylabel=ylabel, x_rotation=x_rotation, tight_layout=tight_layout, show=show, y_auc=y_auc, x_axis_fmt=x_axis_fmt, y_axis_fmt=y_axis_fmt, add_date=add_date, desc=desc, as_xpptx=as_xpptx)


def pre_plot(figsize=(6, 5)):
    return plt.subplots(figsize=figsize)


def post_plot(title='', legend=True, legend_loc='best', xlim=None, ylim=None, xlabel=None, ylabel=None, x_rotation=None, tight_layout=True, show=True, y_auc=False, x_axis_fmt=None, y_axis_fmt=None, add_date=False, desc='', as_xpptx=None):
    """
    Helper function to set various plot attributes...
    """
    if as_xpptx and as_xpptx.fake:
        as_xpptx = None

    ax = plt.gca()

    if y_auc:
        ylim = [0, 1]

    if title:
        plt.title(title)

    if '\n' in title and not desc:
        title, desc = title.split('\n', maxsplit=1)

    if xlim:
        plt.xlim(xlim)

    if ylim:
        plt.ylim(ylim)

    if xlabel:
        plt.xlabel(xlabel)

    if ylabel:
        plt.ylabel(ylabel)

    if ylabel is False:
        ax.get_yaxis().set_visible(False)

    if xlabel is False:
        ax.get_xaxis().set_visible(False)

    if x_rotation:
        plt.xticks(rotation=x_rotation)

    if x_axis_fmt:
        if x_axis_fmt == int:
            plt.gca().xaxis.set_major_locator(mticker.MultipleLocator(1))

        else:
            ax.xaxis.set_major_formatter(x_axis_fmt)

    if y_axis_fmt:
        if y_axis_fmt == int:
            plt.gca().yaxis.set_major_locator(mticker.MultipleLocator(1))
        else:
            ax.yaxis.set_major_formatter(y_axis_fmt)

    if y_auc:
        plt.axhline(y=0.5, ls=':', color='red', alpha=0.75)
        plt.axhline(y=0.65, ls=':', color='xkcd:dark yellow', alpha=0.75)
        plt.axhline(y=0.35, ls=':', color='xkcd:dark yellow', alpha=0.75)
        plt.axhline(y=0.8, ls=':', color='xkcd:green', alpha=0.75)
        plt.axhline(y=0.2, ls=':', color='xkcd:green', alpha=0.75)

    if add_date:
        date_str = dt.date.today().isoformat()
        down_shift = -0.08
        if isinstance(add_date, int) or isinstance(add_date, float):
            down_shift *= add_date
        plt.annotate(date_str, xy=(0.9, down_shift), xycoords='axes fraction')

    if tight_layout:
        plt.tight_layout()

    if legend:
        plt.legend(loc=legend_loc)

    if as_xpptx:
        as_xpptx.add_slide('left_column', title=title, text=desc, text_2=as_xpptx.capture_image())

    elif show:
        plt.show()


def plot_multi(df, kind=None, plot_func=None, x=None, y=None, var_name='variable', value_name='value', plot_on=None, group_on=None, color_on=None, annotate_on=None, cmap=None, label_on=None, style_on=None, size_on=None, figsize=(10,6), alpha=1.0, hdi_probs=(0.1, 0.25, 0.5, 0.8, 0.999), kde_cov=0.25, kde_percentile=None, hist_calc='perc', hist_type='step', hist_bins=10, hist_range=None, color_dict=None, title='', x_axis_type=None, y_axis_type=None, x_axis_fmt=None, y_axis_fmt=None, invert_yaxis=False, legend_loc='best', xlim=None, ylim=None, save_to=None, clear_folder=False, add_date=True, add_counts=True, plot_decorate_func=None, drop_na=True, as_xpptx=None, desc='', reset_colors=True, show=True, **kwargs):
    """
    :param df: input dataframe
    :param kind: type of plot ('scatter', 'line', 'hdi', '%', 'kde', 'hist')
    :param plot_func: alternative to *kind*, can provide a custom function that takes a subset of data & plots
    :param x: name of column for x-axis
    :param y: name of column for y-axis (can be iterable)
    :param var_name: in case y is a list
    :param value_name: in case y is a list
    :param plot_on: column name that generates different plot for each unique value
    :param group_on: column name for different subgroup of data (usually not neaded if provide color_on, etc)
    :param color_on: column name for different colors
    :param cmap: (optional) name of colormap to use, eg 'plasma' or 'cool'
    :param label_on: column name for different labels
    :param style_on: column name for different styles
    :param figsize:
    :param alpha: transparency
    :param hdi_probs: used for kind == 'hdi'
    :param kde_cov: used for kind == 'kdi'
    :param hist_calc: 'perc', 'count'
    :param hist_bins: either number of bins, or a fraction of possible unique vals
    :param hist_range: optional, default <min, max> for plot
    :param color_dict:
    :param title:
    :param x_axis_type: can set to int
    :param y_axis_type: can be set to int
    :param legend_loc:
    :param xlim:
    :param ylim:
    :param save_to: instead of displaying, can save fig to file
    :param clear_folder:
    :param add_date: adds a date to fig
    :param plot_decorate_func: called once per entire plot
    :param drop_na: removes NA before plotting (prevents strange errors)
    :param show: whether to call plt.show() when finished
    :param kwargs: additional params that get passed to plot_func
    :return:
    """

    if reset_colors:
        xsettings.x_reset_colors()

    if as_xpptx and as_xpptx.fake:
        as_xpptx = None

    if kind is None and plot_func is None:
        kind = 'scatter'

    multi_y = False
    if isinstance(y, list) or isinstance(y, tuple):
        multi_y = True
        # id_vars = set()
        # for zz in [x, color_on, group_on, plot_on, label_on, size_on, style_on]:
        #     if zz is None:
        #         continue
        #
        #     if isinstance(zz, str):
        #         id_vars.add(zz)
        #     else:
        #         for i in zz:
        #             id_vars.add(i)
        #
        # id_vars = [i for i in id_vars if i]
        id_vars = list(set(df.columns) - set(y))
        df = pd.melt(df, id_vars=id_vars, value_vars=y, var_name=var_name, value_name=value_name)
        y = value_name
        if color_on is None:
            color_on = var_name
        elif style_on is None:
            style_on = var_name
        else:
            raise ValueError("if y is a list, then either color_on or style_on must be None")

    if kind in ['percentiles', 'percentile', 'percent', 'perc']:
        kind = '%'

    if x is None and y is None:
        raise TypeError('Missing required keyword argument: x or y')

    if save_to:
        save_to = path(save_to)
        save_to.ensure_dir()

        if clear_folder:
            save_to.rmtree()
            save_to.ensure_dir()

    if as_xpptx and plot_on:
        assert isinstance(as_xpptx, xpptx.Presentation), as_xpptx
        if title:
            as_xpptx.add_slide('section_header', title=title, subtitle=desc)

    def to_list(i):
        if not i:
            i = []

        if isinstance(i, str):
            i = [i]

        return i

    color_on = to_list(color_on)
    style_on = to_list(style_on)
    label_on = to_list(label_on)
    group_on = to_list(group_on)

    if not label_on:
        label_on = color_on + style_on

    if not color_on:
        color_on = label_on

    if label_on:
        label_on = sorted(set(label_on))
        df = df.sort_values(label_on)

    group_on = list(set(group_on + color_on + style_on + label_on))

    color_id = 0
    style_id = 0
    color_lookup = None
    style_lookup = dict()
    x_label_override = None
    y_label_override = None

    color_list = xsettings.COLOR_LIST
    if cmap and color_on:
        assert len(color_on) == 1, color_on
        color_vals = np.unique(df[color_on].to_numpy())
        color_vals = np.sort(color_vals)
        color_vals = [f"{color_on[0]}={v}" for v in color_vals]
        color_idxs = np.linspace(0, 255, len(color_vals)).astype(int)
        mpl_cmap = matplotlib.colormaps[cmap]
        color_rgbs = [mpl_cmap(idx) for idx in color_idxs]
        color_lookup = dict(zip(color_vals, color_rgbs))
        # raise NotImplementedError

    line_styles = [
     ('solid', 'solid'),      # Same as (0, ()) or '-'
     ('dotted', 'dotted'),    # Same as (0, (1, 1)) or ':'
     ('dashed', 'dashed'),    # Same as '--'
     ('dashdot', 'dashdot'),  # Same as '-.'
     ('loosely dashed',        (0, (5, 10))),
     ('densely dashed',        (0, (5, 1))),
     ('loosely dashdotted',    (0, (3, 10, 1, 10))),
     ('dashdotted',            (0, (3, 5, 1, 5))),
     ('densely dashdotted',    (0, (3, 1, 1, 1))),
     ('dashdotdotted',         (0, (3, 5, 1, 5, 1, 5))),
     ('loosely dashdotdotted', (0, (3, 10, 1, 10, 1, 10)))]
    line_styles = [ls[1] for ls in line_styles]
    scatter_markers = list(".v1sPp*+xd|_")
    style_param = "ls" if kind in ['line', 'kde'] else 'marker'
    style_list = line_styles if style_param == 'ls' else scatter_markers

    for df_p, keys, plot_title in xpd.x_iter_groups(df, plot_on):
        labels = set()
        plt.clf()
        did_plot = False

        label_counts = None
        if label_on:
            if kind in ['scatter', 'kde', 'hist']:
                label_counts = df_p.value_counts(label_on).reset_index(name='_count')
            elif kind in ['line'] and group_on:
                if multi_y:
                    label_counts = df_p.value_counts(label_on).reset_index(name='_count')
                else:
                    label_counts = df_p.drop_duplicates(group_on).value_counts(label_on).reset_index(name='_count')

        fig, ax = plt.subplots(figsize=figsize)

        hist_range_p = hist_bins_p = None
        if kind == 'hist':
            hist_range_p = hist_range
            if hist_range_p is None:
                hist_range_p = [df_p[y].min(), df_p[y].max()]
                if np.issubdtype(df_p[y].iloc[0], np.integer):
                    hist_range_p[0] -= 1

            if hist_range_p[0] is None:
                hist_range_p[0] = df_p[y].min()

            if hist_range_p[1] is None:
                hist_range_p[1] = df_p[y].max()

            hist_bins_p = hist_bins
            if isinstance(hist_bins_p, float):
                assert np.issubdtype(df_p[y].iloc[0], np.integer), df_p[y].dtype
                hist_bins_p = int((hist_range_p[1] - hist_range_p[0] + 1)*hist_bins_p)

        for df_g, _, group_title in xpd.x_iter_groups(df_p, group_on):
            color = None
            label = None
            style = None

            if drop_na:
                df_g = df_g.dropna(subset=[y]).copy()

            if not len(df_g):
                continue

            did_plot = True

            if label_on:
                sa_label = df_g.iloc[0][label_on]
                label = ", ".join([f"{k}={v}" for k,v in sa_label.items()])
                if add_counts and label_counts is not None:
                    count = xpd.x_filter_by_keys(label_counts, sa_label)['_count'].iloc[0]
                    label = f"{label} ({count})"

            if label in labels:
                label = None

            labels.add(label)

            if color_on:
                sa_color_val = df_g.iloc[0][color_on]
                color_val = ", ".join([f"{k}={v}" for k, v in sa_color_val.items()])
                if color_lookup:
                    color = color_lookup[color_val]
                else:
                    color = xsettings.x_get_color(color_val)

            if style_on:
                sa_style_val = df_g.iloc[0][style_on]
                style_val = ", ".join([f"{k}={v}" for k, v in sa_style_val.items()])
                if style_val not in style_lookup:
                    style_lookup[style_val] = style_list[style_id]
                    style_id += 1

                style = style_lookup[style_val]

            params = dict()
            if color is not None:
                params['color'] = color

            if style is not None:
                params[style_param] = style

            if label is not None:
                params['label'] = label

            if alpha is not None:
                params['alpha'] = alpha

            params.update(kwargs)

            if plot_func:
                params2 = params.copy()
                if kind is not None:
                    if 'label' in params2:
                        del params2['label']

                for k in kwargs:
                    del params2[k]

                plot_func(plt, df_g, **params2)

            if kind in ['scatter', 'reg']:
                _x = df_g[x]
                _y = df_g[y]
                params['s'] = params.get('s', 2)

                if kind == 'reg':
                    X = _x.to_numpy().reshape(-1, 1)
                    reg = linear_model.LinearRegression()
                    reg.fit(X, _y)
                    _y_pred = reg.predict(X)
                    st = xstats.x_model_pred_stats(_y, _y_pred, is_classification=False)
                    text = f"R2={st.r2:.3f} Corr={st.corr:.3f} MAE={st.mae:.3f}"
                    x_min = _x.iloc[_x.argmin()]
                    x_max = _x.iloc[_x.argmax()]
                    y_min = _y_pred[_x.argmin()]
                    y_max = _y_pred[_x.argmax()]

                    if 'label' in params:
                        params['label'] = f"{params['label']} ({text})"
                    else:
                        plt.text(.01, .99, text, ha='left', va='top', transform=ax.transAxes)

                    if color:
                        fact = 0.5
                        reg_color = to_rgba(color)
                        reg_color = (reg_color[0]*fact, reg_color[1]*fact, reg_color[2]*fact, reg_color[3])
                    else:
                        reg_color = 'black'

                    plt.plot([x_min, x_max], [y_min, y_max], ls=':', color=reg_color)

                if size_on:
                    min_s = params.get('s', 2)
                    sizes = df_g[size_on]
                    min_size = sizes.min()
                    max_size = sizes.max()
                    size_diff = max_size - min_size
                    size_ratio = 1
                    if size_diff > 0:
                        size_ratio = 10 / size_diff

                    sizes = (sizes - min_size) * size_ratio + min_s
                    params['s'] = sizes

                plt.scatter(x=_x, y=_y, **params)

                if annotate_on:
                    _txt = [str(i) for i in df_g[annotate_on]]
                    for __txt, __x, __y in zip(_txt, _x, _y):
                        ax.annotate(__txt, (__x, __y))

            elif kind == 'line':
                if len(df_g) == 1:
                    params['marker'] = 'x'

                df_g = df_g.sort_values([x, y])
                plt.plot(df_g[x], df_g[y], **params)

            elif kind == 'hdi':
                hdi_probs = sorted(hdi_probs)
                alpha_step = alpha / len(hdi_probs)
                g_hdi = df_g.groupby(x)
                for hdi_prob in hdi_probs:
                    try:
                        df_hdi = g_hdi.apply(lambda dfx: pd.Series(az.hdi(dfx[y].to_numpy(), hdi_prob=hdi_prob), index=['low', 'high']))
                    except ValueError:
                        raise
                    df_hdi = df_hdi.reset_index()
                    params['label'] = label
                    params['alpha'] = alpha_step
                    if 'color' not in params:
                        params['color'] = 'blue'

                    plt.fill_between(df_hdi[x], df_hdi['low'], df_hdi['high'], linewidth=0, **params)
                    label = None

                df_mode = g_hdi.apply(lambda dfx: pd.Series(az.hdi(dfx[y].to_numpy(), hdi_prob=0.05), index=['low', 'high'])).mean(axis=1)
                plt.plot(df_mode.index.values, df_mode.to_numpy(), ls='--', color=color)
                # df_means = g_hdi[y].median().reset_index(name='_mean_val')
                # plt.plot(df_means[x], df_mode.to_numpy(), ls='--', color=color)

            elif kind == '%':
                hdi_probs = sorted(hdi_probs)
                alpha_step = alpha / len(hdi_probs)

                g_hdi = df_g.groupby(x)

                for hdi_prob in hdi_probs:
                    perc_low = 0.5 - hdi_prob / 2
                    perc_high = 0.5 + hdi_prob / 2

                    sa_low = g_hdi.apply(lambda dfx: np.percentile(dfx[y].to_numpy(), 100 * perc_low))
                    sa_high = g_hdi.apply(lambda dfx: np.percentile(dfx[y].to_numpy(), 100 * perc_high))

                    params['label'] = label
                    params['alpha'] = alpha_step
                    if 'color' not in params:
                        params['color'] = 'blue'

                    plt.fill_between(sa_low.index.values, sa_low, sa_high, linewidth=0, **params)
                    label = None

                df_means = g_hdi[y].median().reset_index(name='_mean_val')
                plt.plot(df_means[x], df_means['_mean_val'], ls='--', alpha=0.7, color=color)

            elif kind == 'kde':
                # credit: https://stackoverflow.com/questions/4150171/how-to-create-a-density-plot-in-matplotlib
                _y = df_g[y].astype(float)
                if kde_percentile:
                    _y_min = np.percentile(_y, 100 * (0.5 - kde_percentile / 2))
                    _y_max = np.percentile(_y, 100 * (0.5 + kde_percentile / 2))
                    _y = _y[(_y_min <= _y) & (_y <= _y_max)]

                density = stats.gaussian_kde(_y)
                xs = np.linspace(_y.min(), _y.max(), 200)
                density.covariance_factor = lambda: kde_cov
                density._compute_covariance()
                plt.plot(xs, density(xs), **params)
                y_label_override = 'density'
                x_label_override = xsettings.x_get_desc(y)
                if ylim is None:
                    ylim = [0, None]

            elif kind == 'hist':
                _y = df_g[y].astype(float)
                counts, bins = np.histogram(_y, bins=hist_bins_p, range=hist_range_p)
                if hist_calc == 'perc':
                    counts = counts / counts.sum()
                    y_label_override = 'Percent'
                    y_axis_fmt = FORMATTER_PERC
                else:
                    y_label_override = 'Count'

                plt.hist(bins[:-1], bins, weights=counts, histtype=hist_type, **params)

                x_label_override = xsettings.x_get_desc(y)

            elif not plot_func:
                raise ValueError(kind)

        if title and plot_title:
            if title.endswith('\n'):
                plot_title = f"{title}{plot_title}"
            else:
                plot_title = f"{title}: {plot_title}"

        elif title:
            plot_title = title

        if not did_plot:
            continue

        if plot_decorate_func is not None:
            plot_decorate_func(plt, df_p)

        if plot_title:
            plt.title(plot_title)

        if labels and legend_loc != 'off':
            plt.legend(loc=legend_loc)

        if x_axis_type == int:
            plt.gca().xaxis.set_major_locator(mticker.MultipleLocator(1))

        if y_axis_type == int:
            plt.gca().yaxis.set_major_locator(mticker.MultipleLocator(1))

        if x_axis_fmt:
            if x_axis_fmt == int:
                plt.gca().xaxis.set_major_locator(mticker.MultipleLocator(1))

            else:
                ax.xaxis.set_major_formatter(x_axis_fmt)

        if y_axis_fmt:
            if y_axis_fmt == int:
                plt.gca().yaxis.set_major_locator(mticker.MultipleLocator(1))
            else:
                ax.yaxis.set_major_formatter(y_axis_fmt)

        if invert_yaxis:
            plt.gca().invert_yaxis()

        if xlim:
            plt.xlim(xlim)

        if ylim:
            plt.ylim(ylim)

        if x_label_override:
            plt.xlabel(x_label_override)
        elif x:
            plt.xlabel(xsettings.x_get_desc(x))

        if y_label_override:
            plt.ylabel(y_label_override)
        elif y:
            plt.ylabel(xsettings.x_get_desc(y))

        if add_date:
            date_str = dt.date.today().isoformat()
            ax.annotate(date_str, xy=(0.9, -0.08), xycoords='axes fraction')

        plt.tight_layout()

        if save_to:
            plot_title = plot_title or "all"
            plt.savefig(save_to.joinpath(f"{plot_title}.png"), pad_inches=0)

        elif as_xpptx:
            if plot_on:
                text = "\n".join([f"{k}={v}" for k,v in keys.items()])
                slide_title = ''
            else:
                slide_title = title
                text = desc

            as_xpptx.add_slide('left_column', title=slide_title, text=text, text_2=as_xpptx.capture_image())

        elif show:
            plt.show()
