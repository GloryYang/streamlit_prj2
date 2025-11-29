import streamlit as st
import numpy as np

# 设置页面为宽布局，可以更好地利用空间
st.set_page_config(layout="wide")

st.title("我的Streamlit应用")

# 在侧边栏放置一个全局滑块
with st.sidebar:
    data_points = st.slider("选择数据点的数量", 5, 20, 10)

# 创建数据
data = np.random.randn(data_points, 1)

# 创建两个选项卡
tab_chart, tab_data, tab_about = st.tabs(["📈 图表", "🗃 数据", "ℹ️ 关于"])

with tab_chart:
    st.subheader("交互式图表")
    # 在选项卡内使用列布局
    col1, col2 = st.columns([3, 1])
    with col1:
        st.line_chart(data)
    with col2:
        st.metric("平均值", np.mean(data).round(2))

with tab_data:
    st.subheader("原始数据")
    st.dataframe(data)

with tab_about:
    st.subheader("关于这个应用")
    with st.expander("点击查看说明"):
        st.write("这个应用展示了Streamlit选项卡的基本用法。")
    st.info("你可以通过上方的选项卡切换不同的视图。")
