"""Scrapes AO3 for data."""

import aiohttp
import asyncio
import requests as req
from bs4 import BeautifulSoup

BASE_URL = "https://archiveofourown.org/works/search?commit=Search&page="
QUERY_PARAMETERS = "&work_search%5Bhits%5D=&work_search%5Bkudos_count%5D=&work_search%5Blanguage_id%5D=&work_search%5Bquery%5D=&work_search%5Brating_ids%5D=&work_search%5Brelationship_names%5D=&work_search%5Brevised_at%5D=&work_search%5Bsingle_chapter%5D=0&work_search%5Bsort_column%5D=created_at&work_search%5Bsort_direction%5D=desc&work_search%5Btitle%5D=&work_search%5Bword_count%5D="


def return_outer_divs(whole_page: BeautifulSoup) -> tuple:
    """Returns the two main divs separately."""

    meta_div = whole_page.find("dl", {"class": "work meta group"})
    preface_div = whole_page.find("div", {"class": "preface group"})

    return meta_div, preface_div


def return_all_tags(dd: BeautifulSoup) -> list[str]:
    """Given a HTML dd object, returns all tag texts inside of it."""

    tags = dd.find_all("a", {"class": "tag"})

    return [tag.text for tag in tags]


def extract_from_meta_div(meta_div: BeautifulSoup) -> dict:
    """Extracts metadata from the relevant div."""

    list_dds = ["fandom", "relationship", "additional", "character"]

    field_names = meta_div.find_all("dt")
    field_values = meta_div.find_all("dd")

    fields_zipped = list(zip([f.text.strip().lower() for f in field_names],
                             field_values))

    metadata = {}
    for i in range(0, len(fields_zipped)):

        if any(list_dd in fields_zipped[i][0] for list_dd in list_dds):
            metadata[fields_zipped[i][0]] = return_all_tags(
                fields_zipped[i][1])
        else:
            metadata[fields_zipped[i][0]] = fields_zipped[i][1].text.strip()

    return metadata


def extract_from_preface_div(preface_div: BeautifulSoup) -> dict:
    """Extracts ONLY the fanfic name and author."""

    return {
        "title": preface_div.find("h2").text.strip(),
        "author": preface_div.find("h3").text.strip()
    }


async def scrape_one_single_work(session, fanfic_id: str) -> dict:
    """Scrapes a single work."""

    url = f"https://archiveofourown.org/works/{fanfic_id}/"

    async with session.get(url) as res:

        print("work", res.status)

        html = await res.text()

        soup = BeautifulSoup(html, "html.parser")

        meta, preface = return_outer_divs(soup)

        data = extract_from_meta_div(meta)
        preface_data = extract_from_preface_div(preface)

        data.update(preface_data)

        return data


async def scrape_works(work_ids: list) -> list:
    """Asynchronously scrapes all the works on a page."""

    async with aiohttp.ClientSession() as session:
        tasks = [scrape_one_single_work(session, work_id)
                 for work_id in work_ids]
        results = await asyncio.gather(*tasks)
        return results


async def scrape_one_page(session, page_url: str) -> list:
    """Scrape an entire results page, return URLS of all results."""
    async with session.get(page_url) as res:
        print("page", res.status)
        html = await res.text()
        soup = BeautifulSoup(html, "html.parser")

        work_blocks = soup.find("ol").find_all("li", {"class": "work"})

        return [block.attrs["id"][5:]
                for block in work_blocks]


async def scrape_pages(num_pages: int = 1) -> list:
    """Scrapes a number of the most recent works on AO3."""
    async with aiohttp.ClientSession() as session:
        tasks = [scrape_one_page(session, f"{BASE_URL}{str(i)}{QUERY_PARAMETERS}")
                 for i in range(1, num_pages+1)]
        results = await asyncio.gather(*tasks)
        return [item for page_urls in results for item in page_urls]


async def extract(num_pages: int = 1) -> list:
    """The main function."""
    work_ids = await scrape_pages(num_pages)
    return await scrape_works(work_ids)


if __name__ == "__main__":
    print(asyncio.run(extract(2)))
