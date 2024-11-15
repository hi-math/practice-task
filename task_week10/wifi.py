import streamlit as st
import pandas as pd
import pydeck as pdk

with st.sidebar:
    st.image("image.png", caption="서울의 공공와이파이", use_container_width=True)

data = pd.read_csv("publicwifi.csv")

data = data.rename(columns={'Y좌표': 'lat', 'X좌표': 'lon'})
data['color'] = data['실내외구분'].map({'실내': [0, 0, 250], '실외': [255, 200, 0]})
data['radius'] = data['실내외구분'].map({'실내': 30, '실외': 30})

st.markdown("<h1 style='text-align: center;'>서울 공공 와이파이, 어디 있나요?</h1>", unsafe_allow_html=True)
layer = pdk.Layer(
    "ScatterplotLayer",
    data,
    get_position='[lon, lat]',
    get_color='color',
    get_radius='radius',
    pickable=True,  # 마우스 오버시 정보 표시
)

view_state = pdk.ViewState(
    latitude=data['lat'].mean(),
    longitude=data['lon'].mean(),
    zoom=13,
    pitch=30,
)
deck = pdk.Deck(layers=[layer], initial_view_state=view_state)
st.pydeck_chart(deck)

st.markdown("<h3 style='font-size:15px;'>실내 설치는 파란색, 실외 설치는 노란색으로 표시되었습니다.</h3>", unsafe_allow_html=True)
