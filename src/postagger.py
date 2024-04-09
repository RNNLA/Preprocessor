import pandas as pd
from utils import CSVLoader

from tqdm import tqdm
from typing import List
from typing import Tuple

class POSTagger:
  def __init__(self,
               data_path : str,
               target_column : str,
               removed_list : List[str]):
    self.data = CSVLoader.load_csv(data_path)
    self.target_column = target_column
    self.removed_list = removed_list
    self.tagged_data = None
    tqdm.pandas()

  def pos(self,
          POSmethod,
          inplace = False,
          *args,
          **kwargs) -> pd.DataFrame:

      def _pos(row : List[Tuple[str]], _removed_list : List[str], _POSmethod, *_args, **_kwargs) -> List[Tuple[str]] :
          sentence = _POSmethod(row, *_args, **_kwargs)
          return [(elem.replace(' ', ''), pos) for elem, pos in sentence[0] if pos not in _removed_list]

      self.data = self.data.dropna(axis=0, subset=[self.target_column])
      self.tagged_data = self.data.copy() if not inplace else self.data
      print('start progress pos_tagging')
      self.tagged_data[self.target_column] = self.tagged_data[self.target_column].progress_apply(_pos, args=(self.removed_list, POSmethod, args, kwargs))
      return self.tagged_data

  def save_csv(self,
               save_path : str) -> None :
      if self.tagged_data is not None :
        CSVLoader.save_csv(save_path, self.tagged_data)
      else:
        print('No data')