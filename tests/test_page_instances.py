from vacuum.Page import MainPage
from os import path
from scrapy import Selector

def load_page(name):
    extension = 'html'
    root = 'src'
    project = 'vacuum'
    asset = 'assets'
    file = path.join(root,project,asset,f'{name}.{extension}')
    return Selector(text=open(file).read())

max_files = 7 

def test_main_page_instance():
    response = load_page('p1')
    p = MainPage(response)
    assert isinstance(p,MainPage)

def test_main_page_len_attribute_overload():
    response = load_page('p1')
    p = MainPage(response)
    l = len(p)
    assert l == 42
    
def test_main_page_first_element():
    response = load_page('p1')
    p = MainPage(response)
    p2 = p[0]
    assert type(p[0]).__name__ == 'MainItem'
    
def test_main_page_next_page():
    response = load_page('p1')
    p = MainPage(response)
    assert p.next
    
def test_page_items_count():
    p = [len(MainPage(load_page('p%d'%d))) for d in range(1,8)]
    assert p == [42, 33, 14, 46, 12, 21, 25]
    
def test_to_binary():
    test = lambda d : MainPage(load_page('p%d'%d)) >> 'test' 
    (*map(test,range(1,8)),)
    