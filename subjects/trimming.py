from pathlib import Path
import pandas as pd

# Resolve the data file relative to this script so the script works
# regardless of the current working directory when invoked.
data_file = Path(__file__).resolve().parent / "derecho.jsonl"
if not data_file.exists():
    raise FileNotFoundError(f"Data file not found: {data_file}. Make sure the file exists.")

# Read the JSONL file and print counts of the 'tema' column
df = pd.read_json(data_file, lines=True)
print(df["tema"].value_counts().to_string())