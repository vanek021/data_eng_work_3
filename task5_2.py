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

def handle_file(file_name):
    with open(file_name, encoding="utf-8") as file:
        text = ""
        for row in file.readlines():
            text += row
    
    site = BeautifulSoup(text, 'html.parser')
    item = dict()
    item['name'] = site.find_all("h1", attrs={"itemprop": "name"})[0].get_text().strip()
    item['vintage'] = int(site.find_all("option", attrs={"selected": "selected"})[0].get_text().strip())
    item['case_size'] = site.find_all("div", attrs={"class": "pricing-option"})[0].get_text().split("\n")[3].strip()
    item['price'] = float(site.find_all("span", attrs={"class": "price"})[0].get_text().replace("£", "").replace(",", "").strip())

    return item

items = []
for i in range(1, 11):
    file_name = f"./task5/single_objects/{i}.html"
    items.append(handle_file(file_name))

items = sorted(items, key=lambda x: x['price'], reverse=True)

with open("./task5/result2_all.json", 'w', encoding="utf-8") as f:
    f.write(json.dumps(items))

filtered_items = []
for item in items:
    if item['vintage'] > 2005:
        filtered_items.append(item)

with open("./task5/result2_filtered.json", 'w', encoding="utf-8") as f:
    f.write(json.dumps(filtered_items))

num_stat = get_num_stat("price", items)

print(num_stat)

title_freq = get_freq("case_size", items)

print(title_freq)