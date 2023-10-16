from sharetop.core.ship.ship_detail import get_ship_indicators

token = "9ada862fa17ce574"

d = get_ship_indicators(token, org_name="中国", ship_indicators="1", is_explain=True)

print(d)
