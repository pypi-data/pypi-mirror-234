import requests

url = "https://hq.sinajs.cn/?rn=1694440934177&list=globalbd_{bond_name}"

bond_name = "gcny10"

headers = {
            "Referer": "https://stock.finance.sina.com.cn/forex/globalbd/gcny10.html"
        }

r = requests.get(url.format(bond_name=bond_name), headers=headers)

d = r.text


print(d)