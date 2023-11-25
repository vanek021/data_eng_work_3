from bs4 import BeautifulSoup
import re
import utils

def handle_file(file_name):
    with open(file_name, encoding="utf-8") as file:
        text = ""
        for row in file.readlines():
            text += row
        
        site = BeautifulSoup(text, 'html.parser')

        item = dict()

        address = site.find_all("p", attrs={"class": "address-p"})[0].get_text().split("Начало:")

        item['type'] = site.find_all("span", string=re.compile("Тип:"))[0].get_text().replace("Тип:", "").strip()
        item['title'] = site.find_all("h1")[0].get_text().replace("Турнир:\n", "").strip()
        item['city'] = address[0].replace("Город:", "").strip()
        item['date'] = address[1].strip()
        item['count'] = int(site.find_all("span", attrs={"class": "count"})[0].get_text().split(":")[1].strip())
        item['time'] = int(site.find_all("span", attrs={"class": "year"})[0].get_text().split(":")[1].replace("мин", "").strip())
        item['minRating'] = int(site.find_all("span", string=re.compile("Минимальный рейтинг для участия:"))[0].get_text().split(":")[1].strip())
        item['image'] = site.find_all("img")[0]['src']
        item['views'] = int(site.find_all("span", string=re.compile("Просмотры:"))[0].get_text().split(":")[1].strip())
        item['rating'] = float(site.find_all("span", string=re.compile("Рейтинг:"))[0].get_text().split(":")[1].strip())

        return item

items = []
for i in range(1, 1000):
    file_name = f"./task1/zip_var_29/{i}.html"
    result = handle_file(file_name)
    items.append(result)

items = sorted(items, key=lambda x: x['views'], reverse=True)

filtered_items = []
for tournament in items:
    if tournament['minRating'] >= 2400:
        filtered_items.append(tournament)

num_stat = utils.get_num_stat("views", items)
city_freq = utils.get_freq("city", items)

utils.write_to_json("./task1/result_all.json", items)
utils.write_to_json("./task1/result_filtered.json", filtered_items)
utils.write_to_json("./task1/result_num_stat.json", num_stat)
utils.write_to_json("./task1/result_city_freq.json", city_freq)
