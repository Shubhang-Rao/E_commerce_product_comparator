import threading
from concurrent.futures import ThreadPoolExecutor
import requests
from bs4 import BeautifulSoup
import re
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_cors import cross_origin
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/products')
@cross_origin()
def get_products():
    product_name = request.args.get('product_name')
    def get_title(soup):
        try:
            title = soup.find("span", attrs={"id": 'productTitle'})
            title_string = title.text.strip() if title else ""
        except AttributeError:
            title_string = ""
        return title_string

# Function to get price from soup
    def get_price(soup):
        try:
            price_element = soup.find("span", attrs={'class': 'aok-offscreen'})
            price_string = price_element.string.strip() if price_element else ""
            
            # Extract numeric part of the price using regular expression
            price = re.search(r'\d[\d,\.]*', price_string).group().replace(',', '') if price_string else ""
            # price = int(price) if price is not "" else ""
        except AttributeError:
            price = ""
        return int(float(price)) if price != "" else 0

    # Function to get product details
    def get_product_details(link):
        data = dict()
        new_webpage = requests.get("https://www.amazon.in" + link, headers=HEADERS)
        new_soup = BeautifulSoup(new_webpage.content, "html.parser")
        data['title']=get_title(new_soup)

        data['price']=get_price(new_soup)

        data['image_url']=get_image_url(new_soup)

        data['product_link']="https://www.amazon.in" + link

        data['platform'] = "Amazon"


        lock.acquire()
        final_list.append(data)
        lock.release()

    # Function to extract Image URL
    def get_image_url(soup):
        try:
            # Find the div containing the product image
            image_container = soup.find("div", class_="imgTagWrapper")
            html_content = str(image_container)
            soup = BeautifulSoup(html_content, 'html.parser')
            img_tag = soup.find('img')
            first_image_url = img_tag.get('src')

        except (AttributeError, IndexError, ValueError):
            # If there is any error, return an empty string
            first_image_url = ""
        
        return first_image_url

    # Function to save data to CSV file

    lock = threading.Lock()

    search_query = product_name

    HEADERS = {'User-Agent': '', 'Accept-Language': 'en-IN, en;q=0.5'}
    URL = f"https://www.amazon.in/s?k={search_query.replace(' ', '+')}&ref=nb_sb_noss_2"
    webpage = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(webpage.content, "html.parser")
    links = soup.find_all("a", attrs={'class': 'a-link-normal s-no-outline'})
    links_list = []

    for link in links:
        links_list.append(link.get('href'))

    final_list = []
    executor = ThreadPoolExecutor(max_workers=50)
    for link in links_list:
        executor.submit(get_product_details, link)
    executor.shutdown(wait=True)        

    # Print number of items fetched
    print(f"Number of items fetched: {len(final_list)}")

    def get_title1(soup):
        try:
            title = soup.find("span", class_="VU-ZEz")
            title_string = title.text.strip() if title else ""
        except AttributeError:
            title_string = ""
        return title_string

# Function to get price from soup
    def get_price1(soup):
        try:
            price = soup.find("div", class_="Nx9bqj CxhGGd").text.strip()
        except AttributeError:
            price = ""
        return int(price.replace(",","")[1:]) if price != "" else 0

# Function to get product details
    def get_product_details1(link):
        data = dict()
        new_webpage = requests.get(link, headers=HEADERS)
        new_soup = BeautifulSoup(new_webpage.content, "html.parser")

        data['title']=get_title1(new_soup)

        data['price']=get_price1(new_soup)

        data['image_url']=get_image_url1(new_soup)

        data['product_link']=link
        data['platform'] = "Flipkart"

        lock.acquire()
        final_list1.append(data)
        lock.release()

# Function to extract Image URL
    def get_image_url1(soup):
        try:
            image_container = soup.find("div", class_="_4WELSP _6lpKCl")
            image_url = image_container.find("img")["src"]
        except (AttributeError, IndexError):
            image_url = ""
        return image_url

    lock = threading.Lock()

    search_query = product_name

    HEADERS = {'User-Agent': '', 'Accept-Language': 'en-IN, en;q=0.5'}
    URL = f"https://www.flipkart.com/search?q={search_query.replace(' ', '+')}"
    webpage = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(webpage.content, "html.parser")
    products = soup.find_all("a", class_="CGtC98")

    final_list1 = []
    executor = ThreadPoolExecutor(max_workers=50)
    for product in products:
        product_link = "https://www.flipkart.com" + product["href"]
        executor.submit(get_product_details1, product_link)
    executor.shutdown(wait=True)        

    # Print number of items fetched
    print(f"Number of items fetched: {len(final_list1)}")

    new_list = []
    final_list.extend(final_list1)
    for i in final_list:
        if i["price"] == 0:
            print("skipped")
            continue
        new_list.append(i)
    new_list.sort( key=lambda x: x["price"])
    return jsonify(new_list)

if __name__ == '__main__':
    app.run(debug=True)


