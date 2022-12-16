# menu

## 나이스에서 수집한 '급식식단정보' 데이터 전처리

해당 repository 에 업로드 된 코드의 목적은
1. 수집된 데이터를 '음식명' 데이터를 각 메뉴별로 **새로운 row 데이터로 생성해서 메뉴별 데이터 셋 만들기**
2. 누비랩에서 제공한 nuvi_food 데이터를 활용해 **각각의 row를 nuvi_food 데이터에 기입된 'food_name' 별로 매칭**
---

1) 음식명의 데이터를 스플릿한 리스트 데이터로 다른 데이터 프레임 생성 -> 목적에 맞게 변형 한 후 원래 데이터 프레임과 merge
```python
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
```

2) python 의 라이브러리중 difflib의 get_close_matches 함수 이용 -> 하나의 단어와 많은 단어들 간의 유사도를 측정하여 그 중 가장 유사한 단어를 반환 받을 수 있는 함수.

df['DDISH_NM']<-(요리명 column명)과 df_nuvi_food['food_name']을 1 대 多 로 비교 하여 **가장 유사한 단어 하나 반환 df['nuvi_food'] 에 입력.**
```python 

from difflib import get_close_matches

for i in tqdm(df['nuvi_food'].index):
    # print(i)
    a = get_close_matches(df['DDISH_NM'][i], df_nuvi_food['food_name'], n=1)
    df['nuvi_food'][i] = a

```
