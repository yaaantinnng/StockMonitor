import akshare as ak
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
import webbrowser
import os

def plot_individual_k_lines(symbol):
    # 获取日K线数据（前复权）
    stock_data = ak.stock_zh_a_hist(symbol=symbol, adjust="qfq")

    # 转换日期列，并设置日期为索引，按日期排序
    stock_data['日期'] = pd.to_datetime(stock_data['日期'])
    stock_data.set_index('日期', inplace=True)
    stock_data = stock_data.sort_index()

    # 过滤掉非开盘日
    stock_data = stock_data[stock_data['开盘'] > 0]

    # 日K线数据（近一年），计算移动平均线并只保留最近15行数据
    daily_data = stock_data[stock_data.index >= (pd.Timestamp.now() - pd.DateOffset(years=1))]
    daily_data['MA5'] = daily_data['收盘'].rolling(window=5).mean()
    daily_data['MA10'] = daily_data['收盘'].rolling(window=10).mean()
    daily_data['MA20'] = daily_data['收盘'].rolling(window=20).mean()
    daily_data['MA30'] = daily_data['收盘'].rolling(window=30).mean()
    daily_data = daily_data.tail(15)
    daily_data.index = daily_data.index.strftime('%y-%m-%d')  # 格式化为字符串格式

    # 周K线数据（近三年），计算移动平均线并只保留最近15行数据
    weekly_data = stock_data['收盘'].resample('W').ohlc().dropna()
    weekly_data['MA5'] = weekly_data['close'].rolling(window=5).mean()
    weekly_data['MA10'] = weekly_data['close'].rolling(window=10).mean()
    weekly_data['MA30'] = weekly_data['close'].rolling(window=30).mean()
    weekly_data['MA99'] = weekly_data['close'].rolling(window=99).mean()
    weekly_data = weekly_data[weekly_data.index >= (pd.Timestamp.now() - pd.DateOffset(years=3))]
    weekly_data.fillna(method='ffill', inplace=True)
    weekly_data = weekly_data.tail(15)
    weekly_data.index = weekly_data.index.strftime('%y-%m-%d')  # 格式化为字符串格式

    # 月K线数据（历史所有数据）
    monthly_data = stock_data['收盘'].resample('M').ohlc().dropna()
    monthly_data['MA5'] = monthly_data['close'].rolling(window=5).mean()
    monthly_data['MA10'] = monthly_data['close'].rolling(window=10).mean()
    monthly_data['MA20'] = monthly_data['close'].rolling(window=20).mean()
    monthly_data['MA30'] = monthly_data['close'].rolling(window=30).mean()
    monthly_data.fillna(method='ffill', inplace=True)
    monthly_data.index = monthly_data.index.strftime('%y-%m-%d')  # 格式化为字符串格式

    # 日K线图
    fig_daily = go.Figure()
    fig_daily.add_trace(go.Candlestick(
        x=daily_data.index, open=daily_data['开盘'], high=daily_data['最高'],
        low=daily_data['最低'], close=daily_data['收盘'], name="Daily K-line"))
    fig_daily.add_trace(go.Scatter(x=daily_data.index, y=daily_data['MA5'], mode='lines', name='MA5', line=dict(width=1)))
    fig_daily.add_trace(go.Scatter(x=daily_data.index, y=daily_data['MA10'], mode='lines', name='MA10', line=dict(width=1)))
    fig_daily.add_trace(go.Scatter(x=daily_data.index, y=daily_data['MA20'], mode='lines', name='MA20', line=dict(width=1)))
    fig_daily.add_trace(go.Scatter(x=daily_data.index, y=daily_data['MA30'], mode='lines', name='MA30', line=dict(width=1)))
    fig_daily.update_layout(
        title=f"{symbol} Daily K-line with MA5, MA10, MA20, MA30 (Recent 15 Days)",
        xaxis_title="Date", yaxis_title="Price (CNY)", template="plotly_dark",
        xaxis=dict(type='category'),  # 将x轴设置为类别型
        xaxis_rangeslider_visible=False
    )

    # 周K线图
    fig_weekly = go.Figure()
    fig_weekly.add_trace(go.Candlestick(
        x=weekly_data.index, open=weekly_data['open'], high=weekly_data['high'],
        low=weekly_data['low'], close=weekly_data['close'], name="Weekly K-line"))
    fig_weekly.add_trace(go.Scatter(x=weekly_data.index, y=weekly_data['MA5'], mode='lines', name='MA5', line=dict(width=1)))
    fig_weekly.add_trace(go.Scatter(x=weekly_data.index, y=weekly_data['MA10'], mode='lines', name='MA10', line=dict(width=1)))
    fig_weekly.add_trace(go.Scatter(x=weekly_data.index, y=weekly_data['MA30'], mode='lines', name='MA30', line=dict(width=1)))
    fig_weekly.add_trace(go.Scatter(x=weekly_data.index, y=weekly_data['MA99'], mode='lines', name='MA99', line=dict(width=1)))
    fig_weekly.update_layout(
        title=f"{symbol} Weekly K-line with MA5, MA10, MA30, MA99 (Recent 15 Weeks)",
        xaxis_title="Date", yaxis_title="Price (CNY)", template="plotly_dark",
        xaxis=dict(type='category'),  # 将x轴设置为类别型
        xaxis_rangeslider_visible=False
    )

    # 月K线图
    fig_monthly = go.Figure()
    fig_monthly.add_trace(go.Candlestick(
        x=monthly_data.index, open=monthly_data['open'], high=monthly_data['high'],
        low=monthly_data['low'], close=monthly_data['close'], name="Monthly K-line"))
    fig_monthly.add_trace(go.Scatter(x=monthly_data.index, y=monthly_data['MA5'], mode='lines', name='MA5', line=dict(width=1)))
    fig_monthly.add_trace(go.Scatter(x=monthly_data.index, y=monthly_data['MA10'], mode='lines', name='MA10', line=dict(width=1)))
    fig_monthly.add_trace(go.Scatter(x=monthly_data.index, y=monthly_data['MA20'], mode='lines', name='MA20', line=dict(width=1)))
    fig_monthly.add_trace(go.Scatter(x=monthly_data.index, y=monthly_data['MA30'], mode='lines', name='MA30', line=dict(width=1)))
    fig_monthly.update_layout(
        title=f"{symbol} Monthly K-line with MA5, MA10, MA20, MA30 (All History)",
        xaxis_title="Date", yaxis_title="Price (CNY)", template="plotly_dark",
        xaxis=dict(type='category'),  # 将x轴设置为类别型
        xaxis_rangeslider_visible=False
    )

    # 将所有图表保存到一个HTML文件
    html_file = f"{symbol}_k_lines_combined.html"
    abs_html_path = os.path.abspath(html_file)  # 获取文件的绝对路径
    with open(html_file, "w") as f:
        f.write(fig_daily.to_html(full_html=False, include_plotlyjs='cdn'))
        f.write(fig_weekly.to_html(full_html=False, include_plotlyjs=False))
        f.write(fig_monthly.to_html(full_html=False, include_plotlyjs=False))

    # 使用 webbrowser 打开生成的HTML文件
    webbrowser.open(f"file://{abs_html_path}")

# 调用函数查看股票
plot_individual_k_lines("603259")  # 示例：吴Xi AppTec (603259)
