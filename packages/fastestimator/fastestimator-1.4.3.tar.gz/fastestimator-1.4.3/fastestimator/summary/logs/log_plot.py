# Copyright 2019 The FastEstimator Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
import math
import os
import re
from collections import defaultdict
from typing import Any, Dict, List, Optional, Set, Union

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.markers import MarkerStyle
from matplotlib.ticker import EngFormatter
from natsort import humansorted
from scipy.ndimage.filters import gaussian_filter1d

from fastestimator.summary.summary import Summary, ValWithError
from fastestimator.util.util import prettify_metric_name, to_list, to_set


class _MetricGroup:
    """A class for wrapping the values recorded for a given metric based on its experiment id and mode.

    This class is intentionally not @traceable.
    """
    state: Dict[int, Dict[str, Dict[str, np.ndarray]]]

    def __init__(self):
        self.state = defaultdict(lambda: defaultdict(dict))  # exp_id: {mode: {ds_id: value}}

    def __getitem__(self, exp_id: int) -> Dict[str, Dict[str, np.ndarray]]:
        return self.state[exp_id]

    def add(self, exp_id: int, mode: str, ds_id: str, values: Dict[int, Any]) -> bool:
        """Add a new set of values to the metric group.

        Args:
            exp_id: The experiment id associated with these `values`.
            mode: The mode associated with these `values`.
            ds_id: The ds_id associated with these values (or empty string for None).
            values: A dictionary of time: value pairs.

        Returns:
            Whether the add was successful.
        """
        if values:
            values = list(sorted(values.items()))
            if len(values) == 1:
                # We will allow any data types if there's only one value since it will be displayed differently
                self.state[exp_id][mode][ds_id] = np.array(
                    values, dtype=None if isinstance(values[0][1], (int, float)) else object)
                return True
            else:
                # We will be plotting something over time
                val_is_object = False
                for idx, (step, elem) in enumerate(values):
                    if isinstance(elem, np.ndarray):
                        if elem.ndim == 0 or (elem.ndim == 1 and elem.shape[0] == 1):
                            elem = elem.item()
                        else:
                            # TODO - handle larger arrays somehow (maybe a heat map?)
                            return False
                    if isinstance(elem, str):
                        # Can't plot strings over time...
                        elem = [float(s) for s in re.findall(r'(\d+\.\d+|\.?\d+)', elem)]
                        if len(elem) == 1:
                            # We got an unambiguous number
                            elem = elem[0]
                        else:
                            # Can't disambiguate what should be plotted
                            return False
                    if not isinstance(elem, (int, float, ValWithError)):
                        # Can only plot numeric values over time
                        return False
                    values[idx] = (step, elem)
                    if isinstance(elem, ValWithError):
                        val_is_object = True
                if val_is_object:
                    # If some points are ValWithError, then they all need to be
                    for idx, (step, elem) in enumerate(values):
                        if isinstance(elem, (int, float)):
                            values[idx] = (step, ValWithError(elem, elem, elem))
                self.state[exp_id][mode][ds_id] = np.array(values, dtype=object if val_is_object else None)

    def ndim(self) -> int:
        """Compute how many dimensions this data require to plot.

        Returns:
            The number of dimensions this data requires to plot.
        """
        ndims = [0]
        for mode_ds_val in self.state.values():
            for _, ds_val in mode_ds_val.items():
                for _, values in ds_val.items():
                    if values.ndim in (0, 1):
                        # A singular value (this should never happen based on implementation of summary)
                        ndims.append(1)
                    elif values.ndim == 2:
                        if values.shape[0] == 1:
                            # Metrics with only 1 time point can be displayed as singular values
                            if isinstance(values[0][1], ValWithError):
                                # ValWithError, however, will always be displayed grapically
                                ndims.append(2)
                            else:
                                ndims.append(1)
                        else:
                            # A regular time vs metric value plot
                            ndims.append(2)
                    else:
                        # Time vs array value. Not supported yet.
                        ndims.append(3)
        return max(ndims)

    def get_val(self, exp_idx: int, mode: str, ds_id: str) -> Union[None, str, np.ndarray]:
        """Get the value for a given experiment id and mode.

        Args:
            exp_idx: The id of the experiment in question.
            mode: The mode under consideration.
            ds_id: The dataset id associated with this value.

        Returns:
            The value associated with the `exp_id` and `mode`, or None if no such value exists. If only a single item
            exists and it is numeric then it will be returned as a string truncated to 5 decimal places.
        """
        vals = self.state[exp_idx].get(mode, {}).get(ds_id, None)
        if vals is None:
            return vals
        if vals.ndim in (0, 1):
            item = vals.item()
            if isinstance(item, float):
                return "{:.5f}".format(item)
            return str(item)
        if vals.ndim == 2 and vals.shape[0] == 1:
            # This value isn't really time dependent
            item = vals[0][1]
            if isinstance(item, float):
                return "{:.5f}".format(item)
            return str(item)
        else:
            return vals

    def modes(self, exp_id: int) -> List[str]:
        """Get the modes supported by this group for a given experiment.

        Args:
            exp_id: The id of the experiment in question.

        Returns:
            Which modes have data for the given `exp_id`.
        """
        return list(self.state[exp_id].keys())

    def ds_ids(self, exp_id: int, mode: Optional[str] = None) -> List[str]:
        """Get the dataset ids supported by this group for a given experiment.

        If mode is provided, then only the ds_ids present for the particular mode will be returned.

        Args:
            exp_id: The id of the experiment in question.
            mode: The mode for which to consider ids, or None to consider over all modes.

        Returns:
            Which dataset ids have data for the given `exp_id` and `mode`.
        """
        if mode is None:
            mode = self.modes(exp_id)
        mode = to_list(mode)
        return [ds for md, dsv in self.state[exp_id].items() if md in mode for ds in dsv.keys()]


