import pandas as pd
from .interfaces import IDataLoader
import os

class CSVLoader(IDataLoader):
    """Loads data into a CSV file."""
    
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def load(self, df: pd.DataFrame, filename: str) -> None:
        output_path = os.path.join(self.output_dir, filename)
        print(f"Saving processed data to {output_path}...")
        df.to_csv(output_path, index=False, encoding='utf-8-sig')
        print("Save complete.")
