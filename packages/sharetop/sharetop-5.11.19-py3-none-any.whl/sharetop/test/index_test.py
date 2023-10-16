from sharetop.core.index.logistics_index import get_logistics_index


token = "9ada862fa17ce574"

d = get_logistics_index(token, start_date='202002', end_date='202306')

print(d)
