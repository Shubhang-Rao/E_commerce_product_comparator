# Single Page

# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from flask_cors import cross_origin
# from bs4 import BeautifulSoup
# import requests
# from concurrent.futures import ThreadPoolExecutor
# import threading

# import requests
# from bs4 import BeautifulSoup

# app = Flask(__name__)
# CORS(app, resources={r"/*": {"origins": "*"}})

# def get_title(soup):
#     try:
#         title = soup.find("span", attrs={"id": 'productTitle'})
#         title_string = title.text.strip() if title else ""
#     except Exception:
#         title_string = ""
#     return title_string

# # Function to extract Product Price
# def get_price(soup):
#     try:
#         price = soup.find("span", attrs={'class': 'a-offscreen'}).string.strip()
#     except Exception:
#         price = ""
#     return price




# def get_image_url(soup):
#     try:
#         # Find the div containing the product image
#         image_container = soup.find("div", class_="imgTagWrapper")
#         html_content = str(image_container)
#         soup = BeautifulSoup(html_content, 'html.parser')
#         img_tag = soup.find('img')
#         first_image_url = img_tag.get('src')

#     except Exception:
#         # If there is any error, return an empty string
#         first_image_url = ""
    
#     return first_image_url


# @app.route('/products')
# @cross_origin()
# def get_products():

#     def get_product_details(link):
#         print("visiting",link[:20],"..")
#         data = dict()
#         new_webpage = requests.get("https://www.amazon.com" + link, headers=HEADERS)
#         new_soup = BeautifulSoup(new_webpage.content, "html.parser")
#         data['title']=get_title(new_soup)
#         data['price']=get_price(new_soup)
#         data['image_url']=get_image_url(new_soup)
#         data['platform']="Amazon"
#         if data['price'].startswith("$"):
#             temp = data['price']
#             data['price']=int(int(temp[1:])*83)
#             lock.acquire()
#             final_list.append(data)
#             lock.release()


#     product_name = request.args.get('product_name')
#     print(product_name)
#     base_url = "https://www.flipkart.com/search"
#     search_url = f"{base_url}?q={product_name}"
#     response = requests.get(search_url)

#     soup = BeautifulSoup(response.content, 'html.parser')

#     product_titles = []
#     product_prices = []
#     product_image_urls = []

#     product_cards = soup.find_all('div', {'class': '_75nlfW'})

#     for card in product_cards:
#         title_card = card.find('div', {'class': 'KzDlHZ'})
#         if title_card:
#             title_text = title_card.text.strip()
#             product_titles.append(title_text)

#         price = card.find('div', {'class': 'Nx9bqj'})
#         if price:
#             price_text = price.text.strip()
#             product_prices.append(price_text)

#         image = card.find('img', {'class': 'DByuf4'})
#         if image:
#             image_url = image.get('src')
#             product_image_urls.append(image_url)

#     products = []
    
#     for title, price, image_url in zip(product_titles, product_prices, product_image_urls):
#         price = price[1:].replace(",","")

#         product_dict = {
#             "title": title,
#             "price": int(price),
#             "image_url": image_url,
#             "platform": "Flipkart"
#         }
#         products.append(product_dict)
    
#     lock = threading.Lock()

#     HEADERS = {'User-Agent': '', 'Accept-Language': 'en-US, en;q=0.5'}
#     URL = f"https://www.amazon.com/s?k={product_name.replace(' ', '+')}&ref=nb_sb_noss_2"
#     webpage = requests.get(URL, headers=HEADERS)
#     soup = BeautifulSoup(webpage.content, "html.parser")
#     links = soup.find_all("a", attrs={'class': 'a-link-normal s-no-outline'})
#     links_list = []

#     for link in links:
#         links_list.append(link.get('href'))

#     final_list = []
#     executor = ThreadPoolExecutor(max_workers=30)
#     for link in links_list:
#         executor.submit(get_product_details,link)
#     executor.shutdown(wait=True)  
#     print('flipkart',len(products))
#     print('amazon',len(final_list))
#     products.extend(final_list)
#     products.sort( key=lambda x: x["price"])

