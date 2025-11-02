import streamlit as st
import pandas as pd
import akshare as ak
import plotly.express as px

# ======================
# 页面配置
# ======================
st.set_page_config(page_title="财务分析仪表盘", layout="wide")
st.title("📊 上市公司财务分析仪表盘")

# ======================
# 输入区
# ======================
stock_code = st.text_input("输入股票代码（如 sh600519、sz000001）:", "sh600519")

@st.cache_data(ttl=3600)
def get_financial_data(code):
    """
    稳定版：尝试多个接口，自动识别列名。
    """
    df = None

    # ---- 优先尝试 新浪接口 ----
    try:
        df = ak.stock_financial_report_sina(stock=code, symbol='利润表')
    except Exception as e:
        print("新浪接口失败：", e)

    # ---- 如果新浪无数据，尝试 东方财富接口 ----
    if df is None or df.empty:
        try:
            df = ak.stock_financial_abstract_ths(symbol=code, indicator='按报告期')
        except Exception as e:
            print("同花顺接口失败：", e)
            return None

    if df is None or df.empty:
        return None

    # ---- 统一字段名 ----
    df.columns = [c.strip() for c in df.columns]
    date_col = None
    for candidate in ["报告期", "报告日", "日期", "报告时间"]:
        if candidate in df.columns:
            date_col = candidate
            break

    if date_col is None:
        st.error("接口返回数据中未找到报告期字段。")
        return None

    df = df.rename(columns={date_col: "报告期"})
    df = df.sort_values("报告期")

    # ---- 保留关键字段 ----
    keep_cols = [c for c in ["报告期", "营业收入", "营业总收入", "净利润", "总资产", "负债合计", "经营现金流净额"] if c in df.columns]
    df = df[keep_cols].dropna(how="all")

    if "报告期" not in df or df.empty:
        return None

    # ---- 生成季度列 ----
    df["报告期"] = pd.to_datetime(df["报告期"], errors="coerce")
    df = df.dropna(subset=["报告期"])
    df["季度"] = df["报告期"].dt.quarter.map({1: "Q1", 2: "Q2", 3: "Q3", 4: "Q4"})
    df["报告期"] = df["报告期"].dt.strftime("%Y-%m-%d")

    for col in ["营业收入", "净利润"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    
    # ---- 计算同比 ----
    if "营业收入" in df.columns:
        df["营业收入同比(%)"] = df["营业收入"].pct_change(4) * 100
    if "净利润" in df.columns:
        df["净利润同比(%)"] = df["净利润"].pct_change(4) * 100

    return df.reset_index(drop=True)


# ======================
# 主体逻辑
# ======================
if stock_code:
    df = get_financial_data(stock_code)

    if df is not None and not df.empty:
        st.success(f"✅ 成功获取 {stock_code} 财务数据，共 {len(df)} 条季度记录")

        # 可选指标
        indicators = [c for c in ["营业收入", "净利润", "总资产", "负债合计", "经营现金流净额"] if c in df.columns]
        selected = st.selectbox("选择指标：", indicators, index=0)

        # ---- 图1：单季度柱状图 ----
        fig1 = px.bar(
            df,
            x="报告期",
            y=selected,
            color="季度",
            title=f"{selected}（单季度）",
            text_auto=".2s",
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig1.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig1, width="stretch")

        # ---- 图2：同比折线图 ----
        if f"{selected}同比(%)" in df.columns:
            fig2 = px.line(
                df,
                x="报告期",
                y=f"{selected}同比(%)",
                markers=True,
                title=f"{selected} 同比增长率（%）",
                line_shape="spline"
            )
            fig2.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig2, width="stretch")

        # ---- 展示原始数据 ----
        with st.expander("📋 查看原始数据"):
            st.dataframe(df, width="stretch")
    else:
        st.warning("未获取到财务数据，请检查股票代码或网络连接。")
else:
    st.info("请输入股票代码开始分析。")

