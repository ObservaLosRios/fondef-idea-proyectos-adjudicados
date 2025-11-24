import os
from src.extract import CSVExtractor
from src.transform import Fondef2000Transformer, Fondef2012Transformer, CleaningTransformer
from src.load import CSVLoader
from src.pipeline import ETLPipeline

def main():
    # Configuration
    raw_data_dir = 'data/raw'
    processed_data_dir = 'data/processed'
    
    # File 1: 2000-2011
    file1_path = os.path.join(raw_data_dir, 'Proyectos-ID-Adjudicados-2000-2011.csv')
    if os.path.exists(file1_path):
        pipeline1 = ETLPipeline(
            extractor=CSVExtractor(file1_path, header=4), # Header is on the 5th line
            transformers=[
                Fondef2000Transformer(),
                CleaningTransformer()
            ],
            loader=CSVLoader(processed_data_dir)
        )
        pipeline1.run('fondef_2000_2011_processed.csv')
    else:
        print(f"Warning: {file1_path} not found.")

    # File 2: 2012-2017
    file2_path = os.path.join(raw_data_dir, 'Proyectos-IDeA-Adjudicados-2012-2017-1.csv')
    if os.path.exists(file2_path):
        pipeline2 = ETLPipeline(
            extractor=CSVExtractor(file2_path), # Default header=0
            transformers=[
                Fondef2012Transformer(),
                CleaningTransformer()
            ],
            loader=CSVLoader(processed_data_dir)
        )
        pipeline2.run('fondef_2012_2017_processed.csv')
    else:
        print(f"Warning: {file2_path} not found.")

if __name__ == "__main__":
    main()
