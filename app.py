from __future__ import annotations

import io
from contextlib import redirect_stdout

import pandas as pd
import streamlit as st

from weather_package import run_cleaning_pipeline, run_analysis_pipeline


def ski_resorts() -> pd.DataFrame:
    """Load in our ski resort data."""
    return pd.read_csv("src/weather_package/ski_resorts.csv")

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
        show_cleaning = st.checkbox("Cleaning pipeline output")
        show_analysis = st.checkbox("Analysis pipeline output")

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

    if show_cleaning:
        st.subheader("Cleaning Pipeline Output")

        cleaned_df = run_cleaning_pipeline(
            url="https://en.wikipedia.org/wiki/Comparison_of_North_American_ski_resorts",
            email="wella2@byu.edu"
        )

        st.dataframe(cleaned_df)
        st.caption("Here we are cleaning the data")

    if show_analysis:
        if 'cleaned_df' not in locals():
            st.error("You must run the cleaning step before analysis.")
        else:
            analysis_output = _run_with_capture(
                lambda: run_analysis_pipeline(cleaned_df)
            )
            st.code(analysis_output or "No text emitted.")

        # --- 1. Snowfall Boxplot ---
        st.write("### Snowfall Distribution by Resort")
        st.markdown("""
        Western Canada experience substantially higher snowfall than other regions, 
        while the Midwest and the Southeastern United States receive the least. 
        These patterns are consistent with geographic and climatic expectations: 
        western regions contain more mountainous terrain that promotes orographic precipitation, 
        whereas southern regions have warmer temperatures due to their lower latitudes, 
        resulting in reduced snowfall.
        """)
        st.image("plots/boxplot.png", use_container_width=True)

        # --- 2. Correlation Heatmap ---
        st.write("### Correlation Heatmap")
        st.markdown("""
        We were also curious about the correlation between certain numeric features of the data, 
        total trails, total lifts, and average snowfall. We can see a high positive correlation 
        between the number of trails and number of lifts. That makes sense, considering the 
        structure of a ski resort. There is a moderate correlation between total trails and 
        average snow fall.
        """)
        st.image("plots/correlation_heatmap.png", use_container_width=True)

        # --- 3. Snowfall Distribution ---
        st.write("### Distribution of Annual Snowfall")
        st.markdown("""
        We looked at the distribution of snowfall for the top 20 ski resorts with the highest 
        snowfall. This is left skewed where there are a few resorts that receive an unusually 
        high level of snowfall on average.
        """)
        st.image("plots/distribution_snowfall.png", use_container_width=True)

        # --- 4. Top 10 Resorts ---
        st.write("### Top 10 Resorts by Average Annual Snowfall")
        st.markdown("""
        We then looked at the top 10 resorts that had the highest peak elevation. 
        Nine out of the top 10 resorts were in Colorado. This was a really interesting finding. 
        It seems to be that Colorado has the steepest terrain. The peak elevation was ~ 12,000 - 13,000 
        for these Colorado resorts. For these resorts, the average annual snowfall ranged from 235 
        to 450 inches. It seems that these resorts that have high elevation also have higher average 
        annual snowfall.  
        After looking at the top 10 resorts for elevation, we were curious to see the top 10 resorts 
        for average annual snowfall. The top resort was Alyeska Resort in Alaska with an average 
        of 643 inches of snowfall each year. From these top 10 resorts, 3 of them were from Utah 
        (Alta, Brighton, & Snowbird)
        """)
        st.image("plots/annual_snowfall.png", use_container_width=True)
        
        # --- 5. Annual Snowfall by State ---
        st.write("### Annual Snowfall by State")
        st.markdown("""
        To explore geographic differences in snowfall, we examined the Average Annual Snowfall 
        (inches) column alongside the State/Province column. We created a bar plot that displays 
        each state or province ranked by the snowfall values reported in our dataset. From this 
        visualization, Utah shows the highest average annual snowfall in our dataset, followed 
        by Washington and California. These rankings come directly from the average snowfall 
        values listed for the resorts located in each region. This plot provides a quick snapshot 
        of how snowfall conditions vary across different areas and highlights which regions tend 
        to have resorts with the largest reported snowfall amounts.
        """)
        st.image("plots/annual_snowfall.png", use_container_width=True)

        # --- 6. Elevation vs Snowfall ---
        st.write("### Peak Elevation vs Snowfall")
        st.markdown("""
        Next, we were interested to see how peak elevation and average snowfall are correlated. 
        The scatterplot comparing average annual snowfall to peak elevation reveals a clear 
        upward trend: resorts situated at higher elevations generally experience greater snowfall. 
        While the relationship is not perfectly linear—there is still noticeable spread at each 
        elevation level—the overall pattern suggests that elevation plays a meaningful role in 
        increasing snowfall totals. Higher-altitude resorts likely benefit from colder temperatures 
        and more favorable atmospheric conditions for sustained snowfall, which contributes to the 
        positive trend observed in the plot. This pattern supports the idea that elevation is an 
        important environmental factor influencing resort-level snow accumulation.
        """)
        st.image("plots/peak_elevation.png", use_container_width=True)


if __name__ == "__main__":
    main()