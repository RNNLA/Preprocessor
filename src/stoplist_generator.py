import pandas as pd
from tqdm import tqdm

from utils import CSVLoader

from collections import Counter
from itertools import chain
from typing import List
from typing import Set

class StoplistGenerator:
    def __init__(self,
                stopwords_path : str,
                stopwords_target : pd.DataFrame,
                stopwords_column : str,
                stopwords_target_column : str) :
        self.stopwords_path = stopwords_path
        self.stopwords_column = stopwords_column
        self.stopwords_target_column = stopwords_target_column

        self.stopwords_data = CSVLoader.load_csv(stopwords_path)
        self.stopwords_target = stopwords_target

        tqdm.pandas()

    def generate_stoplists(self,
                           threshold : int,
                           save_counter : bool = True) -> Set[str]:
        counted_df = self.__count_by_pos(save_counter)
        over_thr_df = counted_df.loc[counted_df['count'] > threshold]['pos']
        print('start progress over_thr_df')
        over_thr_df = over_thr_df.progress_apply(lambda x : x[0]).rename(self.stopwords_column).to_frame()
        over_thr_df = over_thr_df[~over_thr_df[self.stopwords_column].isin(['.', '기업', '미국'])]
        self.stopwords_data = pd.concat([self.stopwords_data, over_thr_df])[self.stopwords_column].drop_duplicates()
        return set(self.stopwords_data.to_list())

    def save_stoplists(self) :
        try :
          CSVLoader.save_csv(self.stopwords_path, self.stopwords_data)
        except Exception as e:
          print('Exception while save_stoplists in StopwordGenerator')
          print(self.stopwords_data)
          print(e)

    def __count_by_pos(self,
                       save_counter : bool) -> pd.DataFrame :
        target_df = self.stopwords_target.copy()
        print('Count each tokens...')
        df_to_list = list(target_df[self.stopwords_target_column].values)
        result = list(chain(*df_to_list))
        counter = Counter(result)
        counted_df = pd.DataFrame({'pos' : list(counter.keys()), 'count' : list(counter.values())})

        if save_counter : CSVLoader.save_csv('./tmp_count.csv', counted_df.sort_values(by=['count'], axis=0, ascending=False))
        return counted_df