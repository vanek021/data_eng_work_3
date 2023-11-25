from bs4 import BeautifulSoup
import numpy as np
import re
import json

def get_num_stat(selector: str, items: list):
    nums = list(map(lambda x: float(x[selector]), items))

    stat = {}

    stat['sum'] = sum(nums)
    stat['min'] = min(nums)
    stat['max'] = max(nums)
    stat['avg'] = np.average(nums)
    stat['std'] = np.std(nums)

    return stat

def get_freq(selector: str, items: list):
    freq = {}

    for item in items:
        if selector in item:
            freq[item[selector]] = freq.get(item[selector], 0) + 1
    
    return freq

def get_item(container):
    item = dict()
    item["name"] = container.find_all("td")[1].a.get_text().strip()
    item["vintage"] = container.find_all("td")[2].find_all("span")[0].get_text().strip()
    item["case_size"] = container.find_all("td")[3].get_text().strip()
    item["price"] = float(container.find_all("td")[4].get_text().replace("£", "").replace(",", "").strip())

    return item

def handle_file(file_name):
    items = list()

    with open(file_name, encoding="utf-8") as file:
        text = ""
        for row in file.readlines():
            text += row

        site = BeautifulSoup(text, 'html.parser')
        tr_odd = site.find_all("tr", attrs={"class": "product-row-odd", "id": None})
        tr_even = site.find_all("tr", attrs={"class": "product-row-even", "id": None})

        for tr in tr_odd:
            items.append(get_item(tr))
        
        for tr in tr_even:
            items.append(get_item(tr))

        return items

items = handle_file("./task5/catalog.html")

items = sorted(items, key=lambda x: x['price'], reverse=True)

with open("./task5/result_all.json", 'w', encoding="utf-8") as f:
    f.write(json.dumps(items))

filtered_items = []
for item in items:
    if item['vintage'] == "NV":
        filtered_items.append(item)

with open("./task5/result_filtered.json", 'w', encoding="utf-8") as f:
    f.write(json.dumps(filtered_items))

num_stat = get_num_stat("price", items)

print(num_stat)

title_freq = get_freq("case_size", items)

print(title_freq)
