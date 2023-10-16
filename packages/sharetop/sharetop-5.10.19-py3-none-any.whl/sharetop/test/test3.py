from sharetop.core.stock.stock_base_info import get_stock_base_info
import requests
import datetime
import re
import pandas as pd


def fund_hk_rank_em() -> pd.DataFrame:
    """
    东方财富网-数据中心-香港基金排行
    https://overseas.1234567.com.cn/FundList
    :return: 香港基金排行
    :rtype: pandas.DataFrame
    """
    format_date = datetime.datetime.now().date().isoformat()
    url = "https://overseas.1234567.com.cn/overseasapi/OpenApiHander.ashx"
    params = {
        'api': 'HKFDApi',
        'm': 'MethodFundList',
        'action': '1',
        'pageindex': '0',
        'pagesize': '5000',
        'dy': '1',
        'date1': format_date,
        'date2': format_date,
        'sortfield': 'Y',
        'sorttype': '-1',
        'isbuy': '0',
        '_': '1610790553848',
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
        "Referer": "http://fund.eastmoney.com/fundguzhi.html",
    }
    r = requests.get(url, params=params, headers=headers)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["Data"])
    temp_df.reset_index(inplace=True)
    temp_df["index"] = list(range(1, len(temp_df) + 1))
    temp_df.columns = [
        "序号",
        "_",
        "香港基金代码",
        "基金代码",
        "_",
        "基金简称",
        "可购买",
        "日期",
        "单位净值",
        "日增长率",
        "_",
        "近1周",
        "近1月",
        "近3月",
        "近6月",
        "近1年",
        "近2年",
        "近3年",
        "今年来",
        "成立来",
        "币种",
    ]
    temp_df = temp_df[
        [
            "序号",
            "基金代码",
            "基金简称",
            "币种",
            "日期",
            "单位净值",
            "日增长率",
            "近1周",
            "近1月",
            "近3月",
            "近6月",
            "近1年",
            "近2年",
            "近3年",
            "今年来",
            "成立来",
            "可购买",
            "香港基金代码",
        ]
    ]
    temp_df['日期'] = pd.to_datetime(temp_df['日期']).dt.date
    temp_df['单位净值'] = pd.to_numeric(temp_df['单位净值'], errors="coerce")
    temp_df['日增长率'] = pd.to_numeric(temp_df['日增长率'], errors="coerce")
    temp_df['近1周'] = pd.to_numeric(temp_df['近1周'], errors="coerce")
    temp_df['近1月'] = pd.to_numeric(temp_df['近1月'], errors="coerce")
    temp_df['近3月'] = pd.to_numeric(temp_df['近3月'], errors="coerce")
    temp_df['近6月'] = pd.to_numeric(temp_df['近6月'], errors="coerce")
    temp_df['近1年'] = pd.to_numeric(temp_df['近1年'], errors="coerce")
    temp_df['近2年'] = pd.to_numeric(temp_df['近2年'], errors="coerce")
    temp_df['近3年'] = pd.to_numeric(temp_df['近3年'], errors="coerce")
    temp_df['今年来'] = pd.to_numeric(temp_df['今年来'], errors="coerce")
    temp_df['成立来'] = pd.to_numeric(temp_df['成立来'], errors="coerce")
    temp_df['成立来'] = pd.to_numeric(temp_df['成立来'], errors="coerce")
    temp_df['可购买'] = temp_df['可购买'].map(lambda x: "可购买" if x == "1" else "不可购买")
    return temp_df


if __name__ == '__main__':
    # t1 = '012768,华夏中证动漫游戏ETF联接A,HXZZDMYXETFLJA,2023-04-28,1.6020,1.6020,9.40,12.10,32.20,78.38,121.61,108.51,,,94.82,60.20,2021-08-31,1,96.1793,1.20%,0.12%,1,0.12%,1,'

    r = fund_hk_rank_em()
    print(r)