from sharetop.core.capital_flow.capital_flow_monitor import get_stock_real_time_daily_capital, \
    get_stock_real_time_sum_capital, get_stock_real_time_sector_capital, get_stock_history_capital

stock_code = "002714"
token = "f109298d079b5f60"


# d = get_stock_real_time_daily_capital(stock_code, is_explain=True)

# d = get_stock_history_capital(token, stock_code, is_explain=False)

# d = get_stock_real_time_sum_capital(stock_code, is_explain=True)

d = get_stock_real_time_sector_capital("area", "1", is_explain=True)

print("d====:", d.to_dict("records"))