
from sharetop.core.stock.getter import get_stock_kline_data, get_stock_real_time_data, get_stock_market_real_time_data
from sharetop.core.stock.quarterly_report import get_stock_all_report_dates, get_stock_company_report_data, get_stock_all_company_quarterly_report
from sharetop.core.stock.rank_list import get_stock_dragon_tiger_list

from sharetop.core.stock.stock_base_info import get_stock_base_info
from sharetop.core.prepare import BasicTop


token = "9ada862fa17ce574"

# d = get_stock_kline_data(token, ['000917.SH', '470050.sz'], klt=5)
# print(d)
# h = {"quote_id_mode": True}

# d = get_stock_kline_data(token, "0.000903", is_explain=False, **h)

# d = get_real_time_bill("002714")

# d = get_history_data(token, "002714", klt=102)

# d = get_real_time_data(["002714", "516110"])

# d = get_stock_market_real_time_data(token, "cn10y", is_explain=False)

# d = get_stock_company_report_data(token, '002714', None, False)

# d = get_stock_all_company_quarterly_report(token, '2013-12-31', is_explain=True)

# d = get_stock_dragon_tiger_list(token, '2023-07-21', '2023-08-03')

# d = get_stock_base_info("0.000903")
# d = get_stock_base_info(["002714", "600809"], is_explain=True)

# d = get_stock_all_report_dates(token, is_explain=False)

# d = get_stock_real_time_data("002714", is_explain=False)

# print(d)

# print(type(d.to_dict("records")[0]['free_float_market_cap']))


if __name__ == '__main__':
    token = "9ada862fa17ce574"
    sharetop_obj = BasicTop(token)
    # print(sharetop_obj)
    d = sharetop_obj.common_exec_func("stock_to_index_list", {"limit": 10, "is_explain": False})
    # d = sharetop_obj
    print(d.to_dict("records"))
