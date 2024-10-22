# Amazon Brand Automation

This project is a web application designed to scrape brand data from Amazon. It utilizes Django as the backend framework, Django Rest Framework for API endpoints, and Celery for task scheduling. The application is designed to run scrapers at regular intervals and provide an admin panel for managing brands and products.

## Table of Contents

- [Installation](#installation)
- [Requirements](#requirements)
- [Database Migration](#database-migration)
- [Creating a Superuser](#creating-a-superuser)
- [Running the Development Server](#running-the-development-server)
- [Adding Brands](#adding-brands)
- [Task Scheduling](#task-scheduling)
- [Celery Commands](#celery-commands)
- [Logging and Caching](#logging-and-caching)
- [API Endpoints](#api-endpoints)
- [Scraping Features](#scraping-features)



## Installation Guide

## Set up a Virtual Environment (optional but recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

```


## Requirements

This project requires Python 3.x. All dependencies are listed in the `requirements.txt` file. You can install the required packages using:

```bash
pip install -r requirements.txt

```



## Database Migration

After installing the requirements, navigate to the project directory where manage.py is located and run the following commands to migrate the database tables:

```bash
python manage.py migrate
python manage.py migrate django_celery_results
python manage.py migrate django_celery_beat

```



## Creating a Superuser

To access the admin panel, create a superuser account:

```bash
python manage.py createsuperuser

```
You will be prompted to enter a username and password.




## Running the Development Server

Start the Django development server with the following command:

```bash
python manage.py runserver
```
Once the server is running, you can access the admin panel at:

```bash
http://127.0.0.1:8000/admin

```



## Adding Brands

In the admin panel, you can add brands and their corresponding Amazon URLs. When adding a brand, format the URL as follows:

```bash
https://www.amazon.com/{{brand_name}}-products/s?k={{brand_name}}+products

```
After adding a brand, wait for the scheduler to run and scrape all the data for the brand.



## Task Scheduling

The scraper task runs every 6 hours (4 times a day). Ensure that you have the Redis server, Celery workers, and Celery Beat running.




## Celery Commands to run Scheduling

To manage task scheduling and worker processes, you need to run the following commands:

### 1. Start the Redis Server

```bash
redis-server

```



### 2. Run the Celery Worker:

```bash
celery -A amazon_scrape worker -l info

```

### 3. Run the Celery Beat Scheduler:

```bash
celery -A amazon_scrape beat -l info

```
You can also update the time for the cron by updating in the follwoing peice of code in settings.py. If you want to run every 5 minutes you can change it to:

```bash
CELERY_BEAT_SCHEDULE = {
    'scrape_amazon': {
        'task': 'products.tasks.scrape_amazon',
        'schedule': crontab(minute='*/5'),
    },
}

```



## Logging and Caching

The application utilizes logging to track scraping activities and errors. The logging configuration is set to log messages in scraping.log.

File-based caching is used to minimize redundant scraping efforts, improving performance and reducing the load on the scraping target.




## API Endpoints

The application provides two API endpoints:

### 1. Get Product Data for a Brand
- **Endpoint:** `/api/brands/{brand_id}/products/`
- **Method:** `GET`

### 2. Search Products by Name
- **Endpoint:** `/api/products/search/`
- **Method:** `GET`
- **Query Parameters:** 
  - `name` (string)




## Scraping Features

The project includes advanced scraping features, including:

- **Retries** for scraping requests
- **Anti-scraping measures** (user agents)
- **CAPTCHA handling**
- **Error and info logging**
- **File-based caching** for efficiency

