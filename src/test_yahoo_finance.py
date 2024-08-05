import requests
from bs4 import BeautifulSoup


def main():
    CODE = "JD"
    r = requests.get(f"https://finance.yahoo.com/quote/{CODE}/?p={CODE}").text

    soup = BeautifulSoup(r, "html.parser")
    alldata = soup.find_all("tbody")
    print(alldata)
    try:
        table1 = alldata[0].find_all("tr")
    except:
        table1 = None
    try:
        table2 = alldata[1].find_all("tr")
    except:
        table2 = None
    l = {}
    u = list()

    # print(soup)

    for i in range(0, len(table1)):
        try:
            table1_td = table1[i].find_all("td")
        except:
            table1_td = None

    l[table1_td[0].text] = table1_td[1].text

    u.append(l)
    l = {}

    for i in range(0, len(table2)):
        try:
            table2_td = table2[i].find_all("td")
        except:
            table2_td = None

    l[table2_td[0].text] = table2_td[1].text

    u.append(l)
    print(u)
    l = {}
    {
        "Yahoo finance": [
            {"Previous Close": "2,317.80"},
            {"Open": "2,340.00"},
            {"Bid": "0.00 x 1800"},
            {"Ask": "2,369.96 x 1100"},
            {"Day’s Range": "2,320.00–2,357.38"},
            {"52 Week Range": "1,626.03–2,475.00"},
            {"Volume": "3,018,351"},
            {"Avg. Volume": "6,180,864"},
            {"Market Cap": "1.173T"},
            {"Beta (5Y Monthly)": "1.35"},
            {"PE Ratio (TTM)": "112.31"},
            {"EPS (TTM)": "20.94"},
            {"Earnings Date": "Jul 23, 2020 — Jul 27, 2020"},
            {"Forward Dividend &amp; Yield": "N/A (N/A)"},
            {"Ex-Dividend Date": "N/A"},
            {"1y Target Est": "2,645.67"},
        ]
    }


if __name__ == "__main__":
    main()
