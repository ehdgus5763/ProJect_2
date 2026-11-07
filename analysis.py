서울 따릉이 자치구별 이용 현황 분석

SQL(queries.sql)과 같은 기준으로 자치구별 집계를 pandas에서 다시 계산하고,
총 대여건수와 대여소당 대여건수를 나란히 시각화한다.

import os

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 그래프의 한글 폰트 설정 (Windows 기준). 파일 인코딩과는 별개의 설정이다.
plt.rc('font', family='Malgun Gothic')
plt.rcParams['axes.unicode_minus'] = False

# 1. 데이터 불러오기
# 원본 CSV가 cp949로 저장되어 있어 utf-8로 읽으면 에러가 난다.
df = pd.read_csv('ddareung_db.csv', encoding='cp949')
print(df.head())

# 2. 자치구별 집계 (queries.sql의 1번 쿼리와 같은 기준)
summary = (
    df.groupby('자치구')
      .agg(대여소수=('대여소명', 'nunique'),
           대여건수=('대여건수', 'sum'),
           반납건수=('반납건수', 'sum'))
      .reset_index()
)
summary['대여소당_대여건수'] = (summary['대여건수'] / summary['대여소수']).round(1)

# 3. 상위·하위 5개 자치구 확인
by_total = summary.sort_values('대여건수', ascending=False)
by_per_station = summary.sort_values('대여소당_대여건수', ascending=False)

print('\n[총 대여건수 상위 5]')
print(by_total.head(5))
print('\n[총 대여건수 하위 5]')
print(by_total.tail(5))
print('\n[대여소당 대여건수 상위 5]')
print(by_per_station.head(5))
print('\n[대여소당 대여건수 하위 5]')
print(by_per_station.tail(5))

# 4. 대여소 수와 총 대여건수의 상관계수
print('\n대여소 수와 총 대여건수의 상관계수:',
      round(summary['대여소수'].corr(summary['대여건수']), 3))

# 5. 시각화: 총 대여건수 vs 대여소당 대여건수 (전체 자치구)
fig, axes = plt.subplots(1, 2, figsize=(16, 9))
panels = [
    (axes[0], by_total, '대여건수', '자치구별 총 대여건수'),
    (axes[1], by_per_station, '대여소당_대여건수', '자치구별 대여소당 대여건수'),
]
for ax, data, col, title in panels:
    sns.barplot(data=data, x=col, y='자치구', color='#4C72B0', ax=ax)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_xlabel(col)
    ax.set_ylabel('')
    ax.grid(axis='x', linestyle='--', alpha=0.6)

plt.tight_layout()

os.makedirs('images', exist_ok=True)
plt.savefig('images/ddareung_usage.png', dpi=150, bbox_inches='tight')
plt.show()
