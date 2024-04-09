from tqdm import tqdm
import pandas as pd
import numpy as np
import json
import re


class ArticleCleaner():
  def __init__(
      self, 
      target_data_path:str, 
      regex_data_paths:str,
      target_data_col_name:str, 
      save_path:str = 'result.csv',
      repl_patterns:list = [r' \1', ' '],
      debug:bool = False
  ) -> None:
    self.debug = debug,
    self.repl_patterns = repl_patterns
    self.target_data_col_name = target_data_col_name
    self.target_data = self.__load_target_data(target_data_path)
    self.save_path = save_path
    self.__regexs_sets = [self.__load_regex_data(regex_data_path) for regex_data_path in regex_data_paths]
  
  def run(self):
    self.__run_each()
    self.__save_target_data()

  def __run_each(self):
    self.__convert_data_str_type()
    i = 0
    for regex_set, repl_pattern in zip(self.__regexs_sets, self.repl_patterns):
      for regex in tqdm(regex_set, desc=f'{i+1}nd task cleaning'):
        self.__clean_data_using_regex(r'' + regex, repl_pattern)
      self.__clean_data_spaces()
      i += 1
    self.target_data.replace('', np.nan, inplace=True)
    self.target_data.dropna(inplace=True)

  def __load_target_data(self, path: str):  
    return pd.read_csv(path, encoding='UTF-8-sig')
  
  def __load_regex_data(self, path: str):
    return json.load(open(path))
  
  def __save_target_data(self):
    self.target_data.to_csv(self.save_path, encoding='UTF-8-sig', index=False)
    if self.debug: self.target_data[self.target_data_col_name].to_csv(
      f'{self.save_path.split(".csv")[0]}-DEBUG.csv', encoding='UTF-8-sig', index=False
    )
  def __convert_data_str_type(self):
    self.target_data = self.target_data.astype(str)

  def __clean_data_using_regex(self, pattern: re.Pattern, repl_pattern: re.Pattern|str):
    self.target_data[self.target_data_col_name] = self.target_data[self.target_data_col_name].apply(lambda x: re.sub(pattern, repl_pattern, x))
  
  def __clean_data_spaces(self):
    self.target_data[self.target_data_col_name] = self.target_data[self.target_data_col_name].apply(lambda x: ' '.join(x.split())) 

if __name__ == '__main__':
    ac_first = ArticleCleaner(
      target_data_path='../../Data/news_data-1016-TFIDF.csv',
      regex_data_paths=['./regex-dot.json', './regex-zip.json'],
      target_data_col_name='content',
      repl_patterns=[r' \1', ' '],
      save_path='./result.csv',
      debug=True
    )
    ac_first.run()
