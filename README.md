# Subito.it scraper

A python script that scrape subito.it items and tracks them.

Inspired from
[subito-it-searcher](https://github.com/morrolinux/subito-it-searcher).

### Install

<details>
<summary>
Manual
</summary>

The required python libraries are:

- requests
- beautifulsoup4
- regex

which are also listed in `requirements.txt`.

An example of installation in a virtual environment could be as follow

```
git clone https://github.com/its-fonsy/subito-it-scraper.git
cd subito-it-scraper
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python ./subito-it-scraper.py -v
```
</details>

<details>
<summary>
Archlinux
</summary>

Archlinux users can use the `PKGBUILD` in the current repository to install the
required libraries and the script

```
git clone https://github.com/its-fonsy/subito-it-scraper.git
cd subito-it-scraper
makepkg -si
```
</details>

**Note**: a database named `subito-it-scraper.json` is saved inside
`$XDG_CONFIG_HOME` or `$HOME/.config`, ensure that at least on of the
environment variable is set and the folder exists.

### Usage examples

Navigate to [subito.it](www.subito.it) and search for the item to track.
Then copy the URL and use the script as follow
```
# Add a query
subito-it-scraper -a "iPhone" "https://www.subito.it/annunci-italia/vendita/usato/?q=iphone"

# Add a query with price range
subito-it-scraper -a "iPhone" "https://www.subito.it/annunci-italia/vendita/usato/?q=iphone" --min-price 100 --max-price 500

# List all the queries and their entries
subito-it-tracker -l

# Remove a query
subito-it-scraper -r "iPhone"

# Show help
subito-it-scraper -h
```
Once a query is added to the database its entries can be updated just by running
```
subito-it-tracker
```
