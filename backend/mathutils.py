def get_price(listentries):
    prices = []
    for a in listentries:
        prices.append(a[2])
    return sum(prices)
