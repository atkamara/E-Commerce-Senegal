from .Model import Site
from .Page import MainPage
from functools import cached_property
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
    def __init__(self, name, start_urls, db=None,credentials={})->None:
        """
        Initializes a MainSite object.
        Args:
            name (str): The name of the main website.
            start_urls (list): A list of starting URLs for the web crawler.
            db (str, optional): The database connection string. Defaults to None.
        """
        self.name: str = name
        self.start_urls: list = start_urls
        self.Page = MainPage
        if db:
            self.db: str = db(**credentials) 
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
    sites: dict[dict]
    db : str = None
    @cached_property
    def site_names(self):
        """
        Property to retrieve the names of all sites.
        Returns:
            list: A list of site names.
        """
        return list(self.sites.keys())
    def __len__(self):
        """
        Returns the number of sites.
        Returns:
            int: The number of sites.
        """
        return len(sites)
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
            return self[self.loop_state-1]
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
        return MainSite((name:=self.site_names[ix]),
                        (args:=self.sites[name]).pop('start_urls'),
                         self.db,
                         args.get('credentials',{})
                         )