#     return jsonify(products)


# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_cors import cross_origin
from bs4 import BeautifulSoup
import requests
from concurrent.futures import ThreadPoolExecutor
import threading

import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

def get_title(soup):
    try:
        title = soup.find("span", attrs={"id": 'productTitle'})
        title_string = title.text.strip() if title else ""
    except Exception:
        title_string = ""
    return title_string


def get_price(soup):
    try:
        price = soup.find("span", attrs={'class': 'a-offscreen'}).string.strip()
    except Exception:
        price = ""
    return price




def get_image_url(soup):
    try:
        # Find the div containing the product image
        image_container = soup.find("div", class_="imgTagWrapper")
        html_content = str(image_container)
        soup = BeautifulSoup(html_content, 'html.parser')
        img_tag = soup.find('img')
        first_image_url = img_tag.get('src')

    except Exception:
        # If there is any error, return an empty string
        first_image_url = ""
    
    return first_image_url



@app.route('/products')
@cross_origin()
def get_products():
    final_list = []

    def outer_thread_function(URL):
        webpage = requests.get(URL, headers=HEADERS)
        soup = BeautifulSoup(webpage.content, "html.parser")
        links = soup.find_all("a", attrs={'class': 'a-link-normal s-no-outline'})
        links_list = []

        for link in links:
            links_list.append(link.get('href'))

        executor = ThreadPoolExecutor(max_workers=10)
        for link in links_list:
            executor.submit(get_product_details,link)
        executor.shutdown(wait=True)  


    def get_product_details(link):
        print("visiting",link[:20],"..")
        data = dict()
        new_webpage = requests.get("https://www.amazon.com" + link, headers=HEADERS)
        new_soup = BeautifulSoup(new_webpage.content, "html.parser")
        data['title']=get_title(new_soup)
        data['price']=get_price(new_soup)
        data['image_url']=get_image_url(new_soup)
        data['link']=get_plink(new_soup)
        data['platform']="Amazon"
        if data['price'].startswith("$"):
            temp = data['price']
            data['price']=int(int(temp[1:])*83)
            lock.acquire()
            final_list.append(data)
            lock.release()
       

    product_name = request.args.get('product_name')
    print(product_name)
    base_url = "https://www.flipkart.com/search"
    search_url = f"{base_url}?q={product_name}"
    response = requests.get(search_url)

    soup = BeautifulSoup(response.content, 'html.parser')

    product_titles = []
    product_prices = []
    product_image_urls = []

    product_cards = soup.find_all('div', {'class': '_75nlfW'})

    for card in product_cards:
        title_card = card.find('div', {'class': 'KzDlHZ'})
        if title_card:
            title_text = title_card.text.strip()
            product_titles.append(title_text)

        price = card.find('div', {'class': 'Nx9bqj'})
        if price:
            price_text = price.text.strip()
            product_prices.append(price_text)

        image = card.find('img', {'class': 'DByuf4'})
        if image:
            image_url = image.get('src')
            product_image_urls.append(image_url)

    products = []
    
    for title, price, image_url in zip(product_titles, product_prices, product_image_urls):
        price = price[1:].replace(",","")

        product_dict = {
            "title": title,
            "price": int(price),
            "image_url": image_url,
            "platform": "Flipkart"
        }
        products.append(product_dict)
    
    lock = threading.Lock()

    HEADERS = {'User-Agent': '', 'Accept-Language': 'en-US, en;q=0.5'}
    URL = f"https://www.amazon.com/s?k={product_name.replace(' ', '+')}&ref=nb_sb_noss_2"
    
    executor = ThreadPoolExecutor(max_workers=5)
    for i in range(5):
        executor.submit(outer_thread_function,URL+"&page="+str(i))
    executor.shutdown(wait=True) 

    print('flipkart',len(products))
    print('amazon',len(final_list))
    products.extend(final_list)
    products.sort( key=lambda x: x["price"])

    return jsonify(products)


if __name__ == '__main__':
    app.run(debug=True)


