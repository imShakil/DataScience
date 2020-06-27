from web_scraping.scraper import *
import csv
import time

headers = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) snap Chromium/83.0.4103.106 Chrome/83.0.4103.106 Safari/537.36"
training_keywords = ['করোনা', 'কোভিড-১৯', 'উহান-ভাইরাস']  # add keywords here


def store_in_csv(item):
    with open('data.csv', 'a+', newline='') as file:
        file_header = ['Title', 'Link']
        writer = csv.writer(file, file_header)
        writer.writerow(item)


def find_date_time(string):
    items = string.find_all('time')
    if len(items) > 0:
        for i in items:
            return i.get_text().strip()

    return ""


def print_only_corona_news(links):
    news_count = 0
    for link in links:
        news_link = get_valid_link(str(link.get('href')))
        title = link.get_text().strip()
        if news_link is None or len(title) <= 0:
            continue
        title_words = title.split()

        if set(training_keywords).intersection(set(title_words)):
            store_in_csv([title, news_link])
            news_count += 1
        else:
            metadata = scrape_url(news_link, headers).find_all('meta')
            for tag in metadata:
                if 'name' in tag.attrs.keys() and tag.attrs['name'].strip().lower() in ['keywords', 'description']:
                    sample_keywords = tag.attrs['content'].strip().split()
                    if set(training_keywords).intersection(set(sample_keywords)):
                        news_count += 1
                        # date = find_date_time(scrap_url(news_link, headers))
                        store_in_csv([title, news_link])

    return news_count


if __name__ == '__main__':
    start_time = time.time()
    total_news = 0
    with open('data.csv', 'w', newline='') as data:
        writer = csv.DictWriter(data, fieldnames=['Title', 'Link'])
        writer.writeheader()

    website_list = ["https://jamuna.tv", "https://bangla.bdnews24.com", "https://somoynews.tv", "https://prothomalo.com"]  # add target website URL here
    for web_url in website_list:
        soup = scrape_url(web_url, headers)
        all_links = soup.find_all('a')
        total_news += print_only_corona_news(all_links)
    print(f'Total {total_news} news collected')
    print(f'Total time spent: {time.time() - start_time} seconds')
