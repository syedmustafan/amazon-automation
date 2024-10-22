import json
import logging
import random
import time
import urllib.parse

import requests
from bs4 import BeautifulSoup
from django.core.cache import cache  # Import cache from Django
from requests.exceptions import RequestException

from .models import Product

# Set up logging
logging.basicConfig(
    filename='scraping.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)


def load_user_agents(file_path='user-agent.txt'):
    """Load user agents from a file."""
    try:
        with open(file_path, 'r') as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        logging.error("User agent file not found.")
        return []


def get_random_user_agent():
    """Get a random user agent from the list."""
    user_agents = load_user_agents()
    return random.choice(user_agents)


def scrape_products(brand):
    """Scrape products from a brand's Amazon URL."""
    cache_key = f"products_{brand.id}"  # Create a cache key based on the brand ID
    cached_data = cache.get(cache_key)  # Check if data is cached

    if cached_data:
        logging.info(f"Data is already cached and saved in database for brand '{brand.name}'.")
        return

    base_url = brand.amazon_url
    next_page_url = base_url
    page_number = 1
    products_data = []

    while next_page_url:
        try:
            time.sleep(random.uniform(2, 6))  # Random delay to avoid detection
            response = fetch_page(next_page_url)

            if response:
                products_on_page = process_page(response, brand, page_number)
                products_data.extend(products_on_page)  # Collect products data
                next_page_url = get_next_page_url(response)
                page_number += 1
            else:
                next_page_url = None

        except RequestException as e:
            handle_request_exception(next_page_url, e)
            next_page_url = None

    # Cache the scraped data
    cache.set(cache_key, json.dumps(products_data), timeout=3600)  # Cache for 1 hour
    logging.info(f"Scraped and cached data for brand '{brand.name}'.")


def fetch_page(url):
    """Fetch a page from a URL and handle potential errors."""
    headers = {
        "User-Agent": get_random_user_agent(),
        'Accept-Language': 'da, en-gb, en',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Referer': 'https://www.google.com/'
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)

        # Check for CAPTCHA or rate limits
        if "captcha" in response.url or response.status_code == 503:
            logging.warning(f"CAPTCHA or rate limit encountered at {url}. Pausing.")
            time.sleep(random.uniform(60, 120))
            return None  # Indicate that the request should be retried

        response.raise_for_status()
        return response
    except RequestException as e:
        logging.error(f"Request failed for URL: {url}. Error: {e}")
        return None


def process_page(response, brand, page_number):
    """Extract products from the page and return the list of product data."""
    soup = BeautifulSoup(response.content, 'html.parser')
    all_products = soup.find_all("div", {"class": "sg-col-inner"})
    logging.info(f'Total products found on page {page_number} for brand "{brand.name}": {len(all_products)}')

    products_data = []  # List to store product data

    for item in all_products:
        product_data = extract_product_data(item)
        if product_data:
            products_data.append(product_data)  # Collect product data
            update_or_create_product(product_data, brand)

    return products_data  # Return the list of products for caching


def extract_product_data(item):
    """Extract product data from a single item."""
    sku = ""
    name = ""
    asin_value = ""
    image_url = ""

    names = item.find_all("span", {"class": "a-size-base-plus"})
    asin_div = item.find('div', {'data-csa-c-asin': True})
    data_attr = item.find('span', {'data-s-safe-ajax-modal-trigger': True})
    img_tag = item.find('img', {'class': 's-image'})

    if names:
        name = names[-1].text
    if asin_div:
        asin_value = asin_div['data-csa-c-asin']
    if img_tag and 'src' in img_tag.attrs:
        image_url = img_tag['src']
    if data_attr:
        sku = decode_sku(data_attr)

    if not (name or asin_value or sku or image_url):
        logging.info(f"Skipping product with missing fields. asin: {asin_value}, name: {name}")
        return None

    return {'name': name, 'sku': sku, 'asin': asin_value, 'image': image_url}


def decode_sku(data_attr):
    """Decode SKU from the data attribute."""
    try:
        data_json = json.loads(data_attr['data-s-safe-ajax-modal-trigger'])
        decoded_query = urllib.parse.unquote(data_json["ajaxUrl"])
        sku_json = json.loads(decoded_query.split("pl=")[1])
        return sku_json['adCreativeMetaData']['adCreativeDetails'][0]['adId']
    except (KeyError, IndexError, json.JSONDecodeError) as e:
        logging.error(f"Error decoding SKU: {e}")
        return ""


def update_or_create_product(product_data, brand):
    """Update or create a product in the database."""
    product_obj, created = Product.objects.update_or_create(
        asin=product_data['asin'],
        defaults={
            'name': product_data['name'],
            'sku': product_data['sku'],
            'image': product_data['image'],
            'brand': brand
        }
    )


def get_next_page_url(response):
    """Get the URL for the next page."""
    soup = BeautifulSoup(response.content, 'html.parser')
    next_button = soup.find("a", {"class": "s-pagination-next"})
    if next_button and 'href' in next_button.attrs:
        return "https://www.amazon.com" + next_button['href']
    return None  # No more pages


def handle_request_exception(url, exception):
    """Handle request exceptions with retries."""
    retries = 3  # Set number of retries
    while retries > 0:
        logging.info(f"Retrying... {retries} attempts left for URL: {url}")
        time.sleep(random.uniform(5, 10))  # Wait before retrying
        response = fetch_page(url)

        if response:
            return  # Successful response, exit retry loop

        retries -= 1

    logging.error(f"Max retries reached. Skipping URL: {url}.")
