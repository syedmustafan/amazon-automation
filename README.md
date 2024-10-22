# Amazon Brand Automation

This project is a web application designed to scrape brand data from Amazon. It utilizes Django as the backend framework, Django Rest Framework for API endpoints, and Celery for task scheduling. The application is designed to run scrapers at regular intervals and provide an admin panel for managing brands and products.

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Database Migration](#database-migration)
- [Creating a Superuser](#creating-a-superuser)
- [Running the Development Server](#running-the-development-server)
- [Adding Brands](#adding-brands)
- [API Endpoints](#api-endpoints)
- [Task Scheduling](#task-scheduling)
- [Scraping Features](#scraping-features)
- [Celery Commands](#celery-commands)
- [Logging and Caching](#logging-and-caching)
- [Contributing](#contributing)
- [License](#license)

## Requirements

This project requires Python 3.x. All dependencies are listed in the `requirements.txt` file. You can install the required packages using:

```bash
pip install -r requirements.txt
