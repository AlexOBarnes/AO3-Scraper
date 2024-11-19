"""Scrapes AO3 for data."""

import requests as req
from bs4 import BeautifulSoup


if __name__ == "__main__":

    res = req.get(
        "https://archiveofourown.org/works/51671989/")
    html = res.text

    soup = BeautifulSoup(html)
