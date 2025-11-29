import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

# 横向滚动 CSS
st.markdown("""
<style>
div[data-baseweb="segmented-control"] {
    overflow-x: auto;
    white-space: nowrap;
    padding-bottom: 5px;
}
div[data-baseweb="segmented-control"] > div {
    display: inline-flex !important;
    flex-wrap: nowrap !important;
}
</style>
""", unsafe_allow_html=True)

# 示例数据
df = pd.DataFrame({
    "year": ["2021", "2022", "2023", "2024", "2025Q3"],
    "营业总收入": [100,150,130,120,140],
    "归母净利润": [44.78,155.7,79.14,46.63,45.03],
    "扣非净利润": [40,150,70,45,42],
    "销售毛利率": [22,28,26,24,25],
    "销售净利率": [10,18,15,12,13]
})

metrics = list(df.columns[1:])

# 横向滑动 segmented_control
choice = st.segmented_control("选择指标：", metrics)

# 图表逻辑（你可以加更多）
fig = None
if "率" in choice:
    fig = px.line(df, x="year", y=choice, markers=True)
else:
    fig = px.bar(df, x="year", y=choice, text=choice)

st.plotly_chart(fig, use_container_width=True)
