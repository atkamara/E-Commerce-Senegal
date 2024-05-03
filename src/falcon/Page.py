from .Model import Page
from .Item import MainItem
from .Css import MainCss


class MainPage(Page,MainCss):
    css = [
        'xpaths',
        'next_xpaths']
    def as_item(self,html):
        return MainItem.parse(html,method='relative_value')