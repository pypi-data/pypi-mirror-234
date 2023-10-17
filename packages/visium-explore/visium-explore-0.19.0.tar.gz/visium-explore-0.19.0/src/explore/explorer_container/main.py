"""The explorer container allows the user to interact with the chosen data by selecting columns to explore and plot."""
import pathlib

import pandas as pd
import streamlit as st

from explore.explorer_container.constants import PlotTypes
from explore.explorer_container.plot import Box, Histogram


def explorer_container(file_path: pathlib.Path, tab_key: str, sample_df: pd.DataFrame) -> None:
    """Display the explorer container.

    It allows the user to interact with the chosen data by selecting columns to explore and plot.
    """
    st.write("---")
    st.header("Data exploration")

    file_path = pathlib.Path(file_path)
    dvc_step = file_path.parts[-1]
    columns = list(sample_df.columns)

    col1, col2 = st.columns([1, 3])
    with col1:
        key = f"{tab_key}_{dvc_step}"
        selected_col = st.selectbox(
            "Select a column to inspect (x-axis)",
            options=sorted(columns),
            key=f"col_inspect_{key}",
        )
        plot_type = st.selectbox(
            "Select the type of plot you want to use",
            options=[None, PlotTypes.HISTOGRAM, PlotTypes.BOX],
            key=f"plot_type_{key}",
        )

        if plot_type == PlotTypes.HISTOGRAM:
            plot = Histogram(columns=columns, key=key)
        elif plot_type == PlotTypes.BOX:
            plot = Box(columns=columns, key=key)
        else:
            plot = None

    with col2:
        df = pd.read_parquet(file_path)

        inner_col1, inner_col2 = st.columns([1, 3])
        with inner_col1:
            univariate_description_df = df[selected_col].describe()
            st.write(univariate_description_df)
            if plot is not None and plot.y_axis and pd.api.types.is_object_dtype(df[selected_col]):
                groupby_description = df.groupby(selected_col)[plot.y_axis].describe()
                groupby_description = groupby_description.sort_values(by="count", ascending=False)
                st.write(groupby_description)
        with inner_col2:
            if plot is not None:
                plot.show(df=sample_df, selected_col=selected_col)
            else:
                st.warning("Please select a plot type on the left.")
        # exploration_container(file_path, user_inputs=user_inputs)
