from eradication_data_requirements.cli import (
    write_effort_and_captures_with_probability,
    write_progress_probability_figure,
)
from eradication_data_requirements.data_requirements_plot import data_requirements_plot
from fastapi import FastAPI

api = FastAPI()


@api.get("/write_effort_and_captures_with_probability")
async def api_write_effort_and_captures_with_probability(
    input_path: str, bootstrapping_number: int, output_path: str, window_length: int
):
    resample_method = "cumulative"
    write_effort_and_captures_with_probability(
        input_path, bootstrapping_number, output_path, window_length, resample_method
    )


@api.get("/write_probability_figure")
async def api_write_probability_figure(input_path: str, output_path: str):
    write_progress_probability_figure(input_path, output_path)


@api.get("/plot_cpue_vs_cum_captures")
async def api_plot_cpue_vs_cum_captures(input_path: str, output_path: str):
    data_requirements_plot(input_path, output_path)
