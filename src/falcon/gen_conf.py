"""
This module contains functions to write configurations to a file using configparser based on the parameters passed to the functions. 

Functions:

    write_config(config, file, entity, **kwargs): 
      Writes configuration to the specified file for the given entity with the provided keyword arguments.

    Page(): 
      Defines xpaths and writes the configuration for a Page entity.

    get_relative(paths: tuple): 
      Returns a list of xpaths with 'descendant::' replacing leading slashes.

    ProductTitle(): 
      Defines xpaths and writes the configuration for a ProductTitle entity.

    PublishDate(): 
      Defines xpaths and writes the configuration for a PublishDate entity.

    Contact(): 
      Defines xpaths and writes the configuration for a Contact entity.

    PublishLink(): 
      Defines xpaths and writes the configuration for a PublishLink entity.

    ProductPrice(): 
      Defines xpaths and writes the configuration for a ProductPrice entity.

    VendorLocation(): 
      Defines xpaths and writes the configuration for a VendorLocation entity.
    """
from functools import lru_cache
from itertools import product
import re
import configparser

config = configparser.ConfigParser()
root=['//']
FILE = 'css.ini'

def write_config(config,file,entity,**kwargs):
  config[entity] = dict(kwargs)
  with open(file, 'w+') as cfile:
    config.write(cfile)
def MainPage():
    xpath0 = '//article[contains(@class,"item") and not(contains(@class,"cart"))]'
    div = "//div[{}]".format
    xpath1 = div(f'contains(@class,"list") and contains(@class,"item") ')
    xpath2 = div('@class="media panel panel-default"')
    xpaths = [xpath0,xpath1,xpath2]
    entity_name = 'MainPage'
    next_test = 'contains(@class,"next") or contains(@rel,"next")'
    entity = {
      'xpaths':xpaths,
    'next_xpaths' : [
        f'//a[{next_test}]/@href',
        '//*[contains(@class,"next")]/a[1]/@href'
        ]}
    write_config(config,FILE,entity_name,**entity)
@lru_cache(maxsize=None)
def get_relative(paths:tuple):
    return [
        re.sub(r'^\/+','descendant::',path)
        for path in paths
    ]
def ProductTitle():
    title = '{}[contains(@class,"title")][1]'.format
    header_tags = ['h2','h3','h4','h5',title('p'),title('div')]
    data = ['a[1]/@title','a[1]/text()','text()']
    xpaths = [*map('/'.join,product(root,header_tags,data))]
    relative_xpaths = get_relative(tuple(xpaths))
    entity_name = 'ProductTitle'
    entity = {'xpaths' : xpaths,
    'relative_xpaths' : relative_xpaths}
    write_config(config,FILE,entity_name,**entity)
def PublishDate():
    div = 'div[contains(@class,"{}")]'.format
    date_tags = [div('date'),div('time')]
    data = ['text()','span[1]/text()']
    xpaths = [*map('/'.join,product(root,date_tags,data))]+[
        'span/@data-bs-content',
        'div[ class="media-body"]/p[1]/text()']
    relative_xpaths = get_relative(tuple(xpaths))
    entity_name = 'PublishDate'
    entity = {'xpaths' : xpaths,
    'relative_xpaths' : relative_xpaths}
    write_config(config,FILE,entity_name,**entity)
def Contact():
    types = [
        'tel',
        'sms',
        'whatsapp']
    xpaths = list(map(r'//a[starts-with(@href,"{}:")]/@href'.format,types))
    relative_xpaths = get_relative(tuple(xpaths))
    entity_name = 'Contact'
    entity = {'xpaths' : xpaths,
    'relative_xpaths' : relative_xpaths}
    write_config(config,FILE,entity_name,**entity)
def PublishLink():
    title = '{}[contains(@class,"title")][1]'.format
    header_tags = ['h2','h3','h4','h5',title('p'),title('div')]
    xpaths =[*map('/'.join,product(root,header_tags,['a[1]/@href']))]+['//a[contains(@class,listing)][1]/@href']
    relative_xpaths = get_relative(tuple(xpaths))
    entity_name = 'PublishLink'
    entity = {'xpaths' : xpaths,
    'relative_xpaths' : relative_xpaths}
    write_config(config,FILE,entity_name,**entity)
def ProductPrice():
    price_test1 = '[contains(@class,"price")]'
    price_test2 = '[contains(name(),"price")]'
    price_classes = (f"//*{price_test1}"+"{}").format
    xpaths =[
        price_classes('//text()'),
        price_classes('/text()'),
        f'//a/@*{price_test2}',
        '//h4[class="media-heading"]/span/text()']
    relative_xpaths = get_relative(tuple(xpaths))
    entity_name = 'ProductPrice'
    entity = {'xpaths' : xpaths,
    'relative_xpaths' : relative_xpaths}
    write_config(config,FILE,entity_name,**entity)
def VendorLocation():
    loc_tests = ['[contains(@class,"map")]','[contains(@class,"location")]']
    icon_tags = ['i','svg']
    icon_text = ['/text']
    parent = ['/..']
    data = ['/descendant[2]/text()','/text()']
    xpaths = list(map(''.join,product(root,icon_tags,loc_tests,parent,data)))+\
             list(map(''.join,product(root,icon_tags,icon_text,loc_tests,parent,data)))+[
            '//img[contains(@src,"location")]/../text()']
    relative_xpaths = get_relative(tuple(xpaths))
    entity_name = 'VendorLocation'
    entity = {'xpaths' : xpaths,
    'relative_xpaths' : relative_xpaths}
    write_config(config,FILE,entity_name,**entity)
if __name__ =='__main__':
  MainPage()
  ProductTitle()
  PublishDate()
  Contact()
  PublishLink()
  ProductPrice()
  VendorLocation()