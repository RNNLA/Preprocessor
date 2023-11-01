import pandas as pd
from utils import CSVLoader

from typing import List
from typing import Tuple
from typing import Set

class StoplistGenerator:
    def __init__(self,
                stopwords_path : str,
                stopwords_data : pd.DataFrame,
                stopwords_column : str,
                stopwords_data_column : str,
                unused_pos_list : List[str]) :
        self.stopwords_path = stopwords_path
        self.stopwords_column = stopwords_column
        self.stopwords_data_column = stopwords_data_column
        self.unused_pos_list = unused_pos_list

        self.stopwords_list = set(CSVLoader.load_csv(stopwords_path, self)[stopwords_column].to_list())
        self.stopwords_data = stopwords_data

        self.pos_list = []

    def generate_stoplists(self) -> Set[str]:
        return self.__pos()

    def save_stoplists(self) :
        try :
          df = pd.DataFrame(list(self.stopwords_list), columns = [self.stopwords_column])
          CSVLoader.save_csv(self.stopwords_path, df, self)
        except Exception as e:
          print('Exception while save_stoplists in StopwordGenerator')
          print(e)

    #temporary method for POS selection
    # def tagged_df(self) -> List :
    #     return [[elem] for elem in self.pos_list]

    def __pos(self) -> List :
        for tagged_sentences in tqdm(self.stopwords_data[self.stopwords_data_column], desc="Adding Stopwords...") :
            # self.pos_list.append(tagged_sentences)#temporary statement for POS Selection
            self.__add_stopword_by_pos(tagged_sentences)
        return list(self.stopwords_list)


    def __add_stopword_by_pos(self,
                              tagged_sentences : List[str]) :
        for elem, pos in tagged_sentences :
            if pos in self.unused_pos_list :
              self.stopwords_list.add(elem)