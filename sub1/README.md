# Pandas 기본 명령어

## 데이터 프레임 생성, 접근 삭제

### DataFrame 생성

```python
my_2darray = np.array([[1, 2, 3], [4, 5, 6]])
display(pd.DataFrame(my_2darray))

# Take a dictionary as input to your DataFrame 
my_dict = {"a": ['1', '3'], "b": ['1', '2'], "c": ['2', '4']}

# Take a DataFrame as input to your DataFrame 
my_df = pd.DataFrame(data=[4,5,6,7], index=range(0,4), columns=['A'])

# Take a Series as input to your DataFrame
my_series = pd.Series({"United Kingdom":"London", "India":"New Delhi", "United States":"Washington", "Belgium":"Brussels"})
```

### DataFrame 접근

```python
df = pd.DataFrame({"A":[1,4,7], "B":[2,5,8], "C":[3,6,9]})

# Use `iloc[]` to select a row
df.iloc[0]
df.loc[0]
df.ix[0] 

# Use `loc[]` to select a column
df.loc[:,'A']
df['A']

# 특정 row, column을 선택하기
df.ix[0]['A'] # 1
df.loc[0]['B'] # 2
```

* loc :  integer positon를 통해 값을 찾을 수 있다. label로는 찾을 수 없다 
* iloc :  label 을 통해 값을 찾을 수 있다. integer position로는 찾을 수 없다.
* ix : integer position과 label모두 사용 할 수 있다. 만약 label이 숫자라면 label-based index만 된다.

### DataFrame 추가/삭제

#### 인덱스 설정

```python
# Print out your DataFrame `df` to check it out
display(df)

# Set 'C' as the index of your DataFrame
df = df.set_index('A')
```

#### Row 추가

```python
df = pd.DataFrame(data=np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]), index= [2.5, 12.6, 4.8], columns=[48, 49, 50])

# There's no index labeled `2`, so you will change the index at position `2`
df.ix[2] = [60, 50, 40]

# This will make an index labeled `2` and add the new values
df.loc[2] = [11, 12, 13]
```

```python
df = pd.DataFrame(data=np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]), columns=[48, 49, 50])
a = pd.DataFrame(data=[[1,2,3]], columns=[48,49,50])

df = df.append(a)
df = df.reset_index(drop=True)
```

#### Column 추가

```python
df = pd.DataFrame(data=np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]), columns=['A', 'B', 'C'])

# Append a column to `df`
df.loc[:, 'D'] = pd.Series(['5', '6', '7'], index=df.index)

# Print out `df` again to see the changes
df['E'] = pd.Series(['5', '6', '7'], index=df.index)
```



#### 인덱스 삭제

```python
df = df.reset_index(drop=True)
```

#### Row 삭제

```python
df = pd.DataFrame(data=np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]), columns=['A', 'B', 'C'])
display(df)

# Drop the column with label 'A'              
# drop axis의 경우 column이면 1, row이면 0이다.
df.drop(0, axis=0, inplace=True)
```

* inplace 옵션을 통해 대체할지 안할지 결정

```python
df = pd.DataFrame(data=np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9], [40, 50, 60], [23, 35, 37]]), index= [2.5, 12.6, 4.8, 4.8, 2.5], columns=[48, 49, 50])
df = df.reset_index()
df = df.drop_duplicates(subset='index', keep='last').set_index('index')
```

* 중복 로우 삭제시 사용 keep 옵션을 통해 어떤것을 킵할지 정할 수 있음

```python
df = pd.DataFrame(data=np.array([[1, 2, 3], [1, 5, 6], [7, 8, 9]]), columns=['A', 'B', 'C'])
# Drop the index at position 1
df.index[1]
df.drop(df.index[1])
df.drop(0)
```

* index메소드는 해당 위치에 있는 인덱스를 받아오는것
* drop메소드를 통해 해당 인덱스를 삭제

#### Column 삭제

```python
df = pd.DataFrame(data=np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]), columns=['A', 'B', 'C'])
display(df)

# Drop the column with label 'A'              
# drop axis의 경우 column이면 1, row이면 0이다.
df.drop('A', axis=1, inplace=True)
```

* inplace 옵션을 통해 대체할지 안할지 결정

## 데이터 프레임 병합

> Pandas는 두 개 이상의 데이터프레임을 하나로 합치는 데이터 병합(merge)이나 연결(concatenate)을 지원한다. 

```python
pd.merge(df1, df2) # inner join
pd.merge(df1, df2, how="outer") # outer join
```

* inner join :  양쪽 데이터프레임에 모두 키가 존재하는 데이터만 보여줌
* outer join :   키 값이 한쪽에만 있어도 데이터를 보여줌
* 테이블에 키 값이 같은 데이터가 여러개 있는 경우, 있을 수 있는 모든 경우의 수를 따져서 조합을 만들어냄
* 기준 열이 아니면서 이름이 같은 열에는 `_x` 또는 `_y` 와 같은 접미사가 붙음

```python
pd.merge(df1, df2, how='left')
pd.merge(df1, df2, how='right')
```

* left, right 방식은 각각 첫번째, 혹은 두번째 데이터프레임의 키 값을 모두 보여줌

```python
pd.merge(df1, df2, left_on='이름', right_on="성명")
```

* 키가 되는 기준열의 이름이 두 데이터프레임에서 다르다면 `left_on`, `right_on` 인수를 사용하여 기준열을 명시

## 데이터 분석용 통계함수

| 함수           | 설명                                                    |
| -------------- | ------------------------------------------------------- |
| count          | 전체성분의 (NaN이 아닌) 값의 개수 계산                  |
| min, max       | 전체 성분의 최소, 최대값 계산                           |
| argmin, argmax | 전체 성분의 최소값, 최댓값이 위치한 (정수)인덱스를 반환 |
| idxmin, idxmax | 전체 인덱스 중 최솟값, 최댓값을 반환                    |
| quantile       | 전체 성분의 특정 사분위 수에 해당하는 값을 반환         |
| sum            | 전체 성분의 합을 계산                                   |
| mean           | 전체 성분의 평균을 계산                                 |
| median         | 전체 성분의 중간값을 반환                               |
| mad            | 전체성분의 평균값으로부터 절대 편차의 평균을 계산       |
| std, var       | 전체 성분의 표준편차, 분산을 계산                       |
| cumsum         | 맨 첫 번째 성분부터 각 성분까지의 누적합을 계산         |
| sumprod        | 맨 첫 번째 성분부터 각 성분까지의 누적곱을 계산         |

* axis=0 : 행 방향(default)
* axis=1 : 열 방향

## index 기준 정렬

```python
df.sort_values(by="칼럼명")
df.sort_values(by=["칼럼1", "칼럼2"])
```

## IF문

```python
df2 = df1[df1["칼럼명"]=="값"]
```

## For문

```python
# iterrows()
for i, store in df1.iterrows():
    print(i, store[col])
```

```python
# loc
for i in df1.index:
    print(df1.loc[i, col])
```

```python
# get_value(), set_value()
for i in df1.index:
    print(df1.get_value(i, col))
```

