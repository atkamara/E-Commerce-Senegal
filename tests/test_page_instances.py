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
    p2 = p[0].dataclass
    assert type(p[0]).__name__ == 'MappedData'
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
    assert p == [42, 32, 11, 44, 12, 21, 25]
def test_main_page_items_to_dict():
    """
    Tests the items of MainPage objects.
    """
    response = load_page('p1')
    p0 = MainPage(response)[0]
    assert isinstance(p0.to_dict(),dict)
def test_main_page2_instance():
    """
    Tests the instantiation of MainPage objects.
    """
    response = load_page('p4')
    p = MainPage(response)
    contact = p[0].dataclass.Contact
    assert isinstance(p, MainPage)