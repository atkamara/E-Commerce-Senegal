"""
Module for testing the functionality of the falcon.Page.MainPage class.
Functions:
    load_page: Loads a page for testing.
    test_main_page_instance: Tests the instantiation of MainPage objects.
    test_main_page_len_attribute_overload: Tests the length attribute of MainPage objects.
    test_main_page_first_element: Tests accessing the first element of a MainPage object.
    test_main_page_next_page: Tests the next page attribute of MainPage objects.
    test_page_items_count: Tests the count of items on each page.
"""
from falcon.Page import MainPage
from os import path
from scrapy import Selector
def load_page(name):
    """
    Loads a page for testing.
    Args:
        name (str): The name of the page to load.
    Returns:
        Selector: A Selector object representing the loaded page.
    """
    extension = 'html'
    root = 'src'
    project = 'falcon'
    asset = 'assets'
    file = path.join(root, project, asset, f'{name}.{extension}')
    return Selector(text=open(file).read())
max_files = 7 
def test_main_page_instance():
    """
    Tests the instantiation of MainPage objects.
    """
    response = load_page('p1')
    p = MainPage(response)
    assert isinstance(p, MainPage)
def test_main_page_len_attribute_overload():
    """
    Tests the length attribute of MainPage objects.
    """
    response = load_page('p1')
    p = MainPage(response)
    l = len(p)
    assert l == 42
def test_main_page_first_element():
    """
    Tests accessing the first element of a MainPage object.
    """
    response = load_page('p1')
    p = MainPage(response)
    p2 = p[0]
    assert type(p[0]).__name__ == 'MainItem'
def test_main_page_next_page():
    """
    Tests the next page attribute of MainPage objects.
    """
    response = load_page('p1')
    p = MainPage(response)
    assert p.next
def test_page_items_count():
    """
    Tests the count of items on each page.
    """
    p = [len(MainPage(load_page('p%d' % d))) for d in range(1, 8)]
    assert p == [42, 33, 14, 46, 12, 21, 25]
