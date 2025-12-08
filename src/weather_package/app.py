from __future__ import annotations

import io
from contextlib import redirect_stdout

import pandas as pd
import streamlit as st

from weather_package.analysis import add, run_analysis_pipeline
from weather_package.cleaning import run_cleaning_pipeline


def ski_resorts() -> pd.DataFrame:
    """Load in our ski resort data."""
    return pd.read_csv("ski_resorts.csv")

df = ski_resorts()


def _run_with_capture(func) -> str:
    """Capture stdout from placeholder pipelines so Streamlit can display it."""
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        func()
    return buffer.getvalue().strip()


def main() -> None:
    st.set_page_config(page_title="Ski Resort Analysis", layout="wide")
    st.title("Ski Resort Analysis")
    st.write(
        "In our preliminary project proposal, we expressed interest in examining snowfall patterns and exploring the potential to predict snowfall for skiers. However, after evaluating the data available to us, we found that a different set of questions could be addressed more effectively. Specifically, we became interested in how ski resort characteristics, such as size, elevation and geographic location, relate to annual snowfall. We also aim to identify which resorts across the United States and Canada receive the greatest snowfall. Understanding these patterns can help skiers make more informed decisions when planning trips and selecting destinations that maximize their time on the snow."
        " After implementing a full cleaning pipeline and running exploratory data analysis (EDA), we identified clear trends: Western Canada and the Western U.S. have the highest average annual snowfall, Utah and Washington consistently exhibit the highest average annual snowfall, and high elevation is moderately associated with higher snowfall. These findings can support tourism planning, resort benchmarking, and ultimately help skiers decide where to ski."
    )

    with st.sidebar:
        st.header("Controls")
        dataset_choice = st.selectbox("Dataset", ["Ski Resort Data", "Upload CSV"])
        show_cleaning = st.checkbox("Preview cleaning pipeline output")
        show_analysis = st.checkbox("Preview analysis pipeline output")
        a = st.number_input("Toy add() input A", value=1)
        b = st.number_input("Toy add() input B", value=2)

    if dataset_choice == "Ski Resort Data":
        df = ski_resorts()
    else:
        uploaded = st.file_uploader("Upload a CSV file", type="csv")
        if uploaded:
            df = pd.read_csv(uploaded)
        else:
            st.info("No file uploaded yet. Falling back to the sample data so the widgets stay live.")
            df = ski_resorts()

    st.subheader("Data Preview")
    st.dataframe(df, use_container_width=True)

    st.subheader("Quick Math Sandbox")
    st.write(
        "The package's `add` helper is wired up below so students can see how to surface custom utilities."
    )
    st.metric(label="add(a, b)", value=add(a, b))

    if show_cleaning:
        st.subheader("Cleaning Pipeline Output")
        cleaning_output = _run_with_capture(
            lambda: run_cleaning_pipeline(
                url="https://en.wikipedia.org/wiki/Comparison_of_North_American_ski_resorts",
                email="wella2@byu.edu"
            ))
        st.code(cleaning_output or "run_cleaning_pipeline() did not emit text.")
        st.caption("Replace run_cleaning_pipeline with your real preprocessing logic.")

    if show_analysis:
        st.subheader("Analysis Pipeline Output")
        analysis_output = _run_with_capture(
            lambda: run_analysis_pipeline(df))
        st.code(analysis_output or "run_analysis_pipeline() did not emit text.")
        st.caption("Swap this stub with charts, metrics, or model diagnostics from your project.")

    st.info(
        "Next steps: customize the sidebar controls, drop in Streamlit charts (st.bar_chart, st.map, etc.), "
        "and layer in explanations so stakeholders can self-serve results."
    )


if __name__ == "__main__":
    main()