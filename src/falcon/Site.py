"""
Main Module
This module defines classes representing websites and multiple websites.
Classes:
    MainSite: Represents a main website with attributes and methods for web crawling.
    MultipleSites: Represents multiple websites with methods for iteration and retrieval.
Example:
    >>> sites_data = {
    ...     'Site1': {'start_urls': ['url1', 'url2']},
    ...     'Site2': {'start_urls': ['url3', 'url4']}
    ... }
    >>> multiple_sites = MultipleSites(sites=sites_data, db='database_connection_string')
    >>> for site in multiple_sites:
    ...     print(site.name)
    ...
    'Site1'
    'Site2'
"""
from functools import cached_property
from .Model import Site
from .Page import MainPage
class MainSite(Site):
    """
    A class representing a main website.
    Attributes:
        name (str): The name of the main website.
        start_urls (list): A list of starting URLs for the web crawler.
        db (str, optional): The database connection string. Defaults to None.
    Methods:
        __init__: Initializes a MainSite object with the provided attributes.
    """
    def __init__(self,
                 name,
                 start_urls,
                 db=None,
                 follow=True) -> None:
        """
        Initializes a MainSite object.
        Args:
            name (str): The name of the main website.
            start_urls (list): A list of starting URLs for the web crawler.
            db (str, optional): The database connection string. Defaults to None.
        """
        self.name: str = name
        self.start_urls: list = start_urls
        self.pageclass = MainPage
        if db:
            self.Db: str = db
        self.follow = follow
class MultipleSites:
    """
    A class representing multiple websites.
    Attributes:
        loop_state (int): Current state of iteration.
        sites (dict): A dictionary containing lists of URLs for each website.
        db (str, optional): The database connection string. Defaults to None.
    Methods:
        site_names: A property to retrieve the names of all sites.
        __len__: Returns the number of sites.
        __iter__: Returns an iterator object.
        __next__: Returns the next site in iteration.
        __getitem__: Returns the MainSite object corresponding to the given index.
    """
    loop_state = 0
    def __init__(self, sites: list[dict]):
        self.sites = sites
    def __len__(self)->int:
        return len(self.sites)
    def __iter__(self):
        """
        Returns an iterator object.
        Returns:
            iterator: An iterator object.
        """
        return self
    def __next__(self):
        """
        Returns the next site in iteration.
        Returns:
            MainSite: The next MainSite object.
        Raises:
            StopIteration: If all sites have been iterated.
        """
        if self.loop_state < len(self):
            self.loop_state += 1
            return self[self.loop_state - 1]
        self.loop_state = 0
        raise StopIteration
    def __getitem__(self, ix):
        """
        Returns the MainSite object corresponding to the given index.
        Args:
            ix (int): The index of the MainSite object to retrieve.
        Returns:
            MainSite: The MainSite object at the specified index.
        """
        return MainSite((site:=self.sites[ix])[0],**site[1])
