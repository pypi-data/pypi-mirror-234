"""Streamlit app module for the exploration container."""
import pathlib

import pandas as pd
import plotly.express as px
import streamlit as st

from explore.explorer_container.user_input_container import UserInputs


def exploration_container(file_path: pathlib.Path, user_inputs: UserInputs) -> None:
    """Display the exploration container.

    It allows the user to interact with the chosen data by selecting columns to explore and plot.
    """
    if user_inputs.button_activator:
        df = pd.read_parquet(file_path)

        col1, col2 = st.columns([1, 3])

        with col1:
            univariate_description_df = df[user_inputs.selected_col].describe()
            st.write(univariate_description_df)
            if user_inputs.selected_y and pd.api.types.is_object_dtype(df[user_inputs.selected_col]):
                groupby_description = df.groupby(user_inputs.selected_col)[user_inputs.selected_y].describe()
                groupby_description = groupby_description.sort_values(by="count", ascending=False)
                st.write(groupby_description)
        with col2:
            show_plotly_figure(df, user_inputs)
    else:
        st.warning("Select options on the left to load and explore the data.\nThen click on Inspect.")


def show_plotly_figure(df: pd.DataFrame, user_inputs: UserInputs) -> None:
    """Show a plotly figure based on the dataframe and the user inputs."""
    if user_inputs.plot_type == "histogram":
        fig = px.histogram(
            df,
            x=user_inputs.selected_col,
            y=user_inputs.selected_y,
            color=user_inputs.selected_color,
            barmode="group",
            histfunc=user_inputs.selected_histfunc,
            nbins=user_inputs.selected_nbins,
            marginal=user_inputs.selected_marginal,
            log_x=user_inputs.selected_log_x,
            log_y=user_inputs.selected_log_y,
            category_orders=determine_category_order(user_inputs, df),
            orientation=user_inputs.selected_orientation,
        )
        st.plotly_chart(fig, use_container_width=True)
    elif user_inputs.plot_type == "box":
        fig = px.box(
            df,
            x=user_inputs.selected_col,
            y=user_inputs.selected_y,
            color=user_inputs.selected_color,
            points=user_inputs.selected_points,
            log_x=user_inputs.selected_log_x,
            log_y=user_inputs.selected_log_y,
            category_orders=determine_category_order(user_inputs, df),
            orientation=user_inputs.selected_orientation,
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("You can plot something by selecting an option on the left panel.")


def determine_category_order(user_inputs: UserInputs, df: pd.DataFrame) -> dict:
    """Determine the category order for the plotly figure."""
    category_order = {user_inputs.selected_col: list(df[user_inputs.selected_col].value_counts().index)}
    if user_inputs.selected_y:
        category_order[user_inputs.selected_y] = list(df[user_inputs.selected_y].value_counts().index)
    return category_order
