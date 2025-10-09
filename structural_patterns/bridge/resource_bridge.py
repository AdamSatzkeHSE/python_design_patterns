""" Bridge pattern: When you want to share an implementation among multiple objects.
Basically, instead of implementing several specialized classes, defining all that is 
required within each class, you can define the following special components:

- An abstraction that applies to all the classes
- A separate interface for the different objects involved
"""
from abc import ABCMeta, abstractmethod
from urllib import request, parse

# Application where the user if going to manage and deliver content after fetching
# it from diverese sources.
# Instead of implementing several content classes, each holding the methods responsible
# for getting the content pieces, assembling them, and showing them inside the application.
# We can define an abstraction for the ResourceContent and separate interface for the objects
# that are responsible for fetching the content.

class ResourceContent:
    """ Define the abstraction's interface.
    Mantain a reference to an object which represents the Implementor.
    """
    def __init__(self, imp):
        self._imp = imp
    
    def show_content(self, path):
        self._imp.fetch(path)

""" As done so far, we define the equivalent of an interface in Python using two
features of the language, the metaclass feature (which helps define the type of a type),
and abstract base class (ABC)
"""
class ResourceContentFetcher(metaclass=ABCMeta):
    """Define the interface for implementation classes that fetch content
    """
    @abstractmethod
    def fetch(path):
        pass

# Now we can add an implementation class to fetch content from a web page or resource.
class URLFetcher(ResourceContentFetcher):
    """ Implement the Implementor interface and define its concrete implementation.
    """
    def fetch(self, path):
        # path is an URL
        req = request.Request(path)
        with request.urlopen(req) as response:
            if response.code == 200:
                the_page = response.read()
                print(the_page)

# We can also add an implementation class to fetch content from a file on the local file system.
class LocalFileFetcher(ResourceContentFetcher):
    """Implement the Implementor interface and define its concrete implementation
    """
    def fetch(self, path):
        # path is the filepath to a text file
        with open(path) as f:
            print(f.read())

# Test
url_fetcher = URLFetcher()
iface = ResourceContent(url_fetcher)
iface.show_content("http://python.org")
print("=============")
localfs_fetcher = LocalFileFetcher()
iface = ResourceContent(localfs_fetcher)
iface.show_content("file.txt")