# -*- coding: utf-8 -*-
"""
Created on Thu Dec 15 11:48:19 2022

@author: 82109
"""


# Dataframe에서 요리명 column의 데이터 문자열을 split 해 각 행을 여러 컬럼으로 나눈 후 병합하는 방법으로 구현
#================================================================================================

from tqdm import tqdm
import pandas as pd

# Data.csv는 나이스 급식식단정보 데이터 : 서울지역전체, 210101~211231 1년간의 급식데이터
df = pd.read_csv('C:/Users/82109/Desktop/nuvi_lab/Data.csv', index_col='Unnamed: 0')
df = df.reset_index(drop=True) 


columns = ['ATPT_OFCDC_SC_CODE', 'ATPT_OFCDC_SC_NM', 'SD_SCHUL_CODE', 'SCHUL_NM', 'MMEAL_SC_CODE', 
'MMEAL_SC_NM', 'MLSV_YMD', 'MLSV_FGR', 'DDISH_NM', 'ORPLC_INFO', 'CAL_INFO', 'NTR_INFO'] 
df = df[columns]


# 요리명 데이터 스플릿해서 다른 데이터 테이블에 넣어놓기
# 각 배열이 Series를 리턴하게 apply를 적용하면, Series -> DataFrame으로 변환할 수 있음.
df2 = df['DDISH_NM'].str.split('<br/>')
split = df2.apply(lambda x: pd.Series(x))

#stack() 으로 컬럼을 행으로 변환
#stack()을 실행하면, 위와 같이 멀티 인덱스를 가진 Series가 됨
# 알파벳 낱자만 가져오기 위해 인덱스를 초기화하고, 기준이 된 인덱스도 제거
# 이 결과는 Series이기 때문에, DataFrame으로 변환
# to_frame()이 파라미터로 컬럼명을 지정
# 원본 프레임에 left join으로 머지
split = split.stack().reset_index(level=1, drop=True).to_frame('nuvi_food')
df = df.merge(split, left_index=True, right_index=True, how='left')
df = df.reset_index(drop=True)

#컬럼 정리
df.drop(columns=('DDISH_NM'), inplace=True)
df.rename(columns={'nuvi_food' : 'DDISH_NM'}, inplace=True)
# 데이터 특수문자 제거
df['DDISH_NM'] = df['DDISH_NM'].replace('[^가-힣]', '', regex=True)


# ======================================================================================================

#다운로드 받은 데이터 csv 파일 read
df_nuvi_food = pd.read_csv('C:/Users/82109/Desktop/nuvi_lab/nuvi_food.csv')
df_main_categories = pd.read_csv('C:/Users/82109/Desktop/nuvi_lab/main_categories.csv')
df_sub_categories = pd.read_csv('C:/Users/82109/Desktop/nuvi_lab/sub_categories.csv')


#카테고리에 nan 값이 기입된 데이터 drop
condition  = df_nuvi_food[['nuvi_food_sub_category_id','nuvi_food_main_category_id']].dropna().index
df_nuvi_food = df_nuvi_food.iloc[condition]
df_nuvi_food = df_nuvi_food.reset_index(drop=True)

#nan값 드랍
df.dropna()
df = df.reset_index(drop=True)


# get_close_matches -> 가장 유사한 단어 뽑아주는 함수
# 기존에 이중 for문으로 돌렸던 이유는 difflib 라이브러리 안에 있는 이 함수를 사용해야했고
# df 데이터 프레임의 한 row에 모든 df_nuvi_food 데이터를 전부 유사도 비교를 해야했기 때문
# 하지만 해당 함수는 1 대 多 의 대응이 가능해서 하나의 for문으로 진행이 가능해서 우선 이렇게 진행
df['nuvi_food'] = 1       

from difflib import get_close_matches

for i in tqdm(df['nuvi_food'].index):
    # print(i)
    a = get_close_matches(df['DDISH_NM'][i], df_nuvi_food['food_name'], n=1)
    df['nuvi_food'][i] = a









