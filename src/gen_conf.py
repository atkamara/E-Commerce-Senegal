"""
Module for generating configuration data for web scraping.
Imports:
    lru_cache: Decorator to cache the results of function calls.
    product: Function to compute the Cartesian product of input iterables.
    re: Module providing support for regular expressions.
    configparser: Module to work with configuration files.
Attributes:
    config (ConfigParser): Configuration parser object.
    root (list): List containing the root XPath expression.
    FILE (str): Name of the configuration file.
Functions:
    write_config: Writes configuration data to a file.
    MainPage: Generates configuration data for the main page.
    get_relative: Computes relative XPath expressions.
    ProductTitle: Generates configuration data for product titles.
    PublishDate: Generates configuration data for publish dates.
    Contact: Generates configuration data for contact information.
    PublishLink: Generates configuration data for publish links.
    ProductPrice: Generates configuration data for product prices.
    VendorLocation: Generates configuration data for vendor locations.
"""
from functools import lru_cache
from itertools import product
import re
import configparser
# Configuration parser object
config = configparser.ConfigParser()
root = ['//']
FILE = 'css.ini'
def write_config(config, file, entity, **kwargs):
    """
    Writes configuration data to a file.
    Args:
        config (ConfigParser): Configuration parser object.
        file (str): Name of the file to write.
        entity (str): Name of the entity being configured.
        **kwargs: Additional keyword arguments representing configuration parameters.
    """
    config[entity] = dict(kwargs)
    with open(file, 'w+') as conf_file:
        config.write(conf_file)
@lru_cache(maxsize=None)
def get_relative(paths: tuple):
    """
    Computes relative XPath expressions.
    Args:
        paths (tuple): Tuple containing XPath expressions.
    Returns:
        list: List of relative XPath expressions.
    """
    return [
        re.sub(r'^\/+', 'descendant::', path)
        for path in paths
    ]
def MainPage():
    """
    Generates configuration data for the main page.
    """
    xpath0 = '//article[contains(@class,"item") and not(contains(@class,"cart"))]'
    div = "//div[{}]".format
    xpath1 = div(f'contains(@class,"list") and contains(@class,"item") ')
    xpath2 = div('@class="media panel panel-default"')
    xpaths = [xpath0, xpath1, xpath2]
    entity_name = 'MainPage'
    next_test = 'contains(@class,"next") or contains(@rel,"next")'
    entity = {
        'xpaths': xpaths,
        'next_xpaths': [
            f'//a[{next_test}]/@href',
            '//*[contains(@class,"next")]/a[1]/@href'
        ]
    }
    write_config(config, FILE, entity_name, **entity)
def ProductTitle():
    """
    Generates configuration data for product titles.
    """
    title = '{}[contains(@class,"title")][1]'.format
    header_tags = ['h2', 'h3', 'h4', 'h5', title('p'), title('div')]
    data = ['a[1]/@title', 'a[1]/text()', 'text()']
    xpaths = [*map('/'.join, product(root, header_tags, data))]
    relative_xpaths = get_relative(tuple(xpaths))
    entity_name = 'ProductTitle'
    entity = {'xpaths': xpaths,
              'relative_xpaths': relative_xpaths}
    write_config(config, FILE, entity_name, **entity)
def PublishDate():
    """
    Generates configuration data for publish dates.
    """
    div = 'div[contains(@class,"{}")]'.format
    date_tags = [div('date'), div('time')]
    data = ['text()', 'span[1]/text()']
    xpaths = [*map('/'.join, product(root, date_tags, data))] + [
        'span/@data-bs-content',
        'div[ class="media-body"]/p[1]/text()']
    relative_xpaths = get_relative(tuple(xpaths))
    entity_name = 'PublishDate'
    entity = {'xpaths': xpaths,
              'relative_xpaths': relative_xpaths}
    write_config(config, FILE, entity_name, **entity)
def Contact():
    """
    Generates configuration data for contact information.
    """
    types = [
        'tel',
        'sms',
        'whatsapp']
    xpaths = list(map(r'//a[starts-with(@href,"{}:")]/@href'.format, types))
    relative_xpaths = get_relative(tuple(xpaths))
    entity_name = 'Contact'
    entity = {'xpaths': xpaths,
              'relative_xpaths': relative_xpaths}
    write_config(config, FILE, entity_name, **entity)
def PublishLink():
    """
    Generates configuration data for publish links.
    """
    title = '{}[contains(@class,"title")][1]'.format
    header_tags = ['h2', 'h3', 'h4', 'h5', title('p'), title('div')]
    xpaths = [*map('/'.join, product(root, header_tags, ['a[1]/@href']))] + [
        '//a[contains(@class,listing)][1]/@href']
    relative_xpaths = get_relative(tuple(xpaths))
    entity_name = 'PublishLink'
    entity = {'xpaths': xpaths,
              'relative_xpaths': relative_xpaths}
    write_config(config, FILE, entity_name, **entity)
def ProductPrice():
    """
    Generates configuration data for product prices.
    """
    price_test1 = '[contains(@class,"price")]'
    price_test2 = '[contains(name(),"price")]'
    price_classes = (f"//*{price_test1}" + "{}").format
    xpaths = [
        price_classes('//text()'),
        price_classes('/text()'),
        f'//a/@*{price_test2}',
        '//h4[class="media-heading"]/span/text()']
    relative_xpaths = get_relative(tuple(xpaths))
    entity_name = 'ProductPrice'
    entity = {'xpaths': xpaths,
              'relative_xpaths': relative_xpaths}
    write_config(config, FILE, entity_name, **entity)
def VendorLocation():
    """
    Generates configuration data for vendor locations.
    """
    loc_tests = ['[contains(@class,"map")]', '[contains(@class,"location")]']
    icon_tags = ['i', 'svg']
    icon_text = ['/text']
    parent = ['/..']
    data = ['/descendant[2]/text()', '/text()']
    xpaths = list(map(''.join, product(root, icon_tags, loc_tests, parent, data))) + \
             list(map(''.join, product(root, icon_tags, icon_text, loc_tests, parent, data))) + [
                 '//img[contains(@src,"location")]/../text()']

    relative_xpaths = get_relative(tuple(xpaths))
    entity_name = 'VendorLocation'
    entity = {'xpaths': xpaths,
              'relative_xpaths': relative_xpaths}
    write_config(config, FILE, entity_name, **entity)
if __name__ == '__main__':
    MainPage()
    ProductTitle()
    PublishDate()
    Contact()
    PublishLink()
    ProductPrice()
    VendorLocation()
