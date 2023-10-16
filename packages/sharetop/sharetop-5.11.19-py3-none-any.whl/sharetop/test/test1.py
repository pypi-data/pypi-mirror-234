get_stock_market_real_time_data_fields = {
    "股票代码": "stock_code",
    "股票名称": "stock_name",
    "涨跌幅": "percentage_change",
    "最新价": "last_price",
    "最高": "high_price",
    "最低": "low_price",
    "今开": "open_price",
    "涨跌额": "price_change",
    "换手率": "turnover_rate",
    "量比": "volume_ratio",
    "动态市盈率": "price_to_earnings_ratio",
    "成交量": "trading_volume",
    "成交额": "trading_volume",
    "昨日收盘": "previous_close",
    "总市值": "market_cap",
    "流通市值": "free_float_market_cap",
    "行情ID": "item_id",
    "市场类型": "market_type",
    "更新时间": "update_time",
    "最新交易日": "latest_trading_day"
}

h = []

for k, v in get_stock_market_real_time_data_fields.items():
    temp_data = {
        "name": v,
        "data_type": "str",
        "show": "Y",
        "description": k
    }
    h.append(temp_data)
print(h)

