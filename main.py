import time
import csv

from bs4 import BeautifulSoup
import requests

filename = "products.csv"

data_lost_count = 0

with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Name", "Product Price", "Product URL", "Rating", "No. of Reviews", "ASIN", "Item Weight",
                     "Manufacturer", "Model Number", "Quantity", "Generic Name", "Description"])

for i in range(1, 21):
    url = f"https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&page={i}"
    while True:
        try:
            responses = requests.get(url)
            responses.raise_for_status()

        except requests.exceptions.HTTPError as e:
            print(e)
            time.sleep(1)

        except requests.exceptions.RequestException as e:
            print(f"Connection error: {e}")
            print("Retrying in 1 second...")
            time.sleep(1)

        else:
            response = responses.text

            soup = BeautifulSoup(response, "html.parser")

            products = soup.find_all(
                class_="sg-col-20-of-24 s-result-item s-asin sg-col-0-of-12 sg-col-16-of-20 sg-col s-widget-spacing-small sg-col-12-of-16")

            a = 0

            for product in products:
                p_url = product.find(
                    class_="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal").get(
                    "href")
                product_url = "https://amazon.in" + p_url

                asin = product_url.split("/")[-1]

                manufacturer = "N/A"
                model_no = "N/A"
                item_weight = "N/A"
                quantity = "N/A"
                gen_name = "N/A"
                description = ""
                while True:
                    try:
                        pro_response = requests.get(product_url)
                        pro_response.raise_for_status()

                    except requests.exceptions.HTTPError as e:
                        print(e)
                        a += 1
                        print(f"run-time = {a}")
                        if a >= 30:
                            a = 0
                            data_lost_count += 1
                            print(f"data_lost_count = {data_lost_count}")
                            break
                        time.sleep(1)

                    except requests.exceptions.RequestException as e:
                        print(f"Connection error: {e}")
                        print("Retrying in 1 second...")
                        time.sleep(1)

                    else:
                        a = 0
                        get_product = BeautifulSoup(pro_response.text, 'html.parser')
                        try:
                            info = get_product.find(id="productDetails_techSpec_section_1")
                            additional_info = get_product.find(id="productDetails_detailBullets_sections1")

                            try:
                                get_manufacturer = info.find('th', text=" Manufacturer ")
                                manufacturer = get_manufacturer.find_next_sibling('td').text.strip()
                            except AttributeError:
                                get_manufacturer = additional_info.find('th', text=" Manufacturer ")
                                manufacturer = get_manufacturer.find_next_sibling('td').text.strip()
                            print(manufacturer)

                            try:
                                get_model_number = info.find('th', text=" Item Model number ")
                                model_no = get_model_number.find_next_sibling("td").text.strip()
                            except AttributeError:
                                try:
                                    get_model_number = info.find('th', text=" Item model number ")
                                    model_no = get_model_number.find_next_sibling("td").text.strip()
                                except AttributeError:
                                    get_model_number = info.find('th', text=" Item Model Number ")
                                    model_no = get_model_number.find_next_sibling("td").text.strip()
                            print(model_no)

                            try:
                                get_item_weight = info.find('th', text=" Item Weight ")
                                item_weight = get_item_weight.find_next_sibling("td").text.strip()
                            except AttributeError:
                                try:
                                    get_item_weight = additional_info.find('th', text=" Item Weight ")
                                    item_weight = get_item_weight.find_next_sibling("td").text.strip()
                                except AttributeError:
                                    try:
                                        get_item_weight = info.find('th', text=" Weight ")
                                        item_weight = get_item_weight.find_next_sibling("td").text.strip()
                                    except AttributeError:
                                        get_item_weight = additional_info.find('th', text=" Weight ")
                                        item_weight = get_item_weight.find_next_sibling("td").text.strip()
                            print(item_weight)

                            try:
                                get_quantity = additional_info.find('th', text=" Net Quantity ")
                                quantity = get_quantity.find_next_sibling("td").text.strip()
                            except AttributeError:
                                get_quantity = info.find('th', text=" Net Quantity ")
                                quantity = get_quantity.find_next_sibling("td").text.strip()
                            print(quantity)

                            try:
                                get_generic_name = additional_info.find('th', text=" Generic Name ")
                                gen_name = get_generic_name.find_next_sibling("td").text.strip()
                            except AttributeError:
                                get_generic_name = info.find('th', text=" Generic Name ")
                                gen_name = get_generic_name.find_next_sibling("td").text.strip()
                            print(gen_name)

                        except AttributeError as e:
                            print(e)
                            print("next lined")
                            try:
                                details = get_product.find(id="detailBullets_feature_div")
                                try:
                                    get_manufacturer_name = details.find('span',
                                                                         text='Manufacturer\n                                    ‏\n                                        :\n                                    ‎\n                                ')
                                    manufacturer = get_manufacturer_name.find_next_sibling('span').get_text()
                                except AttributeError:
                                    manufacturer = "N/A"
                                    print("manufacturer name not provided")

                                try:
                                    get_model_number = details.find('span',
                                                                    text='Item model number\n                                    ‏\n                                        :\n                                    ‎\n                                ')
                                    model_no = get_model_number.find_next_sibling('span').get_text()
                                except AttributeError:
                                    try:
                                        get_model_number = details.find('span',
                                                                        text='Item Model number\n                                    ‏\n                                        :\n                                    ‎\n                                ')
                                        model_no = get_model_number.find_next_sibling('span').get_text()
                                    except AttributeError:
                                        print("Model no not provided")
                                        model_no = "N/A"

                                try:
                                    get_item_weight = details.find('span',
                                                                   text='Item Weight\n                                    ‏\n                                        :\n                                    ‎\n                                ')
                                    item_weight = get_item_weight.find_next_sibling('span').get_text()
                                except AttributeError:
                                    print("Item weight not provided")
                                    item_weight = "N/A"

                                try:
                                    print(item_weight)
                                    get_quantity = details.find('span',
                                                                text='Net Quantity\n                                    ‏\n                                        :\n                                    ‎\n                                ')
                                    quantity = get_quantity.find_next_sibling('span').get_text()
                                except AttributeError:
                                    print("Net quantity not provided")
                                    quantity = "N/A"

                                try:
                                    get_generic_name = details.find('span',
                                                                    text='Generic Name\n                                    ‏\n                                        :\n                                    ‎\n                                ')
                                    gen_name = get_generic_name.find_next_sibling('span').get_text()
                                except AttributeError:
                                    print("Generic name not provided")
                                    gen_name = "N/A"

                            except AttributeError as e:
                                print(e)
                                break
                            else:
                                try:
                                    description = get_product.find('div', {'id': 'productDescription'}).find("span").text
                                except AttributeError:
                                    description = "N/A"
                                    print("No description provided")
                                    break
                                else:
                                    break

                        else:
                            print("space one")
                            try:
                                all_description = get_product.find(id="aplus").find("h4").find_next_sibling(
                                    'p').text.strip()
                                description = all_description
                                # for one_desc in all_description:
                                #     desc = one_desc.find_next_sibling('p').text.strip()
                                #     description += desc + "\n"

                            except AttributeError:
                                description = "N/A"
                                print("No description provided")
                                break
                            else:
                                break

                name = product.find(class_="a-size-medium a-color-base a-text-normal").text

                try:
                    ratings = product.find(class_="a-icon-alt").text
                except AttributeError:
                    ratings = "N/A"

                try:
                    reviews = product.find(class_="a-size-base s-underline-text").text
                except AttributeError:
                    reviews = "N/A"

                try:
                    original_price = product.find(class_="a-price a-text-price").find(class_="a-offscreen").text
                except AttributeError:
                    original_price = "N/A"

                try:
                    selling_price = product.find('span', {'class': 'a-price-whole'}).text
                except AttributeError:
                    selling_price = "N/A"

                # print(name)
                # print(selling_price)
                # print(original_price)
                # print(product_url)
                # print(ratings)
                # print(reviews)
                # print(asin)
                # print(manufacturer)
                # print(model_no)
                # print(item_weight)
                # print(quantity)
                # print(gen_name)
                # print(description)
                data = [name, selling_price, product_url, ratings, reviews, asin, item_weight, manufacturer, model_no,
                        quantity, gen_name, description]
                try:
                    with open(filename, 'a', newline='', encoding='utf-8-sig') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow(data)
                    print("-----------------------data written-------------------------")

                except FileNotFoundError:
                    print("File will be created")
                    with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow(
                            ["Name", "Product Price", "Product URL", "Rating", "No. of Reviews", "ASIN", "Item Weight",
                             "Manufacturer", "Model Number", "Quantity", "Generic Name", "Description"])

                    with open(filename, 'a', newline='', encoding='utf-8-sig') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow(data)

            print(f"data_lost_count = {data_lost_count}")
            break
