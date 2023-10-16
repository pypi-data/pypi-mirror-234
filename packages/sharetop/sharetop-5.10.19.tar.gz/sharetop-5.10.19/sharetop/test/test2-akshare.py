import requests
import pandas as pd

def index_value_name_funddb() -> pd.DataFrame:
    """
    funddb-指数估值-指数代码
    https://funddb.cn/site/index
    :return: pandas.DataFrame
    :rtype: 指数代码
    """
    url = "https://api.jiucaishuo.com/v2/guzhi/showcategory"
    r = requests.get(url)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["data"]["right_list"])
    temp_df.columns = [
        "指数开始时间",
        "-",
        "指数名称",
        "指数代码",
        "最新PE",
        "最新PB",
        "PE分位",
        "PB分位",
        "股息率",
        "-",
        "-",
        "-",
        "更新时间",
        "股息率分位",
        "-",
        "-",
        "-",
        "-",
        "-",
        "-",
        "-",
        "-",
        "-",
        "-",
        "-",
        "-",
        "-",
        "-",
        "-",
        "-",
    ]
    temp_df = temp_df[
        [
            "指数名称",
            "最新PE",
            "PE分位",
            "最新PB",
            "PB分位",
            "股息率",
            "股息率分位",
            "指数代码",
            "指数开始时间",
            "更新时间",
        ]
    ]
    temp_df["指数开始时间"] = pd.to_datetime(temp_df["指数开始时间"]).dt.date
    temp_df["最新PE"] = pd.to_numeric(temp_df["最新PE"], errors="coerce")
    temp_df["PE分位"] = pd.to_numeric(temp_df["PE分位"], errors="coerce")
    temp_df["最新PB"] = pd.to_numeric(temp_df["最新PB"], errors="coerce")
    temp_df["PB分位"] = pd.to_numeric(temp_df["PB分位"], errors="coerce")
    temp_df["股息率"] = pd.to_numeric(temp_df["股息率"], errors="coerce")
    temp_df["股息率分位"] = pd.to_numeric(temp_df["股息率分位"], errors="coerce")
    return temp_df

if __name__ == '__main__':
    d = index_value_name_funddb()
    print(d.to_dict("records"))

