import pandas as pd
from tqdm import tqdm
from typing import Dict
from typing import List

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
    
class ClassfierByPos:
  def __init__(self,
               target_df : pd.DataFrame,
               target_column : str,
               pos_dict : Dict):
    self.pos_dict = pos_dict
    self.target_column = target_column
    self.target_df = target_df

    self.result_dict = self.__make_empty_result_dict()
    self.table_dict = self.__make_table_dict()

  def classify_by_pos(self,
                      result_path : str) :
    for index, row in tqdm(enumerate(self.target_df[self.target_column]), desc="token csv.."):
      self.__classify_each(index, row)
    self.__save_data(result_path)

  def __make_empty_result_dict(self) -> Dict :
    result_dict = {}
    for key, value in self.pos_dict.items():
      result_dict[key] = []
    return result_dict

  def __make_table_dict(self) -> Dict :
    table_dict = {}
    for key, value in self.pos_dict.items():
      for pos in value :
        table_dict[pos] = key
    return table_dict

  def __classify_each(self, index : int, each_list : List) :
    for pos_token in each_list :
        key = self.table_dict.get(pos_token[1])
        self.result_dict.get(key).append((index, pos_token[0], pos_token[1]))

  def __save_data(self, result_path : str):
    try :
        for key, value in tqdm(self.result_dict.items(), desc="saving..."):
            if len(value) != 0 :
              self.__save_data_each(result_path, key, value)
    except Exception as fe:
        print('Something is wrong while saving data...')
        print(fe)

  def __save_data_each(self,
                       result_path : str,
                       key : str,
                       token_list : List[str]):
      token_list.sort(key = lambda x : x[0])
      df = pd.DataFrame(data=token_list, columns=['index', 'token', 'subpos'])
      df.to_csv(result_path+f'pos_{key}.csv', encoding='UTF-8-sig', index=False)