def plot_logs(experiments: List[Summary],
              smooth_factor: float = 0,
              share_legend: bool = True,
              ignore_metrics: Optional[Set[str]] = None,
              pretty_names: bool = False,
              include_metrics: Optional[Set[str]] = None) -> plt.Figure:
    """A function which will plot experiment histories for comparison viewing / analysis.

    Args:
        experiments: Experiment(s) to plot.
        smooth_factor: A non-negative float representing the magnitude of gaussian smoothing to apply (zero for none).
        share_legend: Whether to have one legend across all graphs (True) or one legend per graph (False).
        pretty_names: Whether to modify the metric names in graph titles (True) or leave them alone (False).
        ignore_metrics: Any keys to ignore during plotting.
        include_metrics: A whitelist of keys to include during plotting. If None then all will be included.

    Returns:
        The handle of the pyplot figure.
    """
    # Sort to keep same colors between multiple runs of visualization
    experiments = humansorted(to_list(experiments), lambda exp: exp.name)
    n_experiments = len(experiments)
    if n_experiments == 0:
        return plt.subplots(111)[0]

    ignore_keys = ignore_metrics or set()
    ignore_keys = to_set(ignore_keys)
    ignore_keys |= {'epoch'}
    include_keys = to_set(include_metrics)
    # TODO: epoch should be indicated on the axis (top x axis?). Problem - different epochs per experiment.
    # TODO: figure out how ignore_metrics should interact with mode
    # TODO: when ds_id switches during training, prevent old id from connecting with new one (break every epoch?)
    ds_ids = set()
    metric_histories = defaultdict(_MetricGroup)  # metric: MetricGroup
    for idx, experiment in enumerate(experiments):
        history = experiment.history
        # Since python dicts remember insertion order, sort the history so that train mode is always plotted on bottom
        for mode, metrics in sorted(history.items(),
                                    key=lambda x: 0 if x[0] == 'train' else 1 if x[0] == 'eval' else 2 if x[0] == 'test'
                                    else 3 if x[0] == 'infer' else 4):
            for metric, step_val in metrics.items():
                base_metric, ds_id, *_ = f'{metric}|'.split('|')  # Plot acc|ds1 and acc|ds2 on same acc graph
                if len(step_val) == 0:
                    continue  # Ignore empty metrics
                if metric in ignore_keys or base_metric in ignore_keys:
                    continue
                # Here we intentionally check against metric and not base_metric. If user wants to display per-ds they
                #  can specify that in their include list: --include mcc 'mcc|usps'
                if include_keys and metric not in include_keys:
                    continue
                metric_histories[base_metric].add(idx, mode, ds_id, step_val)
                ds_ids.add(ds_id)

    metric_list = list(sorted(metric_histories.keys()))
    if len(metric_list) == 0:
        return plt.subplots(111)[0]
    ds_ids = humansorted(ds_ids)  # Sort them to have consistent ordering (and thus symbols) between plot runs
    n_ds_ids = len(ds_ids)  # Each ds_id will have its own set of legend entries, so need to count them

    # If sharing legend and there is more than 1 plot, then dedicate subplot(s) for the legend
    share_legend = share_legend and (len(metric_list) > 1)
    n_legends = math.ceil(n_experiments * n_ds_ids / 4)
    n_plots = len(metric_list) + (share_legend * n_legends)

    # map the metrics into an n x n grid, then remove any extra columns. Final grid will be n x m with m <= n
    n_rows = math.ceil(math.sqrt(n_plots))
    n_cols = math.ceil(n_plots / n_rows)
    metric_grid_location = {}
    nd1_metrics = []
    idx = 0
    for metric in metric_list:
        if metric_histories[metric].ndim() == 1:
            # Delay placement of the 1D plots until the end
            nd1_metrics.append(metric)
        else:
            metric_grid_location[metric] = (idx // n_cols, idx % n_cols)
            idx += 1
    for metric in nd1_metrics:
        metric_grid_location[metric] = (idx // n_cols, idx % n_cols)
        idx += 1

    sns.set_context('paper')
    fig, axs = plt.subplots(n_rows, n_cols, sharex='all', figsize=(4 * n_cols, 2.8 * n_rows))

    # If only one row, need to re-format the axs object for consistency. Likewise for columns
    if n_rows == 1:
        axs = [axs]
    if n_cols == 1:
        axs = [[ax] for ax in axs]

    for metric in metric_grid_location.keys():
        axis = axs[metric_grid_location[metric][0]][metric_grid_location[metric][1]]
        if metric_histories[metric].ndim() == 1:
            axis.grid(linestyle='')
        else:
            axis.grid(linestyle='--')
            axis.ticklabel_format(axis='y', style='sci', scilimits=(-2, 3))
        axis.set_title(metric if not pretty_names else prettify_metric_name(metric), fontweight='bold')
        axis.spines['top'].set_visible(False)
        axis.spines['right'].set_visible(False)
        axis.spines['bottom'].set_visible(False)
        axis.spines['left'].set_visible(False)
        axis.tick_params(bottom=False, left=False)
        axis.xaxis.set_major_formatter(EngFormatter(sep=""))  # Convert 10000 steps to 10k steps

    # some of the later rows/columns might be unused or reserved for legends, so disable them
    last_row_idx = math.ceil(len(metric_list) / n_cols) - 1
    last_column_idx = len(metric_list) - last_row_idx * n_cols - 1
    for c in range(n_cols):
        if c <= last_column_idx:
            axs[last_row_idx][c].set_xlabel('Steps')
            axs[last_row_idx][c].xaxis.set_tick_params(which='both', labelbottom=True)
        else:
            axs[last_row_idx][c].axis('off')
            axs[last_row_idx - 1][c].set_xlabel('Steps')
            axs[last_row_idx - 1][c].xaxis.set_tick_params(which='both', labelbottom=True)
        for r in range(last_row_idx + 1, n_rows):
            axs[r][c].axis('off')

    # the 1D metrics don't need x axis, so move them up, starting with the last in case multiple rows of them
    for metric in reversed(nd1_metrics):
        row = metric_grid_location[metric][0]
        col = metric_grid_location[metric][1]
        axs[row][col].axis('off')
        if row > 0:
            axs[row - 1][col].set_xlabel('Steps')
            axs[row - 1][col].xaxis.set_tick_params(which='both', labelbottom=True)

    colors = sns.hls_palette(n_colors=n_experiments, s=0.95) if n_experiments > 10 else sns.color_palette("colorblind")
    color_offset = defaultdict(lambda: 0)
    # If there is only 1 experiment, we will use alternate colors based on mode
    if n_experiments == 1:
        color_offset['eval'] = 1
        color_offset['test'] = 2
        color_offset['infer'] = 3

    handles = []
    labels = []
    # exp_id : {mode: {ds_id: {type: True}}}
    has_label = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: False))))
    ax_text = defaultdict(lambda: (0.0, 0.9))  # Where to put the text on a given axis
    # Set up ds_id markers. The empty ds_id will have no extra marker. After that there are 4 configurations of 3-arm
    # marker, followed by asterisks with growing numbers of arms (starting at 4).
    ds_id_markers = ['', "1", "2", "3", "4"] + [(ticks, 2, 0) for ticks in range(4, n_ds_ids - 1)]
    ds_id_markers = {k: v for k, v in zip(ds_ids, ds_id_markers)}
    # Actually do the plotting
    for exp_idx, experiment in enumerate(experiments):
        for metric, group in metric_histories.items():
            axis = axs[metric_grid_location[metric][0]][metric_grid_location[metric][1]]
            if group.ndim() == 1:
                # Single value
                for mode in group.modes(exp_idx):
                    for ds_id in group.ds_ids(exp_idx, mode):
                        ds_title = f"{ds_id} " if ds_id else ''
                        ax_id = id(axis)
                        prefix = f"{experiment.name} ({ds_title}{mode})" if n_experiments > 1 else f"{ds_title}{mode}"
                        axis.text(ax_text[ax_id][0],
                                  ax_text[ax_id][1],
                                  f"{prefix}: {group.get_val(exp_idx, mode, ds_id)}",
                                  color=colors[exp_idx + color_offset[mode]],
                                  transform=axis.transAxes)
                        ax_text[ax_id] = (ax_text[ax_id][0], ax_text[ax_id][1] - 0.1)
                        if ax_text[ax_id][1] < 0:
                            ax_text[ax_id] = (ax_text[ax_id][0] + 0.5, 0.9)
            elif group.ndim() == 2:
                for mode, dsv in group[exp_idx].items():
                    for ds_id, data in dsv.items():
                        ds_title = f"{ds_id} " if ds_id else ''
                        title = f"{experiment.name} ({ds_title}{mode})" if n_experiments > 1 else f"{ds_title}{mode}"
                        if data.shape[0] < 2:
                            # This particular mode only has a single data point, so draw a shape instead of a line
                            xy = [data[0][0], data[0][1]]
                            if mode == 'train':
                                style = MarkerStyle(marker='o', fillstyle='full')
                            elif mode == 'eval':
                                style = MarkerStyle(marker='D', fillstyle='full')
                            elif mode == 'test':
                                style = MarkerStyle(marker='s', fillstyle='full')
                            else:
                                style = MarkerStyle(marker='d', fillstyle='full')
                            if isinstance(xy[1], ValWithError):
                                # We've got error bars
                                x = xy[0]
                                y = xy[1]
                                # Plotting requires positive values for error
                                y_err = [[max(1e-9, y.y - y.y_min)], [max(1e-9, y.y_max - y.y)]]
                                axis.errorbar(x=x,
                                              y=y.y,
                                              yerr=y_err,
                                              ecolor=colors[exp_idx + color_offset[mode]],
                                              elinewidth=1.5,
                                              capsize=4.0,
                                              capthick=1.5,
                                              zorder=3)  # zorder to put markers on top of line segments
                                xy[1] = y.y
                            s = axis.scatter(xy[0],
                                             xy[1],
                                             s=45,
                                             c=[colors[exp_idx + color_offset[mode]]],
                                             label=title,
                                             marker=style,
                                             linewidth=1.0,
                                             edgecolors='black',
                                             zorder=4)  # zorder to put markers on top of line segments
                            if ds_id and ds_id_markers[ds_id]:
                                # Overlay the dataset id marker on top of the normal scatter plot marker
                                s2 = axis.scatter(xy[0],
                                                  xy[1],
                                                  s=45,
                                                  c='white',
                                                  label=title,
                                                  marker=ds_id_markers[ds_id],
                                                  linewidth=1.1,
                                                  zorder=5)  # zorder to put markers on top of line segments
                                s = (s, s2)
                            if not has_label[exp_idx][mode][ds_id]['patch']:
                                labels.append(title)
                                handles.append(s)
                                has_label[exp_idx][mode][ds_id]['patch'] = True
                        else:
                            # We can draw a line
                            y = data[:, 1]
                            y_min = None
                            y_max = None
                            if isinstance(y[0], ValWithError):
                                y = np.stack(y)
                                y_min = y[:, 0]
                                y_max = y[:, 2]
                                y = y[:, 1]
                                if smooth_factor != 0:
                                    y_min = gaussian_filter1d(y_min, sigma=smooth_factor)
                                    y_max = gaussian_filter1d(y_max, sigma=smooth_factor)
                            if smooth_factor != 0:
                                y = gaussian_filter1d(y, sigma=smooth_factor)
                            x = data[:, 0]
                            ln = axis.plot(
                                x,
                                y,
                                color=colors[exp_idx + color_offset[mode]],
                                label=title,
                                linewidth=1.5,
                                linestyle='solid' if mode == 'train' else
                                'dashed' if mode == 'eval' else 'dotted' if mode == 'test' else 'dashdot',
                                marker=ds_id_markers[ds_id],
                                markersize=7,
                                markeredgewidth=1.5,
                                markeredgecolor='black',
                                markevery=0.1)
                            if not has_label[exp_idx][mode][ds_id]['line']:
                                labels.append(title)
                                handles.append(ln[0])
                                has_label[exp_idx][mode][ds_id]['line'] = True
                            if y_max is not None and y_min is not None:
                                axis.fill_between(x.astype(np.float32),
                                                  y_max,
                                                  y_min,
                                                  facecolor=colors[exp_idx + color_offset[mode]],
                                                  alpha=0.3,
                                                  zorder=-1)
            else:
                # Some kind of image or matrix. Not implemented yet.
                pass

    plt.tight_layout()

    if labels:
        if share_legend:
            # Sort the labels
            handles = [h for _, h in sorted(zip(labels, handles), key=lambda pair: pair[0])]
            labels = sorted(labels)
            # Split the labels over multiple legends if there are too many to fit in one axis
            elems_per_legend = math.ceil(len(labels) / n_legends)
            i = 0
            for r in range(last_row_idx, n_rows):
                for c in range(last_column_idx + 1 if r == last_row_idx else 0, n_cols):
                    if len(handles) <= i:
                        break
                    axs[r][c].legend(
                        handles[i:i + elems_per_legend],
                        labels[i:i + elems_per_legend],
                        loc='center',
                        fontsize='large' if elems_per_legend <= 6 else 'medium' if elems_per_legend <= 8 else 'small')
                    i += elems_per_legend
        else:
            for i in range(n_rows):
                for j in range(n_cols):
                    if i == last_row_idx and j > last_column_idx:
                        break
                    # We need to do some processing here to make per-dataset entries appear correctly
                    handles, labels = axs[i][j].get_legend_handles_labels()
                    labels.append('_')  # labels that start with _ wouldn't be collected, so we can use this to pad
                    merged_h, merged_l = [], []
                    idx = 0
                    while idx < len(handles):
                        # duplicates should always be next to one another since they appear as a result of ds_id patches
                        if labels[idx] == labels[idx+1]:
                            merged_l.append(labels[idx])
                            merged_h.append((handles[idx], handles[idx+1]))
                            idx += 1
                        else:
                            merged_l.append(labels[idx])
                            merged_h.append(handles[idx])
                        idx += 1
                    # Apply the same sort order that we'd have if the legend were separate
                    handles = [h for _, h in sorted(zip(merged_l, merged_h), key=lambda pair: pair[0])]
                    labels = sorted(merged_l)
                    axs[i][j].legend(handles, labels, loc='best', fontsize='small')
    return fig


