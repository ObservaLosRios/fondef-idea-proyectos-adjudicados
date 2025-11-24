import pandas as pd
from typing import List
from .interfaces import IDataSource, IDataTransformer, IDataLoader

class ETLPipeline:
    """Orchestrates the ETL process."""
    
    def __init__(self, extractor: IDataSource, transformers: List[IDataTransformer], loader: IDataLoader):
        self.extractor = extractor
        self.transformers = transformers
        self.loader = loader

    def run(self, output_filename: str):
        """Runs the pipeline."""
        print("Starting ETL pipeline...")
        
        # Extract
        df = self.extractor.extract()
        
        # Transform
        for transformer in self.transformers:
            df = transformer.transform(df)
            
        # Load
        self.loader.load(df, output_filename)
        print("Pipeline finished successfully.")
