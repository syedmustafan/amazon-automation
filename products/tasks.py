from celery import shared_task

from .models import Brand
from .scraper import scrape_products


@shared_task
def scrape_amazon():
    brands = Brand.objects.all()
    for brand in brands:
        scrape_products(brand)
