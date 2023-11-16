from bs4 import BeautifulSoup
import numpy as np
import re
import json

def get_num_stat(selector: str, items: list):
    nums = list(map(lambda x: int(x[selector]), items))

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

        star = BeautifulSoup(text, 'xml').star

        item = dict()
        for el in star.contents:
            if el.name is not None:
                item[el.name] = el.get_text().strip()

        return item

items = []
for i in range(1, 501):
    file_name = f"./task3/zip_var_29/{i}.xml"
    items.append(handle_file(file_name))

items = sorted(items, key=lambda x: int(x['radius']), reverse=True)

with open("./task3/result_all.json", 'w', encoding="utf-8") as f:
    f.write(json.dumps(items))

filtered_items = []
for item in items:
    if float(item['rotation'].replace(' days', '').strip()) >= 500:
        filtered_items.append(item)

with open("./task3/result_filtered.json", 'w', encoding="utf-8") as f:
    f.write(json.dumps(filtered_items))

num_stat = get_num_stat("radius", items)

print(num_stat)

title_freq = get_freq("constellation", items)

print(title_freq)
