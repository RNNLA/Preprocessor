import pandas as pd
from tqdm import tqdm
from konlpy.tag import Komoran

from postagger import POSTagger
from remover import Remover
from stoplist_generator import StoplistGenerator
from utils import ClassfierByPos
from constants import pos_dict


if __name__ == '__main__':
    # cleaning_target_path = './news_data-1016.csv'
    # cleaning_target_path = './practice_data_raw_2.csv'
    cleaning_target_path = './Labeled_news_data-1016-TFIDF.csv'
    tokenize_target_path = './data_cleaned.csv'
    stopwords_path = './stopwords_corpus.csv'
    target_col_name = 'content'
    stopwords_col_name = 'removal_list'
    removed_pos_list = ['SP', 'SS', 'SE', 'SO', 'SW', #쉼표 가운뎃점 콜론 빗금, 따옴표 괄효표 줄표, 줄임표, 붙임표
                        'EF', 'EC', 'ETN', 'ETM', 'EP', #종결 어미, 연결 어미, 명사형 전성 어미, 관형형 전성 어미, 선어말 어미
                        'XPN', 'XSN', 'XSV', 'XSA', #체언 접두사, 명사 파생 접미사, 동사 파생 접미사, 형용사 파생 접미사
                        'JKS', 'JKC', 'JKG', 'JKO', 'JKB', 'JKV', 'JKQ', 'JX', 'JC',  #주격 조사, 보격 조사, 관형격 조사, 관형격 조사, 목적격 조사, 부사격 조사, 호격 조사, 인용격 조사, 보조사, 접속 조사.
                        'MAJ', #접속 부사
                        'NNB', 'NR', 'NP', #의존명사, 수사, 대명사
                        'VX', 'VCP', 'VCN', #보조 용언, 긍정 지정사(이다), 부정 지정사(아니다)
                        'IC', #감탄사
                        'NF', 'NV'
                        ]
    """
    쓰고 있는 품사
    ['NNG', 'NNP'], #일반명사, 고유명사,
    ['VV', 'VA',] #순서대로 동사, 형용사,
    ['MM'], #관형사
    ['MAG'], #일반 부사
    ['XR'], # 어근
    ['NF', 'NV', 'NA'], #명사추정범주, 용언추정범주, 분석불능범주
    ['SL', 'SN'] #외국어, 한자, 숫자
    """
    pos_df_path = './pos_df.csv'
    pos_df_stopwords_removed_path = './pos_df_stopwords_removed.csv'
    preproc_final_path = './preproc_final.csv'
    tqdm.pandas()

    ac = ArticleCleaner(
                        target_data_path=cleaning_target_path,
                        regex_data_paths=['./regex-sf.json','./regex-dot.json', './regex-zip.json','./regex-number.json'],
                        target_data_col_name='content',
                        repl_patterns=['.', r' \1', '', '숫'],
                        save_path=tokenize_target_path,
                        debug=False
                        )
    ac.run()



    tagger = POSTagger(data_path=tokenize_target_path,
                    target_column = target_col_name,
                    removed_list = removed_pos_list)
    tagged_data = tagger.pos(Komoran(userdic='./user_dict.txt').pos)
    tagger.save_csv(pos_df_path)

    ##Use this statement when program dies in middle.
    # tagged_data = CSVLoader.load_csv(pos_df_path)
    # tagged_data['content'] = tagged_data['content'].progress_apply(lambda x : ast.literal_eval(x))

    swr = StoplistGenerator(stopwords_path = stopwords_path,
                            stopwords_target = tagged_data,
                            stopwords_column = stopwords_col_name,
                            stopwords_target_column = target_col_name)

    stoplist = swr.generate_stoplists(threshold = 41000,
                                      save_counter = True)
    swr.save_stoplists()

    # ######### if error, use these statements!#######
    # # tagged_data = CSVLoader.load_csv(pos_df_path)
    # # tagged_data['content'] = tagged_data['content'].apply(lambda x : eval(x))
    # # stoplist = CSVLoader.load_csv(stopwords_path)
    # # ################################################



    remover = Remover(target_col_name = target_col_name,
                      target_data = tagged_data,
                      stoplist = stoplist)
    remover.remove(also_as_pos = True)
    remover.save_data(preproc_final_path)
    remover.save_data(pos_df_stopwords_removed_path, as_pos = True)
    tagged_data = remover.get_pos_df()


    cbp = ClassfierByPos(target_df = tagged_data,
                              target_column = target_col_name,
                              pos_dict = pos_dict)
    cbp.classify_by_pos('./')