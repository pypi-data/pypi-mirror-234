"""Streamlit component to display a sample of a dataframe and its schema."""
import pathlib

import pandas as pd
import pyarrow
import streamlit as st
from pyarrow.parquet import ParquetFile

from explore.constants import NROWS


def display_sample_df_container(sample_df: pd.DataFrame) -> pd.DataFrame:
    """Display a sample of the selected dataframe."""
    st.write("---")
    st.header("Data model")
    col1, col2 = st.columns(spec=[4, 1])
    with col1:
        st.subheader("Sample DataFrame")
        # Streamlit does not support displaying timedelta types at the moment.
        if (sample_df.dtypes == "timedelta64[ns]").any():
            td_cols = sample_df.dtypes.index[sample_df.dtypes == "timedelta64[ns]"]
            for col in td_cols:
                sample_df[col] = sample_df[col].dt.total_seconds()

        st.write(sample_df)
    with col2:
        st.subheader("Schema")
        schema_df = pd.DataFrame(sample_df.dtypes).rename(columns={0: "types"})
        st.write(schema_df)


@st.cache_data
def read_df_top_rows(file_path: pathlib.Path, nrows: int) -> pd.DataFrame:
    """Read top nrows rows of a DataFrame in a memory efficient manner, using pyarrow."""
    pf = ParquetFile(file_path)
    first_rows = next(pf.iter_batches(batch_size=nrows))
    df = pyarrow.Table.from_batches([first_rows]).to_pandas()

    return df
