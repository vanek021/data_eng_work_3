from bs4 import BeautifulSoup
import utils

def handle_file(file_name):
    items = list()

    with open(file_name, encoding="utf-8") as file:
        text = ""
        for row in file.readlines():
            text += row

        root = BeautifulSoup(text, 'xml')

        for clothing in root.find_all("clothing"):
            item = dict()
            for el in clothing.contents:
                if el.name is None:
                    continue
                elif el.name == "price" or el.name == "reviews":
                    item[el.name] = int(el.get_text().strip())
                elif el.name == "rating":
                    item[el.name] = float(el.get_text().strip())
                elif el.name == "new":
                    item[el.name] = el.get_text().strip() == "+"
                elif el.name == "exclusive" or el.name == "sporty":
                    item[el.name] = el.get_text().strip() == "yes"
                else:
                    item[el.name] = el.get_text().strip()

            items.append(item)

        return items
    
items = []
for i in range(1, 101):
    file_name = f"./task4/zip_var_29/{i}.xml"
    items += handle_file(file_name)

items = sorted(items, key=lambda x: x['price'], reverse=True)

filtered_items = []
for item in items:
    if item['rating'] >= 4:
        filtered_items.append(item)

num_stat = utils.get_num_stat("price", items)
size_freq = utils.get_freq("size", items)

utils.write_to_json("./task4/result_all.json", items)
utils.write_to_json("./task4/result_filtered.json", filtered_items)
utils.write_to_json("./task4/result_num_stat.json", num_stat)
utils.write_to_json("./task4/result_size_freq.json", size_freq)
