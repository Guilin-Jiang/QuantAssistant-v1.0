def backtest_sma_strategy(df):
    df = df.copy()
    df["Signal"] = 0
    df.loc[df["SMA_20"] > df["SMA_50"], "Signal"] = 1
    df.loc[df["SMA_20"] < df["SMA_50"], "Signal"] = -1
    df["Return"] = df["Close"].pct_change()
    df["Strategy_Return"] = df["Signal"].shift(1) * df["Return"]
    cumulative_return = (1 + df["Strategy_Return"].fillna(0)).cumprod()
    return df, cumulative_return