from eradication_data_requirements.fit_ramsey_time_series import (
    add_slopes_to_effort_capture_data,
    add_probs_to_effort_capture_data,
    fit_resampled_cumulative,
    fit_resampled_captures,
)
from eradication_data_requirements.plot_progress_probability import plot_progress_probability

import pandas as pd
import typer
from typing_extensions import Annotated
import matplotlib.pyplot as plt

app = typer.Typer()


@app.command()
def write_progress_probability_figure(
    data_path: str = typer.Option("", help="Input file path"),
    figure_path: str = typer.Option("", help="Output file path"),
):
    monthly_progress_probability = pd.read_csv(data_path)
    plot_progress_probability(monthly_progress_probability)
    plt.savefig(figure_path)


@app.command()
def write_effort_and_captures_with_probability(
    input_path: str = typer.Option(help="Input file path"),
    bootstrapping_number: int = typer.Option(help="Bootstrapping number"),
    output_path: str = typer.Option(help="Output file path"),
    window_length: int = typer.Option(help="Window length for removal rate"),
    resample_method: Annotated[str, typer.Option(help="")] = "captures",
):
    effort_capture_data = pd.read_csv(input_path)
    resample_method_dictionary = {
        "captures": fit_resampled_captures,
        "cumulative": fit_resampled_cumulative,
    }
    effort_captures_with_slopes = add_probs_to_effort_capture_data(
        effort_capture_data,
        bootstrapping_number,
        window_length,
        resample_method_dictionary[resample_method],
    )
    effort_captures_with_slopes.to_csv(output_path, index=False)


@app.command()
def write_effort_and_captures_with_slopes(
    input_path: str = typer.Option("", help="Input file path"),
    output_path: str = typer.Option("", help="Output file path"),
):
    effort_capture_data = pd.read_csv(input_path)
    effort_captures_with_slopes = add_slopes_to_effort_capture_data(effort_capture_data)
    effort_captures_with_slopes.to_csv(output_path, index=False)
