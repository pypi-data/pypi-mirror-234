""" plotting Module """

import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.api as sm


class Plot:

    def __init__(self):
        self.axes = None

    def shape(self, dim=(10, 5)):
        plt.figure(figsize=dim)
        return self

    def grid(self, c="#EAEAF1"):
        # grid color
        self.axes.set_facecolor(c)
        # grid lines
        self.axes.grid(True, linestyle='-', color='white', linewidth=0.5, alpha=0.5, zorder=1)
        return self

    def label(self, xlabel, ylabel, tlabel):
        self.axes.set_ylabel(ylabel, fontsize=10)
        self.axes.set_xlabel(xlabel, fontsize=10)
        self.axes.set_title(tlabel, pad=10)
        return self

    def spine(self, top=False, right=False, bottom=False, left=False):
        self.axes.spines['top'].set_visible(top)
        self.axes.spines['right'].set_visible(right)
        self.axes.spines['bottom'].set_visible(bottom)
        self.axes.spines['left'].set_visible(left)
        return self

    def tick(self, left=False, bottom=False, labelleft=False, labelbottom=False):
        self.axes.tick_params(labelcolor='black', labelsize='small', width=0.5, labelleft=labelleft,
                              labelbottom=labelbottom, left=left, bottom=bottom)
        return self

    def legend(self):
        self.axes.legend(bbox_to_anchor=(1.05, 1), loc="upper left", prop={"family": "Arial", "size": 12})
        return self

    def bar_label(self, fmt='%.0f', pad=1, fs=10):
        for c in self.axes.containers:
            self.axes.bar_label(c, fmt=fmt, padding=pad, color='black',
                                fontweight=None, fontstyle='italic', family=['monospace'], fontsize=fs)
        return self

    def set_axes(self, ax):
        self.axes = ax

    def render(self):
        plt.show()


class Barplot(Plot):

    def create(self, x, y, data, hue=None, width=0.8, c="#69b3a2", ax=None):
        self.axes = sns.barplot(x=x, y=y, hue=hue, data=data, width=width,
                                estimator="sum", errorbar=None, color=c, ax=ax, zorder=2)
        return self

    # def bar_label(self, fmt='%.0f', pad=1, fs=10):
    #     for c in self.axes.containers:
    #         self.axes.bar_label(c, fmt=fmt, padding=pad, color='black',
    #                             fontweight=None, fontstyle='italic', family=['monospace'], fontsize=fs)
    #     return self


class Lineplot(Plot):

    def create(self, x, y, data):
        self.axes = sns.lineplot(data=data, x=x, y=y, marker='.', markersize=15)
        return self

    def limit(self, y_start, y_end):
        self.axes.set_ylim(y_start, y_end)
        return self

    def fill(self, x, y):
        self.axes.fill_between(x, y, alpha=0.7, zorder=2)
        return self


class Mapplot(Plot):

    def create(self, ct, data, x, y, c, ct_name, ax=None):
        self.axes = ax
        self.country_shape_plot(ct)
        self.data_plot(data, x, y, c)
        self.country_name_plot(ct, ct_name)
        return self

    def country_shape_plot(self, ct):
        ct.plot(ax=self.axes, facecolor="white", edgecolor="k", alpha=1, linewidth=1, zorder=2)

    def data_plot(self, data, x, y, c):
        data.plot(x=x, y=y, kind="scatter", c=c, colormap="Set2", ax=self.axes, zorder=2)

    def country_name_plot(self, ct, ct_name):
        for a, b, label in zip(
                ct.geometry.centroid.x, ct.geometry.centroid.y, ct[ct_name]
        ):
            plt.text(a, b, label, fontsize=8, ha="center")


class Kdeplot(Plot):

    def create(self, data, x, hue, ax=None):
        self.axes = sns.kdeplot(data=data, x=x, hue=hue, multiple="stack", ax=ax, zorder=2)
        return self


class Histplot(Plot):

    def create(self, data, x, hue, ax=None, binwidth=3, kde=False):
        self.axes = sns.histplot(data=data, x=x, hue=hue,
                                 binwidth=binwidth, stat="count", palette="Set2", ax=ax, zorder=2, kde=kde)
        return self


class Boxplot(Plot):

    def create(self, data, x, y):
        self.axes = sns.boxplot(x=x, y=y, data=data, zorder=2)
        return self


class QQplot(Plot):

    def create(self, col, ax=None):
        # without gca() it returns a fig has the need for gca()
        self.axes = sm.qqplot(col, line='s', ax=ax).gca()
        return self


class Countplot(Plot):

    def create(self, data, x):
        self.axes = sns.countplot(data, x=x, zorder=2)
        return self
