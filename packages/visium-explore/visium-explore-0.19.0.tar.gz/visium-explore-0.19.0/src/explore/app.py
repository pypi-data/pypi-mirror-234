"""Streamlit app for data exploration."""
import pathlib

import streamlit as st

from explore.constants import NROWS
from explore.explorer_container.main import explorer_container
from explore.graph_container.main import graph_container
from explore.sample_df_container.main import display_sample_df_container, read_df_top_rows
from explore.utils import discover_parquet_files, parse_dvc_steps_from_dvc_yaml, select_file_container

DATA_PATH = pathlib.Path("data")


st.set_page_config(layout="wide")


def main() -> None:
    """Main function for the Streamlit app."""
    col1, col2 = st.columns([1, 1])
    dvc_steps = parse_dvc_steps_from_dvc_yaml()
    with col1:
        st.title("Explorer")

        selected_dvc_step = st.selectbox(label="DVC Step selection", options=dvc_steps, format_func=lambda x: x.name)
        dvc_step_key = f"select_box_{selected_dvc_step.name}"
        parquet_files_path_list = discover_parquet_files(selected_dvc_step.output_path)
        if len(parquet_files_path_list) > 0:
            file_path = select_file_container(parquet_files_path_list, dvc_step_key)
        else:
            st.warning("No output parquet data found for this DVC step.")
            file_path = None
    with col2:
        graph_container()

    if file_path:
        sample_df = read_df_top_rows(file_path, nrows=NROWS)

        display_sample_df_container(sample_df)

        explorer_container(file_path, dvc_step_key, sample_df=sample_df)
    else:
        st.warning("No parquet file found for this DVC step.")


if __name__ == "__main__":
    main()
