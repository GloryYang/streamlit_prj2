import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

# ------------------------
# 模拟一些数据（你可换成自己的）
# ------------------------
df = pd.DataFrame({
    "year": ["2021", "2022", "2023", "2024", "2025Q3"],
    "营业总收入": [100, 150, 130, 120, 140],
    "归母净利润": [44.78, 155.7, 79.14, 46.63, 45.03],
    "扣非净利润": [40, 150, 70, 45, 42],
    "销售毛利率": [22, 28, 26, 24, 25],
})

metrics = ["营业总收入", "归母净利润", "扣非净利润", "销售毛利率"]


# =====================================================
# 方式一： segmented_control（最像手机 App 的按钮组）
# =====================================================
st.subheader("方式一：segmented_control（最像你图片那种按钮）")

choice1 = st.segmented_control(
    "选择指标（segmented_control）",
    metrics
)

fig1 = px.bar(df, x="year", y=choice1, text=choice1)
st.plotly_chart(fig1, use_container_width=True)


# =====================================================
# 方式二： tabs（适合内容较多的切换）
# =====================================================
st.subheader("方式二：tabs（上方标签切换）")

tab1, tab2, tab3, tab4 = st.tabs(metrics)

for tab, metric in zip([tab1, tab2, tab3, tab4], metrics):
    with tab:
        fig = px.line(df, x="year", y=metric, markers=True, text=metric)
        st.plotly_chart(fig, use_container_width=True)


# =====================================================
# 方式三： radio（最简单通用，支持横向按钮）
# =====================================================
st.subheader("方式三：radio（可水平排列的按钮组）")

choice3 = st.radio(
    "选择指标（radio）",
    metrics,
    horizontal=True
)

fig3 = px.bar(df, x="year", y=choice3, text=choice3)
st.plotly_chart(fig3, use_container_width=True)
