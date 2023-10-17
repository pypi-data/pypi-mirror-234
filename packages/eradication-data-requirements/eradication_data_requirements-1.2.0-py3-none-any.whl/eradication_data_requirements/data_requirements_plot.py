import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from geci_plots import geci_plot


def fit_ramsey_plot(data):
    assert len(data["Cumulative_captures"].unique()) > 1, "It can not fit Ramsey plot"
    fit = np.polynomial.polynomial.Polynomial.fit(data["Cumulative_captures"], data["CPUE"], deg=1)
    intercept_and_slope = fit.convert().coef
    idx = [1, 0]
    slope_and_intercept = intercept_and_slope[idx]
    return slope_and_intercept


def plot_comparative_catch_curves(socorro_path, guadalupe_path, output_path):
    socorro_data = pd.read_csv(socorro_path)
    guadalupe_data = pd.read_csv(guadalupe_path)
    geci_plot()
    plot_catch_curve(socorro_data, "Socorro")
    plot_catch_curve(guadalupe_data, "Guadalupe")
    plt.xlabel("Cumulative captures", size=15, labelpad=15)
    plt.ylabel("CPUE (captures/night traps)", size=15)
    plt.legend(fontsize="xx-large")
    plt.savefig(output_path, dpi=300, transparent=True)


def data_requirements_plot(input_path, output_path):
    data = pd.read_csv(input_path)
    geci_plot()
    plot_catch_curve(data)
    plt.xlabel("Cumulative captures", size=15, labelpad=15)
    plt.ylabel("CPUE (captures/night traps)", size=15)
    plt.savefig(output_path, dpi=300, transparent=True)


def plot_catch_curve(data, label=None):
    theta = fit_ramsey_plot(data.drop([0]))
    y_line = theta[1] + theta[0] * data["Cumulative_captures"]
    plt.plot(data["Cumulative_captures"], y_line, "r")
    plt.scatter(data["Cumulative_captures"], data["CPUE"], marker="o", label=label)
