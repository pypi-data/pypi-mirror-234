
"""
Singleton that allows us to cache an asset scrape.
"""

import importlib
from ciopath.gpath_list import PathList
from ciomaya.lib import scraper_utils


__data__ = None
__missing_paths__ = []

def data(node):
    """
    Cached list of assets. 
    
    This is used by the validator to avoid repeatedly scraping assets for each layer.
    """
    global __data__
    global __missing_paths__

    if __data__:
        return __data__

    scraper_scripts = []
    attr = node.attr("assetScrapers")
    for attr_element in attr:
        if not attr_element.attr("assetScraperActive").get():
            continue
        script = attr_element.attr("assetScraperName").get().strip()
        if not script:
            continue
        scraper_scripts.append(script)

    amendments =  scraper_utils.run_scrapers(node, scraper_scripts)
    paths = [p["path"] for p in amendments["paths"] if p["path"].strip()]
    paths += [p for p in list(node.attr("extraAssets").get()) if p]
    __data__ = PathList(*paths)
    __missing_paths__ = __data__.real_files()
    return __data__


def clear():
    """Invalidate the cache."""
    global __data__
    global __missing_paths__
    __data__ = None
    __missing_paths__ = []

def missing_paths():
    """If the asset cache is populated, this will return the list of missing paths."""
    return __missing_paths__
