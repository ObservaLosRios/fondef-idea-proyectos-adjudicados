import pandas as pd
import numpy as np
from .interfaces import IDataTransformer

class Fondef2000Transformer(IDataTransformer):
    """Transformer for the 2000-2011 dataset."""
    
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        print("Transforming Fondef 2000-2011 dataset...")
        df = df.copy()
        
        # The CSV might have been read with the wrong header because of the first 3 lines
        # But since we passed header=3 in extract (planned), we assume columns are correct-ish.
        # Let's standardize column names
        
        # Map columns to standard schema
        rename_map = {
            'CODIGO': 'project_code',
            'AÑO CONCURSO': 'year',
            'TITULO': 'title',
            'DIRECTOR GENERAL': 'director',
            'MONTO ADJ. FONDEF': 'amount',
            'FECHA INICIO': 'start_date',
            'FECHA TERMINO': 'end_date'
        }
        
        df = df.rename(columns=rename_map)
        
        # Combine keywords
        keyword_cols = ['PALABRA CLAVE 1', 'PALABRA CLAVE 2', 'PALABRA CLAVE 3']
        # Fill NaNs with empty string before joining
        df['keywords'] = df[keyword_cols].fillna('').apply(
            lambda x: ', '.join([str(val).strip() for val in x if str(val).strip() != '']), axis=1
        )
        
        # Add missing columns present in target schema
        # Infer area from keywords
        df['area'] = df.apply(self._infer_area, axis=1)
        
        # Select and reorder columns
        target_cols = ['project_code', 'year', 'title', 'director', 'keywords', 'amount', 'area', 'start_date', 'end_date']
        # Ensure all target cols exist
        for col in target_cols:
            if col not in df.columns:
                df[col] = np.nan
                
        return df[target_cols]

    def _infer_area(self, row):
        text = (str(row.get('keywords', '')) + ' ' + str(row.get('title', ''))).lower()
        
        AREA_KEYWORDS = {
            'Agropecuaria': ['agro', 'fruta', 'cultivo', 'suelo', 'riego', 'plaga', 'vino', 'vid', 'ganado', 'leche', 'bovino', 'ovino', 'agricola', 'veterinaria', 'hortaliza', 'cereal'],
            'Pesca y Acuicultura': ['pesca', 'acuicultura', 'salmon', 'trucha', 'alga', 'marino', 'pez', 'peces', 'bentonico', 'molusco', 'chorito', 'ostion'],
            'Salud': ['salud', 'medicina', 'clinica', 'paciente', 'enfermedad', 'virus', 'bacteria', 'cancer', 'terapia', 'farmaco', 'vacuna', 'biomed', 'hospital'],
            'Minería': ['mineria', 'cobre', 'mineral', 'lixiviacion', 'flotacion', 'relave', 'geologia', 'metalurgia', 'minero'],
            'Forestal': ['forestal', 'bosque', 'madera', 'pino', 'eucalipto', 'celulosa', 'papel', 'arbol', 'silvicultura'],
            'TIC': ['software', 'informatica', 'computacion', 'internet', 'web', 'datos', 'inteligencia', 'digital', 'sistema experto', 'redes', 'tic', 'tecnologia de informacion'],
            'Educación': ['educacion', 'escolar', 'aprendizaje', 'pedagogia', 'didactica', 'aula', 'docente', 'colegio', 'enseñanza'],
            'Energía': ['energia', 'solar', 'eolico', 'biocombustible', 'electrico', 'generacion', 'eficiencia energetica', 'fotovoltaico'],
            'Infraestructura': ['construccion', 'hormigon', 'cemento', 'vivienda', 'pavimento', 'estructuras', 'sismico', 'vial', 'edificio'],
            'Manufactura': ['manufactura', 'proceso', 'industrial', 'materiales', 'polimero', 'plastico', 'envase'],
            'Alimentos': ['alimento', 'nutricion', 'dieta', 'funcional', 'antioxidante', 'proteina', 'gastronomia']
        }
        
        for area, keywords in AREA_KEYWORDS.items():
            for kw in keywords:
                if kw in text:
                    return area
        return 'Otros'

class Fondef2012Transformer(IDataTransformer):
    """Transformer for the 2012-2017 dataset."""
    
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        print("Transforming Fondef 2012-2017 dataset...")
        df = df.copy()
        
        # Map columns
        rename_map = {
            'Código': 'project_code',
            'Concurso': 'contest_name', # This contains year info usually
            'Título': 'title',
            'Director General': 'director',
            'Área ': 'area'
        }
        
        df = df.rename(columns=rename_map)
        
        # Extract year from project_code
        # Format: ID14... -> 2014, CA12... -> 2012
        def extract_year(code):
            try:
                if pd.isna(code): return np.nan
                year_str = str(code)[2:4]
                if year_str.isdigit():
                    return 2000 + int(year_str)
                return np.nan
            except:
                return np.nan
                
        df['year'] = df['project_code'].apply(extract_year)
        
        df['keywords'] = np.nan
        df['amount'] = np.nan
        df['start_date'] = np.nan
        df['end_date'] = np.nan
        
        target_cols = ['project_code', 'year', 'title', 'director', 'keywords', 'amount', 'area', 'start_date', 'end_date']
        return df[target_cols]

class CleaningTransformer(IDataTransformer):
    """General cleaning transformer."""
    
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        print("Applying general cleaning...")
        df = df.copy()
        
        # Clean strings
        str_cols = ['project_code', 'title', 'director', 'area', 'keywords']
        for col in str_cols:
            if col in df.columns:
                df[col] = df[col].astype(str).str.strip().str.title()
                df[col] = df[col].replace('Nan', np.nan)
                df[col] = df[col].replace('Nat', np.nan) # pandas sometimes converts NaN to 'nan' string
        
        # Clean amount
        # Remove dots used as thousand separators (e.g. 150.000 -> 150000)
        if 'amount' in df.columns:
            df['amount'] = df['amount'].astype(str).str.replace('.', '', regex=False)
            df['amount'] = pd.to_numeric(df['amount'], errors='coerce').fillna(0)
            
        # Clean year
        if 'year' in df.columns:
            df['year'] = pd.to_numeric(df['year'], errors='coerce').fillna(0).astype(int)
            
        # Drop duplicates and invalid rows
        df = df.dropna(subset=['project_code'])
        df = df[df['year'] > 1990] # Filter out 0 and invalid years
        df = df.drop_duplicates(subset=['project_code'], keep='first')
        
        return df
