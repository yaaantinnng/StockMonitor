# main.py

from stock_trend_test import plot_individual_k_lines
import webbrowser
import os
from flask import Flask, render_template_string

import warnings
warnings.filterwarnings("ignore")

app = Flask(__name__)

@app.route("/")
def index():
    # 股票代码列表，可以在这里添加更多股票代码
    stock_symbols = ["603259", "000001"]

    # 初始化 HTML 内容
    all_charts_html_content = "<html><head><title>Stock K-Line Charts</title></head><body>"

    # 生成每个股票的图表 HTML 内容
    for symbol in stock_symbols:
        html_content = plot_individual_k_lines(symbol)
        all_charts_html_content += f"<h2>{symbol} Daily K-Line</h2>"
        all_charts_html_content += html_content

    all_charts_html_content += "</body></html>"

    # 渲染 HTML 页面
    return render_template_string(all_charts_html_content)

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))
    # 使用 Heroku 所需的 "0.0.0.0" 作为 host，使应用可以在 Heroku 上被外界访问
    app.run(host="0.0.0.0", port=port)
