from sharetop.core.futures.get_futures_info import get_futures_base_info, get_future_history_data, get_future_deal_detail, get_future_all_realtime_quotes


token = "f109298d079b5f60"


# d = get_futures_base_info(token)

d = get_future_history_data(token, "114.pg2312", is_explain=True)

# d = get_future_deal_detail("114.pg2312")

# d = get_future_all_realtime_quotes(token)

print(d.to_dict("records"))