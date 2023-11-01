import pandas as pd
from utils import CSVLoader

from tqdm import tqdm
from typing import List

class POSTagger:
  def __init__(self,
               data_path : str,
               target_column : str,
               removed_list : List[str]):
    self.data = CSVLoader.load_csv(data_path)
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
        CSVLoader.save_csv(save_path, self.tagged_data)
      else:
        print('No data')

  def __data_process(self,
                     word : str):
      if word == '!' : return word.replace('!', '.')
      elif word == '?' : return word.replace('?', '.')