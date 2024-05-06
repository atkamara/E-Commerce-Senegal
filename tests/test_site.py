from falcon.Site import MainSite,MultipleSites
from os import path
from scrapy import Selector
from scrapy import Spider
from scrapy.crawler import CrawlerProcess

def page_dir(name):
    extension = 'html'
    root = 'file://'+path.dirname(path.realpath(__file__))
    project = 'src/falcon'
    asset = 'assets'
    file_dir = path.join(
                         '/'.join(root.split('/')[:-1]), 
                         project, 
                         asset, f'{name}.{extension}')
    return file_dir
def test_MainSite_instance():
    start_urls = [page_dir('p1')]
    ms = MainSite('p1',start_urls,follow=False)
    assert ms.__class__.__name__ == 'MainSite'
def test_MainSite_spider_attr():
    start_urls = [page_dir('p1')]
    ms = MainSite('p1',start_urls,follow=False)
    spider = ms.spider
    assert issubclass(spider,Spider)
def test_Run_Spider():
    start_urls = [page_dir('p1')]
    ms = MainSite('p1',start_urls,follow=False)
    spider = ms.spider
    process = CrawlerProcess()
    process.crawl(spider)
    process.start() 
    res = process