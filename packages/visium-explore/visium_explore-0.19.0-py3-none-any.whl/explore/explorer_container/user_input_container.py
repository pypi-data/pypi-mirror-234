"""Defines the container that takes user inputs for the exploration of variables."""
import abc
import pathlib
from typing import Optional, Union

import streamlit as st
from pydantic import BaseModel  # pylint: disable=no-name-in-module

from explore.explorer_container.plot import Plot


class UserInputs(BaseModel):
    """Class containing the user inputs for the exploration of variables."""

    plot_type: Optional[str] = None
    selected_col: str
    button_activator: bool
    selected_y: Optional[str] = None
    selected_color: Optional[str] = None
    selected_histfunc: Optional[str] = None
    selected_nbins: Optional[int] = None
    selected_marginal: Optional[str] = None
    selected_points: Optional[Union[str, bool]] = None
    selected_log_x: Optional[bool] = None
    selected_log_y: Optional[bool] = None
    selected_orientation: Optional[str] = None


def user_input_container(file_path: pathlib.Path, tab_key: str, columns: list[str]) -> UserInputs:
    """Container for user inputs."""
    # pylint: disable=too-many-locals
    dvc_step = file_path.parts[-1]
    selected_histfunc = None
    selected_nbins = None
    selected_marginal = None
    selected_points = None

    key = f"{tab_key}_{dvc_step}"
    selected_col = st.selectbox(
        "Select a column to inspect (x-axis)",
        options=sorted(columns),
        key=f"col_inspect_{key}",
    )
    plot_type = st.selectbox(
        "Select the type of plot you want to use",
        options=[None, "histogram", "box"],
        key=f"plot_type_{key}",
    )
    if plot_type:
        plot = Plot(columns=columns, key=key)
    if plot_type == "box":
        selected_points = st.selectbox(
            "Select how to display outliers",
            options=[
                None,
                "outliers",
                "suspectedoutliers",
                "all",
                False,
            ],
        )
    if plot_type == "histogram":
        selected_histfunc = st.selectbox(
            "Select an aggregation function",
            options=["avg", "count", "sum", "min", "max"],
            key=f"histfunc_{key}",
        )
        selected_nbins = st.selectbox(
            "Select the number of bins",
            options=[None, 3, 5, 10, 20],
            key=f"nbins_{key}",
        )
        selected_marginal = st.selectbox(
            "Select a marginal",
            options=[None, "rug", "box", "violin", "histogram"],
            key=f"marginal_{key}",
        )

    button_activator = st.button(
        "Inspect",
        key=f"button_activator_{key}",
    )
    return UserInputs(
        plot_type=plot_type,
        selected_col=selected_col,
        button_activator=button_activator,
        selected_y=plot.y_axis,
        selected_color=plot.color,
        selected_histfunc=selected_histfunc,
        selected_nbins=selected_nbins,
        selected_marginal=selected_marginal,
        selected_points=selected_points,
        selected_log_x=plot.log_x,
        selected_log_y=plot.log_y,
        selected_orientation=plot.orientation,
    )
