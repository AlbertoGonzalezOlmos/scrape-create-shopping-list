def main():

    import requests
    from bs4 import BeautifulSoup

    url = "https://www.coingecko.com/fr/pi%C3%A8ces/1/markets_tab"

    soup = BeautifulSoup(requests.get(url).content, "html.parser")

    print(soup)

    data = []
    for tr in soup.select("tr[class]"):
        if "sponsored" in tr["class"]:
            continue
        _, name, paire, cours, spread, prof, *_ = tr.select("td")

        data.append(
            (
                name.get_text(strip=True),
                paire.get_text(strip=True),
                cours.div.get_text(strip=True),
                spread.get_text(strip=True),
                prof.get_text(strip=True),
            )
        )

    # print the data:
    print(
        "{:<4} {:<30} {:<20} {:<20} {:<10} {:<20}".format(
            "No.", "Name", "Paire", "Cours", "Spread", "+2 % de profondeur"
        )
    )
    for i, row in enumerate(data, 1):
        print("{:<4} {:<30} {:<20} {:<20} {:<10} {:<20}".format(i, *row))


if __name__ == "__main__":
    main()
