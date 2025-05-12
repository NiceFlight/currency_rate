import requests
from bs4 import BeautifulSoup

currency = {
    1: "USD",
    2: "HKD",
    3: "GBP",
    4: "AUD",
    5: "CAD",
    6: "SGD",
    7: "CHF",
    8: "JPY",
    9: "ZAR",
    10: "SEK",
    11: "NZD",
    12: "THB",
    13: "PHP",
    14: "IDR",
    15: "EUR",
    16: "KRW",
    17: "VND",
    18: "MYR",
    19: "CNY",
}


def get_currency_rate():
    url = "https://rate.bot.com.tw/xrt?Lang=zh-TW"

    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    currency_set = soup.find_all("tbody")
    currency_table = currency_set[0].find_all("tr")  # type: ignore

    data = {}
    for i in currency_table:
        currency_name = i.find("div", class_="visible-phone").text.strip().split("(")[1][:3]  # type: ignore
        cash_buying = i.find_all("td", class_="rate-content-cash text-right print_hide")[0].get("data-table")  # type: ignore
        _cash_buying = i.find_all("td", class_="rate-content-cash text-right print_hide")[0].text.strip()  # type: ignore
        cash_selling = i.find_all("td", class_="rate-content-cash text-right print_hide")[1].get("data-table")  # type: ignore
        _cash_selling = i.find_all("td", class_="rate-content-cash text-right print_hide")[1].text.strip()  # type: ignore
        spot_buying = i.find_all("td", class_="rate-content-sight text-right print_hide")[0].get("data-table")  # type: ignore
        _spot_buying = i.find_all("td", class_="rate-content-sight text-right print_hide")[0].text.strip()  # type: ignore
        spot_selling = i.find_all("td", class_="rate-content-sight text-right print_hide")[1].get("data-table")  # type: ignore
        _spot_selling = i.find_all("td", class_="rate-content-sight text-right print_hide")[1].text.strip()  # type: ignore

        structure = {
            "cash_buying": [cash_buying, _cash_buying],
            "cash_selling": [cash_selling, _cash_selling],
            "spot_buying": [spot_buying, _spot_buying],
            "spot_selling": [spot_selling, _spot_selling],
        }
        data.update({currency_name: structure})
    return data


def main():
    try:
        print("歡迎使用台銀匯率查詢系統")
        input_currency = input(
            "請輸入幣別代碼(1)USD,(2)HKD,(3)GBP,(4)AUD,(5)CAD,(6)SGD,(7)CHF,(8)JPY,(9)ZAR,(10)SEK,(11)NZD,(12)THB,(13)PHP,(14)IDR,(15)EUR,(16)KRW,(17)VND,(18)MYR,(19)CNY：\n"
        )
        if int(input_currency) in range(1, 20):
            selected_currency = currency.get(int(input_currency))
            print(f"您選擇的幣別是：{selected_currency}")
            selected_currency_rate = get_currency_rate().get(selected_currency)
            print(
                f"{selected_currency_rate['cash_buying'][0]}：{selected_currency_rate['cash_buying'][1]}\n{selected_currency_rate['cash_selling'][0]}：{selected_currency_rate['cash_selling'][1]}\n{selected_currency_rate['spot_buying'][0]}：{selected_currency_rate['spot_buying'][1]}\n{selected_currency_rate['spot_selling'][0]}：{selected_currency_rate['spot_selling'][1]}\n"  # type: ignore
            )
        else:
            print("請輸入正確的幣別代碼")
            main()
    except ValueError as e:
        print("請輸入正確的幣別代碼")
        main()


if __name__ == "__main__":
    main()
