
import argparse
import itertools
import json
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import random


REQUEST_HEADER = {
    'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"
}

IMAGES_DIR = '../images/'

class ImageScraper(object):

    def __init__(self, upc):
        self.upc = upc
        self.image = ''
        self.image_type = ''

    def get_soup(self, url, header):
        response = urlopen(Request(url, headers=header))
        return BeautifulSoup(response, 'html.parser')

    def get_query_url(self, query):
        return "https://www.google.com/search?q=%s&source=lnms&tbm=isch" % query

    def extract_images_from_soup(self, soup):
        image_elements = soup.find_all("div", {"class": "rg_meta"})
        metadata_dicts = (json.loads(e.text) for e in image_elements)
        link_type_records = ((d["ou"], d["ity"]) for d in metadata_dicts)
        return link_type_records

    def extract_images(self, query, num_images):
        url = self.get_query_url(query)
        print("Souping")
        soup = self.get_soup(url, REQUEST_HEADER)
        print("Extracting image urls")
        link_type_records = self.extract_images_from_soup(soup)
        return itertools.islice(link_type_records, num_images)

    def get_raw_image(self, url):
        req = Request(url, headers=REQUEST_HEADER)
        resp = urlopen(req)
        return resp.read()

    def write_image(self):
        output = open(
            IMAGES_DIR + str(random.randint(1, 10000)) + '.' + self.image_type,
            "wb"
        )
        output.write(self.image)
        output.close()

    def download_images_to_dir(self, images, num_images):
        for i, (url, image_type) in enumerate(images):
            try:
                print("Making request (%d/%d): %s", i, num_images, url)
                self.image = self.get_raw_image(url)
                self.image_type = image_type or 'jpg'
                self.write_image()
            except Exception as e:
                print(e)

    def run(self, query, num_images=1):
        query = '+'.join(query.split())
        print("Extracting image links")
        images = self.extract_images(query, num_images)
        print("Downloading images")
        self.download_images_to_dir(images, num_images)
        print("Finished")

    def scrape(self):
        parser = argparse.ArgumentParser(description='Scrape Google images')
        parser.add_argument('-s', '--search', default=self.upc, type=str, help='search term')
        parser.add_argument('-n', '--num_images', default=1000, type=int, help='num images to save')
        parser.add_argument('-f', '--file', type=str, help='garbage')

        args = parser.parse_args()

        self.run(args.search, args.num_images)


imgObj = ImageScraper('Alec Baldwin')
imgObj.scrape()
