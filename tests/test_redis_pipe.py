from os import path
from falcon.Site import MainSite,MultipleSites
from falcon.Con import RedisUser
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

CREDENTIALS = {'host':'localhost',
               'port':6379,
               'db':11, 
               'decode_responses':True}
        
def set_db(domain,category):
    return RedisUser(domain,category,root='Falcon-Test3',**CREDENTIALS)
def test_Run_Spider():
    start_urls = [page_dir('p1')]
    db = set_db('domain1','category1')
    ms = MainSite('p1',
                  start_urls,
                  db=db,
                  follow=False)
    spider = ms.spider
    process = CrawlerProcess()
    process.crawl(spider)
    process.start() 

def test_Run_SpiderMultisite():
    sites = [
            ((name:=f'p{i}'),
             {'start_urls':[page_dir(name)],
              'db':set_db(f'domain{i}',f'category{i}'),
              'follow':False})
            for i in range(1,8)]
    ms = MultipleSites(sites)
    process = CrawlerProcess()
    for site in ms:
        process.crawl(site.spider)
    process.start() 