def visualize_logs(experiments: List[Summary],
                   save_path: str = None,
                   smooth_factor: float = 0,
                   share_legend: bool = True,
                   pretty_names: bool = False,
                   ignore_metrics: Optional[Set[str]] = None,
                   include_metrics: Optional[Set[str]] = None,
                   verbose: bool = True,
                   dpi: int = 300):
    """A function which will save or display experiment histories for comparison viewing / analysis.

    Args:
        experiments: Experiment(s) to plot.
        save_path: The path where the figure should be saved, or None to display the figure to the screen.
        smooth_factor: A non-negative float representing the magnitude of gaussian smoothing to apply (zero for none).
        share_legend: Whether to have one legend across all graphs (True) or one legend per graph (False).
        pretty_names: Whether to modify the metric names in graph titles (True) or leave them alone (False).
        ignore_metrics: Any metrics to ignore during plotting.
        include_metrics: A whitelist of metric keys (None whitelists all keys).
        verbose: Whether to print out the save location.
        dpi: The dpi at which to save the figure.
    """
    plot_logs(experiments,
              smooth_factor=smooth_factor,
              share_legend=share_legend,
              pretty_names=pretty_names,
              ignore_metrics=ignore_metrics,
              include_metrics=include_metrics)
    if save_path is None:
        plt.show()
    else:
        save_path = os.path.normpath(save_path)
        root_dir = os.path.dirname(save_path)
        if root_dir == "":
            root_dir = "."
        os.makedirs(root_dir, exist_ok=True)
        save_file = os.path.join(root_dir, os.path.basename(save_path) or 'parse_logs.png')
        if verbose:
            print("Saving to {}".format(save_file))
        plt.savefig(save_file, dpi=dpi, bbox_inches="tight")
