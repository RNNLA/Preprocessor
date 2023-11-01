import pandas as pd
from tqdm import tqdm
from typing import List
from typing import Tuple

class CSVLoader:
  def __init__(self):
    print(type(self))
    print(self.__class__.__name__)
    pass

  @classmethod
  def load_csv(cls,
               path : str,
               preproc_obj : object) -> pd.DataFrame:
    try :
        df = pd.read_csv(path, encoding = 'UTF-8-sig').dropna(axis=0)
        return df
    except Exception as e:
        print(f'Error of path {path} in class {preproc_obj.__class__.__name__}')
        raise e

  @classmethod
  def save_csv(clas,
               path : str,
               file : pd.DataFrame,
               preproc_obj : object) -> None:
    try :
        file.dropna(axis = 0)
        file.to_csv(path, encoding='UTF-8-sig', index=False)
    except Exception as e:
        print(f'Error of path {path} in class {preproc_obj.__class__.__name__}')
        raise e
    
class POSTagger:
  def __init__(self,
               data_path : str,
               target_column : str,
               removed_list : List[Tuple[str]]):
    self.data = CSVLoader.load_csv(data_path, self)
    self.target_column = target_column
    self.removed_list = removed_list
    self.tagged_data = None

  def pos(self,
          POSmethod,
          *args,
          **kwargs) -> pd.DataFrame:
      pos_list = []
      for row in tqdm(self.data[self.target_column], desc="POS Tagging...") :
        sentence = POSmethod(row, *args, **kwargs)
        data = [[(self.__data_process(elem), pos) for elem, pos in sentence if pos not in self.removed_list]]
        pos_list.append(data)
      df = pd.DataFrame(pos_list, columns=[self.target_column])
      return df

  def save_csv(self,
               save_path : str) -> None :
      if self.tagged_data is not None :
        CSVLoader.save_csv(save_path, self.tagged_data, self)
      else:
        print('No data')

  def __data_process(self,
                     word : str):
      if word == '!' : return word.replace('!', '.')
      elif word == '?' : return word.replace('?', '.')