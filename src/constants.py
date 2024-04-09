pos_dict = {'Noun' : ['NNG', 'NNP', 'NNB', 'NR', 'NP'],  #순서대로 일반명사, 고유명사, 의존명사, 수사, 대명사
            'Verb' : ['VV', 'VA', 'VX', 'VCP', 'VCN'], #순서대로 동사, 형용사, 보조 용언, 긍정 지정사(이다), 부정 지정사(아니다)
            'Adjective' : ['MM'], #관형사
            'Adverb' : ['MAG', 'MAJ'], #일반 부사, 접속 부사
            'Interjection' : ['IC'], #감탄사
            'Josa' : ['JKS', 'JKC', 'JKG', 'JKO', 'JKB', 'JKV', 'JKQ', 'JX', 'JC'], #주격 조사, 보격 조사, 관형격 조사, 관형격 조사, 목적격 조사, 부사격 조사, 호격 조사, 인용격 조사, 보조사, 접속 조사.
            'Preeomi' : ['EP'], #선어말 어미
            'Eomi' : ['EF', 'EC', 'ETN', 'ETM'], #종결 어미, 연결 어미, 명사형 전성 어미, 관형형 전성 어미
            'Prefix' : ['XPN'], # 체언 접두사
            'Suffix' : ['XSN', 'XSV', 'XSA'], # 명사 파생 접미사, 동사 파생 접미사, 형용사 파생 접미사
            'Radix' : ['XR'], # 어근
            'Punctuation' : ['SF', 'SP', 'SS', 'SE', 'SO', 'SW'], # 마침표물음표 느낌표, 쉼표 가운뎃점 콜론 빗금, 따옴표 괄효표 줄표, 줄임표, 붙임표
            'Unknown' : ['NF', 'NV', 'NA'], #명사추정범주, 용언추정범주, 분석불능범주
            'NotKorean' : ['SL', 'SH', 'SN'] #외국어, 한자, 숫자
                }