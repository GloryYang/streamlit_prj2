import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

# CSS 横向滚动
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

# 所有列名都转为字符串
metrics = [str(c) for c in df.columns[1:]]

choice = st.segmented_control("选择指标：", metrics)

st.write("当前选择：", choice)

# 防止 choice 为 None
if not isinstance(choice, str):
    st.stop()

# 根据指标类型选择图表
if "率" in choice:
    fig = px.line(df, x="year", y=choice, markers=True)
else:
    fig = px.bar(df, x="year", y=choice, text=choice)

st.plotly_chart(fig, use_container_width=True)
