import pandas as pd
from weather_package.analysis import run_analysis_pipeline, add

def test_run_analysis_pipeline_prints_message(capsys):
    # Create a minimal dummy DataFrame for the pipeline to run
    df = pd.DataFrame({
        "Resort Name": ["Test Resort"],
        "State/Province": ["Utah"],
        "Average Annual Snowfall (inches)": ["300"],
        "Peak Elevation (ft)": [10000]
    })

    run_analysis_pipeline(df)
    captured = capsys.readouterr()
    assert "Running analysis pipeline..." in captured.out

def test_add_handles_various_numbers():
    assert add(1, 2) == 3
    assert add(-1, 5) == 4
    assert add(-3, -4) == -7