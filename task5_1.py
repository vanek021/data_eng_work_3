from bs4 import BeautifulSoup
import utils

def get_item(container):
    item = dict()
    item["name"] = container.find_all("td")[1].a.get_text().strip()
    item["vintage"] = container.find_all("td")[2].find_all("span")[0].get_text().strip()
    item["case_size"] = container.find_all("td")[3].get_text().strip()
    item["price"] = float(container.find_all("td")[4].get_text().replace("£", "").replace(",", "").strip())
    reviews_summary = container.find_all("td", attrs={"class": "reviews"})[0]
    if reviews_summary is not None and reviews_summary.a is not None:
        item["reviews_summary"] = reviews_summary.a.get_text()

        parsed_reviews = container.find_next("tr").find_all("div", attrs={"class", "tasting-note"})
        item["reviews"] = list()

        for parsed_review in parsed_reviews:
            review = dict()

            tasting_title = parsed_review.find_all("div", attrs={"class", "tasting-title"})[0]
            review["author"] = tasting_title.find_all("div", attrs={"class", "author"})[0].get_text().replace(",", "").strip()
            review["published"] = tasting_title.find_all("div", attrs={"class", "published"})[0].get_text().strip()
            review["score"] = tasting_title.find_all("div", attrs={"class", "score"})[0].get_text().strip()
            review["note"] = parsed_review.find_all("div", attrs={"class", "note"})[0].get_text().strip()

            item["reviews"].append(review)


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

filtered_items = []
for item in items:
    if item['vintage'] == "NV":
        filtered_items.append(item)

num_stat = utils.get_num_stat("price", items)
case_size_freq = utils.get_freq("case_size", items)

utils.write_to_json("./task5/result_all.json", items)
utils.write_to_json("./task5/result_filtered.json", filtered_items)
utils.write_to_json("./task5/result_num_stat.json", num_stat)
utils.write_to_json("./task5/result_case_size_freq.json", case_size_freq)
