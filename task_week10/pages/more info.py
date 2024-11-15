import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
from matplotlib import rc

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

with st.sidebar:
    st.write("공용 와이파이가 가장 늦게 설치되기 시작한 구는 어디일까요?")

data = pd.read_csv("publicwifi.csv")
st.title("지역구별 실내외에 공용와이파이 설치 현황을 살펴보자")


with st.form("input"):
    region = st.multiselect("지역구별(한 개만 선택하세요.)", data['자치구'].unique())
    submitted = st.form_submit_button("조회")
if submitted:
    filtered_data = data[data['자치구'].isin(region)]
    # 선택 항목 개수 제한
    if len(region) != 1:
        st.error("지역구는 한 개만 선택할 수 있습니다. 다시 선택해주세요.")
    else:
        selected_region = region[0]  # 선택된 지역구 가져오기
        st.write(f"선택한 지역구: {selected_region}")

    for selected_region in region:
        st.subheader(f"{selected_region}의 실내외 공용와이파이 설치 현황")

    # 해당 지역구 데이터 필터링
    region_data = filtered_data[filtered_data['자치구'] == selected_region]

    # 실내외 구분별 데이터 계산
    indoor_outdoor_counts = region_data['실내외구분'].value_counts()

    # 그래프 1: 실내외 구분별 데이터
    fig, ax = plt.subplots()
    indoor_outdoor_counts.plot(kind='bar', ax=ax, color = 'pink')
    ax.set_title(f"{selected_region} 실내외 구분별 와이파이 설치 현황")
    ax.set_xlabel("실내외구분")
    ax.set_ylabel("설치 개수")
    st.pyplot(fig)

    # 연도별 데이터 계산
    year_counts = region_data.groupby(['설치년도', '실내외구분']).size().unstack(fill_value=0)

    # 그래프 2: 연도별 다중 막대 그래프
    fig, ax = plt.subplots(figsize=(10, 6))
    year_counts.plot(kind='bar', ax=ax)
    ax.set_title(f"{selected_region} 연도별 실내외 구분 와이파이 설치 현황")
    ax.set_xlabel("설치년도")
    ax.set_ylabel("설치 개수")
    ax.legend(title="실내외구분")
    st.pyplot(fig)

else:
    st.write("조회할 지역구를 선택해주세요.")