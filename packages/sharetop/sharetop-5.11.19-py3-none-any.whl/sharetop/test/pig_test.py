from sharetop.core.pig.pig_detail import get_pig_fcr
from sharetop.core.prepare import BasicTop


token = "9ada862fa17ce574"

# start_date = '2023-05-01'
# end_date = '2023-05-16'
#
# d = get_pig_fcr(token, start_date, end_date, is_explain=True)
#
# print(d.to_dict("records"))

sharetop_obj = BasicTop(token)
# d = sharetop_obj.common_exec_func("pig_to_warning_kline_data", {"limit": "10", "start_date": "2022-01-23", "is_explain": False})
d = sharetop_obj.common_exec_func("pig_to_fcr_kline_data", {"limit": "100", "start_date": "2022-01-23", "end_date": "2022-02-27", "is_explain": True})

data = d.get("data")

print(data.to_dict("records"))