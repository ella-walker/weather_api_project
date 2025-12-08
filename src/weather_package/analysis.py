import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="whitegrid")

# ---------------------------------------------------------
# Helper: Convert columns to numeric
# ---------------------------------------------------------
def convert_numeric_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert all numeric columns to numeric types (int or float).
    Non-numeric values will be coerced to NaN.
    """
    numeric_cols = [
        "Peak elevation (ft)",
        "Base elevation (ft)",
        "Vertical drop (ft)",
        "Skiable acreage",
        "Total trails",
        "Total lifts",
        "Average annual snowfall (in)",
    ]
    
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    
    return df

# ---------------------------------------------------------
# Helper: Histogram of snowfall
# ---------------------------------------------------------
def plot_snowfall_distribution(df):
    plt.figure(figsize=(10, 6))
    sns.histplot(df["Average Annual Snowfall (inches)"].dropna(), bins=30, kde=True)
    plt.title("Distribution of Average Annual Snowfall (inches)")
    plt.xlabel("Average Annual Snowfall (inches)")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.show()


# ---------------------------------------------------------
# Helper: Add geographic regions
# ---------------------------------------------------------
def assign_regions(df):
    state_region_map = {
        'Quebec': 'Eastern Canada',
        'British Columbia': 'Western Canada', 
        'Alberta': 'Western Canada',
        'Newfoundland and Labrador': 'Eastern Canada',
        'Nova Scotia': 'Eastern Canada',
        'Vermont': 'Northeast US',
        'Colorado': 'Western US',
        'Wyoming': 'Western US', 
        'Nevada': 'Western US', 
        'Idaho': 'Western US', 
        'Montana': 'Western US', 
        'Arizona': 'Western US', 
        'New Mexico': 'Western US',
        'Oregon': 'Western US', 
        'California': 'Western US', 
        'Alaska': 'Western US', 
        'Maine': 'Northeast US', 
        'Michigan': 'Midwest US',
        'New Jersey': 'Northeast US', 
        'Ontario': 'Eastern Canada', 
        'Utah': 'Western US', 
        'New York': 'Northeast US', 
        'West Virginia': 'Southeast US',
        'Washington': 'Western US', 
        'North Carolina': 'Southeast US', 
        'South Dakota': 'Midwest US', 
        'Virginia': 'Southeast US',
        'North Dakota': 'Midwest US', 
        'Connecticut': 'Northeast US', 
        'Rhode Island': 'Northeast US', 
        'Missouri': 'Midwest US',
        'Tennessee': 'Southeast US', 
        'Indiana': 'Midwest US', 
        'Ohio': 'Midwest US', 
        'Maryland': 'Southeast US', 
        'Massachusetts': 'Northeast US',
        'Illinois': 'Midwest US', 
        'Iowa': 'Midwest US', 
        'Alabama': 'Southeast US', 
        'Minnesota': 'Midwest US', 
        'New Hampshire': 'Northeast US',
        'Pennsylvania': 'Northeast US', 
        'Wisconsin': 'Midwest US'
    }

    df["Region"] = df["State/Province"].map(state_region_map)
    return df


# ---------------------------------------------------------
# Helper: Snowfall by region (boxplot)
# ---------------------------------------------------------
def plot_snowfall_by_region(df):
    plt.figure(figsize=(12, 8))
    sns.boxplot(x="Region", y="Average Annual Snowfall (inches)", data=df)
    plt.title("Average Annual Snowfall (inches) by Region")
    plt.xlabel("Region")
    plt.ylabel("Average Annual Snowfall (inches)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


# ---------------------------------------------------------
# Helper: Top 10 snowiest resorts
# ---------------------------------------------------------
def plot_top10_resorts(df):
    top10 = df.nlargest(10, "Average Annual Snowfall (inches)")

    plt.figure(figsize=(12, 8))
    sns.barplot(
        data=top10,
        y="Resort Name",
        x="Average Annual Snowfall (inches)",
        palette="coolwarm"
    )

    # Annotate
    for i, (resort, snowfall) in enumerate(
        zip(top10["Resort Name"], top10["Average Annual Snowfall (inches)"])
    ):
        plt.text(snowfall + 5, i, str(snowfall), va="center", fontsize=10)

    plt.xlabel("Average Annual Snowfall (inches)")
    plt.ylabel("Resort Name")
    plt.title("Top 10 Resorts by Average Annual Snowfall")
    plt.tight_layout()
    plt.show()


# ---------------------------------------------------------
# Helper: Mean snowfall by state
# ---------------------------------------------------------
def plot_state_average_snowfall(df):
    state_snow = (
        df.groupby("State/Province")["Average Annual Snowfall (inches)"]
        .mean()
        .sort_values(ascending=False)
        .reset_index()
    )

    plt.figure(figsize=(12, 8))
    sns.barplot(
        data=state_snow,
        y="State/Province",
        x="Average Annual Snowfall (inches)",
        palette="Blues_r"
    )

    # annotate
    for i, row in state_snow.iterrows():
        plt.text(
            row["Average Annual Snowfall (inches)"] + 2,
            i,
            f"{row['Average Annual Snowfall (inches)']:.0f}",
            va="center",
            fontsize=10,
        )

    plt.xlabel("Average Annual Snowfall (inches)")
    plt.ylabel("State/Province")
    plt.title("Average Annual Snowfall per State/Province")
    plt.tight_layout()
    plt.show()


# ---------------------------------------------------------
# Helper: Snowfall vs Elevation scatterplot
# ---------------------------------------------------------
def plot_snowfall_vs_elevation(df):
    plt.figure(figsize=(12, 8))
    sns.scatterplot(
        data=df,
        x="Peak Elevation (ft)",
        y="Average Annual Snowfall (inches)",
        hue="State/Province",
        palette="tab20",
        s=100,
        alpha=0.8,
    )

    # Annotate top 5 resorts
    top = df.nlargest(5, "Average Annual Snowfall (inches)")
    for _, row in top.iterrows():
        plt.text(
            row["Peak Elevation (ft)"] + 50,
            row["Average Annual Snowfall (inches)"] + 5,
            row["Resort Name"],
            fontsize=10,
        )

    plt.xlabel("Peak Elevation (ft)")
    plt.ylabel("Average Annual Snowfall (inches)")
    plt.title("Average Snowfall vs Peak Elevation of Ski Resorts")
    plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.tight_layout()
    plt.show()


# ---------------------------------------------------------
# MAIN ANALYSIS PIPELINE
# ---------------------------------------------------------
def run_analysis_pipeline(df):
    print("Running analysis pipeline...")

    df = convert_numeric_columns(df)
    df = assign_regions(df)

    plot_snowfall_distribution(df)
    plot_snowfall_by_region(df)
    plot_top10_resorts(df)
    plot_state_average_snowfall(df)
    plot_snowfall_vs_elevation(df)

    print("Analysis complete!")
    return df


# If running directly:
if __name__ == "__main__":
    df = pd.read_csv("data/ski_resorts_cleaned.csv")
    run_analysis_pipeline(df)

def add(a, b):
    return a + b


