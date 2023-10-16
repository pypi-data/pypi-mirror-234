import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import seaborn as sns
import numpy as np


# ==================================================
def init_plot(fig_size=None, font_scale=None):
    """
    initialize matplot.

    Args:
        fig_size (tuple): size of figure, None=(10,8).
        font_scale (float): font scale, None=1.1

    Returns: tuple.
        - pyplot: matplot.pyplot.
        - figure: matplot.pyplot.figure.
    """
    if fig_size is None:
        fig_size = (10, 8)
    if font_scale is None:
        font_scale = 1.4

    sns.set("notebook", "whitegrid", "dark", font_scale=font_scale, rc={"lines.linewidth": 1, "grid.linestyle": "--"})
    figure = plt.figure(figsize=fig_size)

    return plt, figure


# ==================================================
def plot_colormap_line(x, y, c=1.0, cmap="coolwarm", c_range=(-1, 1), width=2.0, opacity=1.0, ax=None):
    """
    plot lines with colormap.

    Args:
        x (list or ndarray): x points.
        y (list or ndarray): (a set of) y points in each column.
        c (float or list or ndarray, optional): (a set of) values for colormap in each column.
        cmap (str, optional): colormap.
        c_range (tuple, optional): range of colormap value.
        width (float, optional): line width.
        opacity (float, optional): opacity.
        ax (Axes, optional): plt axes.

    Returns:
        list: list of LineCollection.
    """
    x = np.array(x)
    c = np.array(c, ndmin=2)
    y = np.array(y, ndmin=2)

    if y.shape[0] == 1:
        y = y.T
    if c.shape[0] == 1:
        c = c.T
    if c.shape != y.shape:
        c = np.full(y.shape, c)

    lc = []
    for i in range(y.shape[1]):
        points = np.array([x, y[:, i]]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)

        lc0 = LineCollection(segments, array=c[:, i], cmap=cmap, linewidth=width, alpha=opacity, norm=plt.Normalize(*c_range))

        if ax is None:
            ax = plt.gca()
        ax.add_collection(lc0)
        lc.append(lc0)

    return lc


# ==================================================
def plot_dispersion(
    k_linear,
    Ek,
    k_name=None,
    phonon=False,
    color="forestgreen",
    width=1.3,
    E_range=None,
    weight=None,
    w_range=None,
    title=None,
    xlabel=None,
    ylabel=None,
    ax=None,
):
    """
    plot dispersion.

    Args:
        k_linear (list): k-linear point.
        Ek (ndarray): eigenvalues, [k_index, eigenstate_index].
        k_name (dict, optional): {position: k point name}.
        phonon (bool, optional): phonon ?
        color (str, optional): color, if colormap name is given, plot with weight and colormap.
        width (float, optional): line width.
        E_range (tuple, optional): enery range.
        weight (ndarray): weight of dispersion, [k_index, eigenstate_index].
        w_range (tuple, optional): weight range.
        title (str, optional): plot title.
        xlabel (str, optional): x label.
        ylabel (str, optional): y label.
        ax (Axes, optional): plt Axes.

    Returns:
        list: list of LineCollection.

    Notes:
        - k-point name, "G" and "Γ" (\u0393) are replaced by "$\Gamma$".
    """
    if k_name is None:
        k_name = {}
    if ylabel is None:
        ylabel = r"$\omega_n(k)$" if phonon else r"$E_n(k)$"
    if title is None:
        title = "dispersion relation"
    if E_range is None:
        E_range = (0.0, Ek.max() + 0.1) if phonon else (Ek.min() - 0.1, Ek.max() + 0.1)
    if w_range is None:
        w_range = (-1, 1)

    k_label = [i.replace("G", r"$\Gamma$").replace("\u0393", r"$\Gamma$") for i in k_name.values()]

    ax.title.set_fontsize(18)
    if xlabel is None:
        ax.set(title=title, xlabel="", ylabel=ylabel)
    else:
        ax.set(title=title, xlabel=xlabel, ylabel=ylabel)

    if len(k_name) > 0:
        ax.set_xticks(list(k_name.keys()))
        ax.set_xticklabels(k_label)
        for i in k_name.keys():
            ax.plot([i, i], E_range, color="gray", linewidth=0.7)
    else:
        ax.grid(which="major", axis="x", color="gray", linewidth=0.7)
    ax.grid(which="major", axis="y", color="gray", linewidth=0.7)

    ax.set_xlim(k_linear[0], k_linear[-1])
    ax.set_ylim(*E_range)

    if color in mpl.colors.cnames.keys() or weight is None:
        cl = ax.plot(k_linear, Ek, color=color, lw=width)
    else:
        cl = plot_colormap_line(k_linear, Ek, weight, c_range=w_range, cmap=color, width=width, ax=ax)

    return cl
