import multiprocessing as mp
from urllib.request import urlopen, urljoin
from bs4 import BeautifulSoup
import re
import time


def crawl(url):
    response = urlopen(url)
    time.sleep(0.1)
    return response.read().decode()


def parse(base_url, html):
    soup = BeautifulSoup(html, 'lxml')
    urls = soup.find_all('a', {'href': re.compile('^/.+?/$')})
    title = soup.find('h1').get_text().strip()
    page_urls = set([urljoin(base_url, url['href']) for url in urls])
    url = soup.find('meta', {'property': "og:url"})['content']
    return title, page_urls, url


def main():
    base_url = 'https://morvanzhou.github.io/'
    # if base_url != "http://127.0.0.1:4000/":
    #     restricted_crawl = True
    # else:
    #     restricted_crawl = False

    unseen = set([base_url, ])
    seen = set()

    pool = mp.Pool(4)
    count, t1 = 1, time.time()

    while len(unseen) != 0:
        # if restricted_crawl and len(seen) > 20:
        #     break

        print('\nDistribute Crawling...')
        crawl_jobs = [pool.apply_async(crawl, args=(url,)) for url in unseen]
        htmls = [j.get() for j in crawl_jobs]  # request connection

        print('\nDistribute Parsing...')
        parse_jobs = [pool.apply_async(parse, args=(base_url, html)) for html in htmls]
        results = [j.get() for j in parse_jobs]

        print('\nAnalysing...')
        seen.update(unseen)
        unseen.clear()

        for title, page_urls, url in results:
            print(count, title, url)
            count += 1
            unseen.update(page_urls - seen)
    print('Total time: %.1f s' % (time.time() - t1,))


if __name__ == '__main__':
    main()
