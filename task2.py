from bs4 import BeautifulSoup
import utils

def handle_file(file_name):
    items = list()

    with open(file_name, encoding="utf-8") as file:
        text = ""
        for row in file.readlines():
            text += row
        
        site = BeautifulSoup(text, 'html.parser')
        products = site.find_all("div", attrs={'class': 'product-item'})

        for product in products:
            item = dict()
            item['id'] = product.a['data-id']
            item['link'] = product.find_all('a')[1]['href']
            item['img_url'] = product.find_all('img')[0]['src']
            item['title'] = product.find_all('span')[0].get_text().strip()
            item['price'] = int(product.price.get_text().replace("₽", "").replace(" ", "").strip())
            item['bonus'] = int(product.strong.get_text().replace("+ начислим ", "").replace(" бонусов", "").strip())
            props = product.ul.find_all("li")
            for prop in props:
                item[prop['type']] = prop.get_text().strip()

            items.append(item)

        return items


items = []
for i in range(1, 72):
    file_name = f"./task2/zip_var_29/{i}.html"
    items += handle_file(file_name)

items = sorted(items, key=lambda x: x['price'], reverse=True)

filtered_items = []
for item in items:
    if item['bonus'] >= 2000:
        filtered_items.append(item)

num_stat = utils.get_num_stat("price", items)
title_freq = utils.get_freq("ram", items)

utils.write_to_json("./task2/result_all.json", items)
utils.write_to_json("./task2/result_filtered.json", filtered_items)
utils.write_to_json("./task2/result_num_stat.json", num_stat)
utils.write_to_json("./task2/result_title_freq.json", title_freq)
