"""Module for the different plot types, their settings and their corresponding streamlit selectors."""
import abc

import pandas as pd
import plotly.express as px
import streamlit as st


class Plot:
    """Base class for the different plot types, their settings and their corresponding streamlit selectors."""

    def __init__(self, columns: list, key: str):
        """Construct Plot object."""
        st.markdown("---")

        self.form = st.form(key=f"form_{key}")
        with self.form:
            st.subheader(f"Settings for {self.__str__()}")
            st.write("Main settings")

            self.y_axis = st.selectbox("Select a y-axis", options=[None] + columns, key=f"abscissa_col_{key}")
            self.color = st.selectbox("Select a color field", options=[None] + columns, key=f"color_col_{key}")
            self.log_x = st.selectbox(
                "Activate log scaling for the x-axis",
                options=[False, True],
                key=f"log_x_{key}",
            )
            self.log_y = st.selectbox(
                "Activate log scaling for the y-axis",
                options=[False, True],
                key=f"log_y_{key}",
            )
            self.orientation = st.selectbox(
                "Choose the orientation:",
                options=[None, "h", "v"],
                key=f"orientation_{key}",
            )
            st.write("---")
            st.write(f"{self.__str__()} specific settings")

    @abc.abstractmethod
    def show():
        """Show the plot in the streamlit webapp."""
        pass

    @abc.abstractmethod
    def __str__(self) -> str:
        """Return the name of the plot."""
        pass


class Histogram(Plot):
    """Class containing the settings for the histogram plot."""

    def __init__(self, columns: list, key: str):
        """Construct the histogram plot settings."""
        super().__init__(columns, key)

        with self.form:
            self.histfunc = st.selectbox(
                "Select an aggregation function",
                options=[None, "count", "sum", "min", "max", "avg"],
                key=f"histfunc_{key}",
            )
            self.nbins = st.selectbox(
                "Select the number of bins",
                options=[None, 3, 5, 10, 20],
                key=f"nbins_{key}",
            )
            self.marginal = st.selectbox(
                "Select a marginal",
                options=[None, "rug", "box", "violin", "histogram"],
                key=f"marginal_{key}",
            )
        self.form.form_submit_button(label="Submit")

    def show(self, df: pd.DataFrame, selected_col: str) -> None:
        """Show the histogram in the streamlit webapp."""
        fig = px.histogram(
            df,
            x=selected_col,
            y=self.y_axis,
            color=self.color,
            barmode="group",
            histfunc=self.histfunc,
            nbins=self.nbins,
            marginal=self.marginal,
            log_x=self.log_x,
            log_y=self.log_y,
            category_orders=determine_category_order(selected_col=selected_col, selected_y=self.y_axis, df=df),
            orientation=self.orientation,
        )
        st.plotly_chart(fig, use_container_width=True)

    def __str__(self) -> str:
        """Return the name of the plot."""
        return "Histogram"


class Box(Plot):
    """Class containing the settings for box plots."""

    def __init__(self, columns: list, key: str):
        """Constuct the box plot settings."""
        super().__init__(columns, key)

        with self.form:
            self.selected_points = st.selectbox(
                "Select how to display outliers",
                options=[
                    None,
                    "outliers",
                    "suspectedoutliers",
                    "all",
                    False,
                ],
            )
        self.form.form_submit_button(label="Submit")

    def show(self, df: pd.DataFrame, selected_col: str) -> None:
        """Show the box plot in the streamlit webapp."""
        fig = px.box(
            df,
            x=selected_col,
            y=self.y_axis,
            color=self.color,
            points=self.selected_points,
            log_x=self.log_x,
            log_y=self.log_y,
            category_orders=determine_category_order(selected_col=selected_col, selected_y=self.y_axis, df=df),
            orientation=self.orientation,
        )
        st.plotly_chart(fig, use_container_width=True)

    def __str__(self) -> str:
        """Return the name of the plot."""
        return "Box"


def determine_category_order(selected_col: str, selected_y: str, df: pd.DataFrame) -> dict:
    """Determine the category order for the plotly figure."""
    category_order = {selected_col: list(df[selected_col].value_counts().index)}
    if selected_y:
        category_order[selected_y] = list(df[selected_y].value_counts().index)
    return category_order
