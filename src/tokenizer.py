from abc import *
import pandas as pd

from tqdm import tqdm
from typing import Union
from typing import List
from typing import Set

class BaseTokenizer(metaclass = ABCMeta) :
    def __init__(self,
                 target_col_name: str,
                 target_data : pd.DataFrame):
        self.target_col_name = target_col_name
        self.target_data = target_data
        self.tokenized_col = []

    @abstractmethod
    def tokenize(self,
                 debug : bool,
                 remove_stopwords : bool,
                 tokenize_option : int) -> Union[List[str], pd.DataFrame] :
        pass

    def get_complete_data(self) -> pd.DataFrame :
        if len(self.tokenized_col) == 0 :
            raise Exception('Please Do Tokenizing Frist')
        columns = [self.target_col_name, 'label']
        data = [[self.tokenized_col[i], i] for i in range(len(self.tokenized_col))]
        data = pd.DataFrame(data=data, columns=columns)
        data = self.__padding(data)
        return data

    def get_tokenized_col(self) -> List[str]  :
        return self.tokenized_col

    def set_target_col_name(self, target_col_name : str) :
        self.target_col_name = target_col_name

    def __padding(self, data) -> pd.DataFrame :
        max_len = data[self.target_col_name].apply(lambda x : len(x)).max()
        data[self.target_col_name] = data[self.target_col_name].apply(lambda x : x + ['0' for i in range(max_len - len(x))])
        return data
    
class KomoranTokenizer(BaseTokenizer):
    def __init__(self,
                 target_col_name : str,
                 target_data : pd.DataFrame,
                 stoplist : Set[str]):
        super().__init__(target_col_name, target_data)
        self.stoplist = stoplist
        self.still_pos_list = []
        self.still_tagged_sentences = []

    def tokenize(self,
                 debug : bool = False,
                 remove_stopwords : bool = False) -> Union[List[str], pd.DataFrame] :
        self.tokenized_col = []
        desc = 'Tokenizing' + (' & Removing Stopwords' if remove_stopwords else '')
        self.__tokenize_each(debug, remove_stopwords, desc)
        return self.get_complete_data()

    def get_pos_df(self):
        df = self.target_data.copy()
        df[self.target_col_name] = self.still_pos_list
        return df

    def __tokenize_each(self,
                        debug : bool,
                       remove_stopwords : bool,
                       desc : str) :
        for row in tqdm(self.target_data[self.target_col_name], desc=desc) :
            tokenized_sentences = [elem for elem, pos in row]
            self.still_tagged_sentences = [elem for elem in row] if debug else [] # refactor!
            if remove_stopwords :
              tokenized_sentences = self.__remove_words(tokenized_sentences, debug)
            self.tokenized_col.append(tokenized_sentences)
            if debug :
              self.still_pos_list.append(self.still_tagged_sentences) #refactor!

    def __remove_words(self,
                        tokenized_sentences : List[str],
                        debug : bool) -> List[str]:
        tokenized_sentences.replace('?', '.')
        tokenized_sentences.replace('!', '.')
        result = [word for word in tokenized_sentences if (word not in self.stoplist and (len(word) > 1 or word == '.') ) ]
        if debug :
          self.still_tagged_sentences = [(word, pos) for word, pos in self.still_tagged_sentences if word in result] #refactor!
        return result