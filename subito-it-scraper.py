#!/usr/bin/env python

import argparse
from bs4 import BeautifulSoup
import json
import re
import requests
import sys
import os

DB_FILENAME = "subito-it-scraper.json"


class Entry:
    def __init__(self, _title, _price, _url, _location):
        self.title = _title
        self.price = _price
        self.url = _url
        self.location = _location

    def __str__(self):
        output = self.title + "\n"
        output += str(self.price) + "€ \n"
        output += str(self.location) + "\n"
        output += str(self.url)
        return output

    def export_to_dictionary(self):
        data = {
            "title": self.title,
            "price": self.price,
            "url": self.url,
            "location": self.location
        }
        return data

    def __eq__(self, other):
        return self.url == other.url

    def __lt__(self, other):
        return self.price < other.price


class WebParser:
    def __init__(self, _url):
        self.headers = {
            "Accept": '"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8"',
            "Accept-Encoding": '"gzip, deflate"',
            "Accept-Language": '"en-US,en;q=0.5"',
            "Connection": '"keep-alive"',
            "Sec-Ch-Ua": '"Chromium";v="128", "Not;A=Brand";v="24", "Brave";v="128"',
            "Sec-Ch-Ua-Mobile": '"?0"',
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": '"document"',
            "Sec-Fetch-Mode": '"navigate"',
            "Sec-Fetch-Site": '"none"',
            "Sec-Fetch-User": '"?1"',
            "Sec-Gpc": '"1"',
            "Upgrade-Insecure-Requests": '"1"',
            "User-Agent": '"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"'
        }
        self.url = _url

    def fetch_all_entries(self):
        page = requests.get(self.url, headers=self.headers)
        soup = BeautifulSoup(page.text, 'html.parser')
        html_items_list = soup.find_all('div', class_=re.compile(r'item-card'))
        entry_list = list()

        for item in html_items_list:

            # Skip sold items
            sold = self.parse_sold(item)
            if sold is not None:
                continue

            # Parse item data
            title = self.parse_title(item)
            price = self.parse_price(item)
            url = self.parse_url(item)
            location = self.parse_location(item)

            # Add item into the list
            entry_list.append(Entry(title, price, url, location))

        return entry_list

    def parse_title(self, item):
        return item.find('h2').string

    def parse_price(self, item):
        try:
            price = item.find('p', class_=re.compile(r'price')).contents[0]
            price = int(price.replace('.', '')[:-2])
        except Exception:
            price = None
        return price

    def parse_url(self, item):
        return item.find('a').get('href')

    def parse_sold(self, item):
        return item.find('span', re.compile(r'item-sold-badge'))

    def parse_location(self, item):
        try:
            location = item.find('span', re.compile(r'town')).string
            location += item.find('span', re.compile(r'city')).string
        except Exception:
            location = "Unknown"

        return location


class Query:
    def __init__(self, _name, _url,  _min_price, _max_price):
        self.name = _name
        self.url = _url
        self.min_price = _min_price
        self.max_price = _max_price
        self.entries = list()

    def is_price_in_range(self, price):
        return (price >= self.min_price) and (price <= self.max_price)

    def run(self):
        parser = WebParser(self.url)
        new_entries = list()

        # Fetch the new entries list
        for entry in parser.fetch_all_entries():
            if self.is_price_in_range(entry.price):
                new_entries.append(entry)

        # Add new entries to current list
        for entry in new_entries:
            if entry not in self.entries:
                self.entries.append(entry)
                print(f"Added entry -> {entry.price}€ {entry.title}")

        # Removed sold items
        for entry in self.entries:
            if entry not in new_entries:
                self.entries.remove(entry)
                print(
                    f"Removed entry \"{entry.price}€ {entry.title}\" because probably sold")

        self.entries.sort()

    def to_dict(self):
        data = {
            "name": self.name,
            "url": self.url,
            "min_price": self.min_price,
            "max_price": self.max_price,
            "entries": list()
        }

        for entry in self.entries:
            data["entries"].append(entry.export_to_dictionary())

        return data

    def __eq__(self, other):
        return self.url == other.url

    def __str__(self):
        out = f"Query: {self.name}"
        out += f"          Minimum price: {self.min_price}"
        out += f"          Maximum price: {self.max_price}\n"
        out += f"URL: {self.url}\n\n"
        for entry in self.entries:
            out += f"{entry.price}€ {entry.title} - {entry.location}\n"
            out += f"{entry.url}\n\n"
        out = out[:-2]
        return out


class Database:
    def __init__(self, _db_filename):
        self.db_filename = _db_filename
        self.queries = list()

    def read(self):
        try:
            with open(self.db_filename) as file:
                data = json.load(file)
        except json.JSONDecodeError as e:
            sys.exit(f"Error while parsing \"{self.db_filename}\":\n  {e}")
        except FileNotFoundError:
            self.save()
            return

        for json_query in data["queries"]:
            query = Query(
                json_query["name"],
                json_query["url"],
                json_query["min_price"],
                json_query["max_price"]
            )

            entry_list = list()
            for json_entry in json_query["entries"]:
                entry = Entry(
                    json_entry["title"],
                    json_entry["price"],
                    json_entry["url"],
                    json_entry["location"]
                )
                entry_list.append(entry)
            query.entries = entry_list

            self.queries.append(query)

    def update(self):
        for query in self.queries:
            query.run()

    def add(self, query):
        if query not in self.queries:
            query.run()
            self.queries.append(query)
        else:
            print(f"Query with url \"{query.url}\" already in the database")

    def remove(self, name):
        index_remove_query = -1
        for index, query in enumerate(self.queries):
            if query.name == name:
                index_remove_query = index

        if index_remove_query == -1:
            print(f"Query \"{name}\" not found, aborting.")
        else:
            self.queries.pop(index_remove_query)
            print(f"Query \"{name}\" removed.")

    def save(self):
        data = {"queries": list()}
        for query in self.queries:
            data["queries"].append(query.to_dict())

        with open(self.db_filename, "w") as file:
            file.write(json.dumps(data, indent=4))


def argparse_setup():
    parser = argparse.ArgumentParser(prog='subito-it-scraper',
                                     description="Item tracker for subito.it website. \
                                     Run without flag will update current queries.")
    parser.add_argument('-a', '--add', nargs=2, metavar=("NAME", "URL"),
                        help="Name and url of the query to be added in the database.")
    parser.add_argument('--min-price', type=int, nargs='?', default=-1,
                        help="Minimum price for a query to be added to the database")
    parser.add_argument('--max-price', type=int, nargs='?', default=sys.maxsize,
                        help="Maximum price for a query to be added to the database")
    parser.add_argument('-l', '--list', action='store_true',
                        help="List all queries in the database")
    parser.add_argument('-r', '--remove', metavar="NAME",
                        help="Remove a query from the database")
    return parser.parse_args()


def get_database_path():
    if os.environ.get("XDG_CONFIG_HOME"):
        path = os.environ.get("XDG_CONFIG_HOME")
    elif os.environ.get("HOME"):
        path = os.environ.get("HOME") + "/.config"
    else:
        sys.exit("Error: Can't find $XDG_CONFIG_HOME nor $HOME/.config")
    return path


if __name__ == "__main__":

    args = argparse_setup()

    path = get_database_path()
    db_path = path + '/' + DB_FILENAME

    db = Database(db_path)
    db.read()

    if args.remove:
        db.remove(args.remove)
    if args.list:
        for query in db.queries:
            print(query)
    if args.add:
        name, url = args.add
        query = Query(name, url, args.min_price, args.max_price)
        db.add(query)
    else:
        db.update()

    db.save()
