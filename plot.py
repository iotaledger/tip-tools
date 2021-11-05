# -*- coding: utf-8 -*-
import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import math
from itertools import cycle

matplotlib.use('TkAgg')

#===============================================================================
class PlotLine(object):
    def __init__(self, subplot_nr, x, y, name, is_y2=False, line_style='-'):
        self.subplot_nr = subplot_nr
        self.x          = x
        self.y          = y
        self.name       = name
        self.is_y2      = is_y2
        self.line_style = line_style

#===============================================================================
class Subplot(object):
    def __init__(self, row_index, column_index, x_label, y1_label, y2_label=None, x_scale='linear', y1_scale='linear', y2_scale='linear', legend_y1_loc='upper left', legend_y2_loc='upper right'):
        self.row_index      = row_index
        self.column_index   = column_index 
        self.x_label        = x_label
        self.y1_label       = y1_label
        self.y2_label       = y2_label
        self.x_scale        = x_scale
        self.y1_scale       = y1_scale
        self.y2_scale       = y2_scale
        self.legend_y1_loc  = legend_y1_loc
        self.legend_y2_loc  = legend_y2_loc

        self.axis           = None

#===============================================================================
def plot(sub_plots, plot_lines, show_plot=True, title=None, file_path=None, size_x_inches=7.0, size_y_inches=5.0, dpi=100.0):

    nrows = 1
    ncols = 1
    for sub_plot in sub_plots:
        if nrows < sub_plot.row_index+1:
            nrows = sub_plot.row_index+1
        if ncols < sub_plot.column_index+1:
            ncols = sub_plot.column_index+1

    # Create plot
    fig, axis_list = plt.subplots(nrows=nrows, ncols=ncols, sharex=True, squeeze=False)
    if title != None:
        plt.title(title)

    # Fullscreen
    mng = plt.get_current_fig_manager()
    mng.resize(*mng.window.maxsize())

    if len(sub_plots) == 1:
        axis_list = [axis_list]

    for subplot_nr, sub_plot in enumerate(sub_plots):
        sub_plot.axis = axis_list[sub_plot.row_index][sub_plot.column_index]
        sub_plot.axis.grid(True)
        sub_plot.axis.set_xscale(sub_plot.x_scale)
        sub_plot.axis.set_yscale(sub_plot.y1_scale)
        sub_plot.axis.set_xlabel(sub_plot.x_label)
        sub_plot.axis.set_ylabel(sub_plot.y1_label, fontsize=8)

        if sub_plot.y2_label != None:
            sub_plot.axis_y2 = sub_plot.axis.twinx()  # instantiate a second axes that shares the same x-axis
            sub_plot.axis_y2.grid(True)
            sub_plot.axis_y2.set_xscale(sub_plot.x_scale)
            sub_plot.axis_y2.set_yscale(sub_plot.y2_scale)
            sub_plot.axis_y2.set_xlabel(sub_plot.x_label)
            sub_plot.axis_y2.set_ylabel(sub_plot.y2_label, fontsize=8)

    prop_cycle = plt.rcParams['axes.prop_cycle']
    colors = cycle(prop_cycle.by_key()['color'])
    
    for plot_line in plot_lines:
        if not plot_line.is_y2:
            sub_plots[plot_line.subplot_nr].axis.plot(plot_line.x, plot_line.y, plot_line.line_style, linewidth=2, label=plot_line.name, color=next(colors))
        else:
            sub_plots[plot_line.subplot_nr].axis_y2.plot(plot_line.x, plot_line.y, plot_line.line_style, linewidth=2, label=plot_line.name, color=next(colors))

    for subplot_nr, sub_plot in enumerate(sub_plots):
        sub_plot.axis.legend(loc=sub_plot.legend_y1_loc)
        if hasattr(sub_plot, 'axis_y2'):
            sub_plot.axis_y2.legend(loc=sub_plot.legend_y2_loc)

    fig.tight_layout()
    plt.autoscale(enable=True, axis='both', tight=None)

    if file_path != None:
        if not os.path.exists(os.path.dirname(file_path)):
            os.makedirs(os.path.dirname(file_path))
        fig.set_size_inches(size_x_inches, size_y_inches)
        plt.draw()
        plt.savefig(file_path, dpi=dpi)

    if show_plot:
        plt.show()
