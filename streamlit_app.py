import streamlit as st
import plotly.graph_objs as go
from app.data_loader import load_stock_data
from app.indicators import add_indicators
from app.model import forecast_stock
from app.backtest import backtest_sma_strategy

st.set_page_config(page_title="Quant Trading Dashboard", layout="wide")
st.title("量化交易与市场预测助手")

ticker = st.text_input("输入股票代码（如 AAPL、TSLA）", "AAPL")
period = st.selectbox("选择历史数据周期", ["1y", "2y", "5y"], index=0)
forecast_period = 180

if st.button("开始分析"):
    df = load_stock_data(ticker, period)
    df = add_indicators(df)
    forecast = forecast_stock(df, periods=forecast_period)
    df_bt, cum_return = backtest_sma_strategy(df)

    st.subheader("收盘价与均线")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["Date"], y=df["Close"], name="Close"))
    fig.add_trace(go.Scatter(x=df["Date"], y=df["SMA_20"], name="SMA 20"))
    fig.add_trace(go.Scatter(x=df["Date"], y=df["SMA_50"], name="SMA 50"))
    st.plotly_chart(fig, use_container_width=True)

    st.subheader(f"未来 {forecast_period} 天价格预测（Prophet）")
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=forecast["ds"], y=forecast["yhat"], name="预测价格"))
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("策略回测（简单双均线）")
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(x=df_bt["Date"], y=cum_return, name="策略累计收益"))
    st.plotly_chart(fig3, use_container_width=True)