from bs4 import BeautifulSoup
import utils

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
    item['img'] = site.find_all("img", attrs={"class": "main-product-image-large"})[0]['src']

    parsed_reviews = site.find_all("div", attrs={"class", "expert-review"})

    if parsed_reviews is not None:
        item["reviews"] = list()
        for parsed_review in parsed_reviews:
            review = dict()

            review["author"] = parsed_review.find_all("div", attrs={"class", "author"})[0].get_text().strip()
            review["score"] = parsed_review.find_all("div", attrs={"class", "score"})[0].get_text().strip()
            review["note"] = parsed_review.find_all("div", attrs={"class", "note"})[0].get_text().strip()

            item["reviews"].append(review)

    return item

items = []
for i in range(1, 11):
    file_name = f"./task5/single_objects/{i}.html"
    items.append(handle_file(file_name))

items = sorted(items, key=lambda x: x['price'], reverse=True)

filtered_items = []
for item in items:
    if item['vintage'] > 2005:
        filtered_items.append(item)

num_stat = utils.get_num_stat("price", items)
case_size_freq = utils.get_freq("case_size", items)

utils.write_to_json("./task5/result2_all.json", items)
utils.write_to_json("./task5/result2_filtered.json", filtered_items)
utils.write_to_json("./task5/result2_num_stat.json", num_stat)
utils.write_to_json("./task5/result2_case_size_freq.json", case_size_freq)