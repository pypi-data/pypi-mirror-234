import requests

url = "http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/MoneyFlow.ssx_ggzj_fszs?page=1&num=20&daima=sz002714&sort=time"

r = requests.get(url)

print(r.text)