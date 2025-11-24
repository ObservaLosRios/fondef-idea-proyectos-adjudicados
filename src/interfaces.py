from abc import ABC, abstractmethod
import pandas as pd

class IDataSource(ABC):
    """Interface for data extraction."""
    
    @abstractmethod
    def extract(self) -> pd.DataFrame:
        """Reads data from a source and returns a DataFrame."""
        pass

class IDataTransformer(ABC):
    """Interface for data transformation."""
    
    @abstractmethod
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Transforms the input DataFrame."""
        pass

class IDataLoader(ABC):
    """Interface for data loading."""
    
    @abstractmethod
    def load(self, df: pd.DataFrame, filename: str) -> None:
        """Saves the DataFrame to a destination."""
        pass
