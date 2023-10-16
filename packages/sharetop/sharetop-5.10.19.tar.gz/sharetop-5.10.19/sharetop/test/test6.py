from sharetop.core.capital_flow.capital_flow_monitor import get_stock_real_time_sum_capital, get_stock_history_capital, get_stock_real_time_daily_capital, get_sector_real_time_capital_flow
from enum import Enum
# d = {"a": 1, "b":2}
# d = get_real_time_capital_flow(["002714", "300033"])
# d = get_real_time_capital_flow(['002714', '300033'])
d = get_sector_real_time_capital_flow('area', '10')

# d = get_real_time_capital_flow("000001")

# print(d)
# print(d.to_dict("records"))
import requests

url = 'http://127.0.0.1:8000/sharetopapi/oil/reserves'
access_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJseHkiLCJleHAiOjE2ODUyNzA0NDd9.lPUylZYeHgrWsLEpvqKTU03nioNEyDFJ-SK3vX9UEhQ'
headers = {
    'Authorization': f'Bearer {access_token}'
}

# response = requests.get(url, headers=headers)
#
# r = response.text
#
# print(r)

# h = "2d029512847cf13c"

# print(len(h))

# from sharetop.core.bond.get_bond_info import get_bond_base_info_list, get_bond_realtime_quotes, get_bond_base_info, get_bond_public
token = "f109298d079b5f60"
# d = get_bond_public(token)
# print("d=============:", d)

# d = get_real_time_capital_flow('002714')
print("d=============:", d.to_dict("records"))
