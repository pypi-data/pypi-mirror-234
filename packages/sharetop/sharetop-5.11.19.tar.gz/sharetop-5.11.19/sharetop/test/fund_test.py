from sharetop.core.fund.fund_list import get_fund_codes
from sharetop.core.fund.get_fund_base_info import get_fund_base_info
from sharetop.core.fund.get_fund_history_data import get_fund_history_price
from sharetop.core.fund.get_fund_industry_info import get_fund_industry_distribution
from sharetop.core.fund.get_fund_invest_info import get_fund_public_dates, get_fund_invest_position
from sharetop.core.fund.get_fund_rank import get_fund_open_rank, get_fund_exchange_rank, get_fund_money_rank, get_fund_hk_rank
from sharetop.core.fund.get_period_change_info import get_fund_period_change
from sharetop.core.fund.get_types_percentage_info import get_fund_types_percentage
from sharetop.core.fund.get_fund_real_time import get_fund_real_time_god
from sharetop.core.prepare import BasicTop


token = "f109298d079b5f60"

# d = get_fund_base_info(token, "001299", is_explain=False)

# d = get_fund_history_price(token, "001299", is_explain=True)

# d = get_public_dates(token, "001299")

# d = get_fund_industry_distribution(token, "161725", "2023-03-31", is_explain=False)

# d = get_fund_invest_position(token, "161725", "2023-03-31")

# d = get_fund_public_dates(token, "161725")

# d = fund_open_fund_rank(token, "债券型")

# d = get_fund_open_rank(token, is_explain=False)

# d = get_fund_exchange_rank(token, is_explain=True)

# d = get_fund_money_rank(token)

# d = get_fund_period_change(token, "161725", is_explain=True)

# d = get_fund_types_percentage(token, "161725")

# d = get_fund_real_time_god("161725", is_explain=True)
# d = fund_money_rank(token)

# d = get_period_change(token, "001299")

# d = get_types_percentage(token, "001299")

# d = get_fund_codes(token, is_explain=True)

# d = get_fund_hk_rank(token, is_explain=False)

# print(d)

if __name__ == '__main__':
    token = "9ada862fa17ce574"
    sharetop_obj = BasicTop(token)
    # print(sharetop_obj.class_map)
    d = sharetop_obj.common_exec_func("fund_to_etf", {"is_explain": False})
    print(d)