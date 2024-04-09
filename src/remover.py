from abc import *
import pandas as pd
from tqdm import tqdm

from utils import CSVLoader
from typing import Tuple
from typing import List
from typing import Set

class Remover:
    def __init__(self,
                 target_col_name : str,
                 target_data : pd.DataFrame,
                 stoplist : Set[str]):
        self.target_col_name = target_col_name
        self.target_data = target_data
        self.removed_data = None
        self.stoplist = stoplist
        self.still_tagged_sentences = []

        tqdm.pandas()

    def remove(self,
              also_as_pos : bool = False) -> None :
        def __remove_each(row : List[Tuple[str]], _also_as_pos : bool, self : Remover) -> List[str] :
              new_list = []
              pos_list = []
              for elem, pos in row :
                if elem in self.stoplist : continue
                elif (len(elem) == 1) and ('a' <= elem.lower() <= 'z') : continue   # Use this condition if one-length word turns out to be stopwords
                new_list.append(elem)
                if _also_as_pos : pos_list.append((elem, pos))

              if _also_as_pos : self.still_tagged_sentences.append(pos_list)
              return new_list

        self.removed_data = self.target_data.copy()
        print('start remove stopwords')
        self.removed_data[self.target_col_name] = self.removed_data[self.target_col_name].progress_apply(__remove_each, args=(also_as_pos, self))

    def get_pos_df(self) -> pd.DataFrame:
        df = self.removed_data.copy()
        df[self.target_col_name] = self.still_tagged_sentences
        return df

    def get_complete_data(self) -> pd.DataFrame :
        df = self.__padding()
        return df

    def save_data(self, path : str, as_pos : bool = False) -> None:
        try :
          if as_pos :
            CSVLoader.save_csv(path, self.get_pos_df())
          elif not as_pos and self.removed_data is not None :
            CSVLoader.save_csv(path, self.get_complete_data())
          else :
            raise Exception('No Proper Data')
        except Exception as e:
          print(f'Exception while saving {"pos-tagged " if as_pos else ""}data in Remover')
          print(e)

    def __padding(self) -> pd.DataFrame :
        data = self.removed_data
        max_len = data[self.target_col_name].apply(lambda x : len(x)).max()
        data[self.target_col_name] = data[self.target_col_name].apply(lambda x : x + ['0' for i in range(max_len - len(x))])
        return data