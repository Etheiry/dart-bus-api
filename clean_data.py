import pandas as pd

# Load the dataset (update the filename if needed)
file_path = "dart_bus_schedules.csv"  # Change this to your actual file path
df = pd.read_csv(file_path)

# Display basic dataset info
print("Dataset Columns:", df.columns)
print("\nFirst 5 Rows:")
print(df.head())

# Check for missing values
print("\nMissing Values:")
print(df.isnull().sum())

# Save to a cleaned file (Optional)
cleaned_file = "dart_cleaned_schedule.csv"
df.dropna().to_csv(cleaned_file, index=False)
print(f"\nCleaned dataset saved as {cleaned_file}")
