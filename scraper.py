import requests
from bs4 import BeautifulSoup
import string
import os


class Parser:

    def __init__(self, pages: int, article: str):
        self.pages = pages
        self.article = article
        self.pages_count = 1
        self.schema = 'https://www.nature.com'

    def get_urls(self):
        my_list = ['https://www.nature.com/nature/articles?year=2020']
        for i in range(2, self.pages+1):
            my_list.append(f'https://www.nature.com/nature/articles?searchType=journalSearch&sort=PubDate&year=2020&page={i}')
        return my_list

    @staticmethod
    def get_response(url):
        response = requests.get(url)
        return response.text

    @staticmethod
    def soup(response):
        soup = BeautifulSoup(response, 'html.parser')
        return soup

    def get_hrefs(self, soup):
        span = soup.find_all('span', 'c-meta__type', string=self.article)
        hrefs_list = []
        for i in span:
            hrefs_list.append(i.find_parent('article').find('a').get('href'))
        return hrefs_list

    def get_text_from_href(self, href_list):
        dict_for_files = {}
        for i in href_list:
            response = requests.get(self.schema + i)
            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.find('h1').text.strip()
            article_teaser = soup.find('p', 'article__teaser').text.strip()
            dict_for_files[title] = article_teaser
        return dict_for_files

    def save_file(self, dict_for_file):
        folder = f'Page_{self.pages_count}'
        os.makedirs(folder, exist_ok=True)
        translator = str.maketrans(' ', '_', string.punctuation)
        for k, v in dict_for_file.items():
            file_path = os.path.join(folder, k.translate(translator))
            print(v)
            with open(f'{file_path}.txt', 'wb', ) as my_file:
                my_file.write(v.encode('utf-8'))
        self.pages_count += 1

    def start_pars(self):
        urls_list = self.get_urls()
        for i in urls_list:
            url = self.get_response(i)
            soup = self.soup(url)
            hrefs_list = self.get_hrefs(soup)
            dict_for_files = self.get_text_from_href(hrefs_list)
            self.save_file(dict_for_files)


def main():
    pages = int(input())
    article = input()
    parser = Parser(pages, article)
    parser.start_pars()


if __name__ == '__main__':
    main()
