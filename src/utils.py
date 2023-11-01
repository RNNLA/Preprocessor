import pandas as pd

class CSVLoader:
  def __init__(self):
    pass

  @classmethod
  def load_csv(cls,
               path : str) -> pd.DataFrame:
    try :
        df = pd.read_csv(path, encoding = 'UTF-8-sig').dropna(axis=0)
        return df
    except Exception as e:
        print(f'Error of path {path}')
        raise e

  @classmethod
  def save_csv(clas,
               path : str,
               file : pd.DataFrame) -> None:
    try :
        file.dropna(axis = 0)
        file.to_csv(path, encoding='UTF-8-sig', index=False)
    except Exception as e:
        print(f'Error of path {path}')
        raise e
    
