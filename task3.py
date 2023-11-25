from bs4 import BeautifulSoup
import utils

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

filtered_items = []
for item in items:
    if float(item['rotation'].replace(' days', '').strip()) >= 500:
        filtered_items.append(item)

num_stat = utils.get_num_stat("radius", items)
title_freq = utils.get_freq("constellation", items)

utils.write_to_json("./task3/result_all.json", items)
utils.write_to_json("./task3/result_filtered.json", filtered_items)
utils.write_to_json("./task3/result_num_stat.json", num_stat)
utils.write_to_json("./task3/result_title_freq.json", title_freq)
