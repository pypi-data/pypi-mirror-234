import importlib
from ciopath.gpath_list import PathList
from cioseq.sequence import Sequence

KNOWN_SCRAPERS = [
    "maya",
    "bifrost",
    "image_planes",
    "yeti",
    "mtoa",
    "mtoa_standins",
    "ocio",
    "vray",
    "redshift",
    "renderman",
    "xgen",
]


def doit(frame_sequence, scrapers=KNOWN_SCRAPERS, resolve=True):
    """
    Run scrapers.
    frame_sequence: list, range, or cioseq.sequence.Sequence object.
    Will be coerced to cioseq.sequence.Sequence 
    Exmples:
    
    * [1,2,3,4,5]
    * range(1,10,2)
    * Sequence.create("1-20,17,22-40x3")
    * Sequence.create(
        playbackOptions(q=True, min=True), 
        playbackOptions(q=True, max=True)
    )

    scrapers: list of scraper names. e.g. "maya", "bifrost", "image_planes",
    "yeti", "mtoa", "vray", "redshift", "renderman".

    The scraper filenames are of the form: "scrape_<scraper_name>.py". Users may
    write and add their own scrapers: Scrapers are discovered by attempting to
    import them. Therefore, they must be in the python path. The project's
    scripts directory for example is a valid scraper location since it's in the
    python path.

    You may also pass resolve=False. This is useful for
    debugging.
    
    Unresolved paths are paths found in the scene, but which haven't
    been resolved to files on disk. The paths may have glob characters in them,
    for example:

    * /path/to/images/shot_001/texture.*.exr - an exr sequence.

    Unresolved path dicts may also contain other fields, such as "plug" for
    example, which holds the attribute the path was found on.

    Returns: dict of amendments. e.g. {"paths":[...], "env":[...]}

    The env list is a list of dicts with keys "name", "value", "merge_policy".
    It's up to you to compile the environment.

    Example usage:
    ```
import pymel.core as pm
from ciomaya.lib import scrape_runner

result = scrape_runner.doit(range(1, 101))

print("-"*20,"PATHS","-"*20)
for p in result["paths"]:
    print(p)

print("-"*20,"ENV","-"*20)
for en in result["env"]:
    print(en)
    ```
    """
    

    sequence = Sequence.create(list(frame_sequence))

    amendments = {"paths": [], "env": []}

    for name in ["scrape_{}".format(s) for s in scrapers]:
        try:
            scraper_module = importlib.import_module(name)
            scraper_result = scraper_module.doit(sequence)
            if scraper_result:
                amendments["paths"] += scraper_result["paths"]
                amendments["env"] += scraper_result["env"]
        except BaseException:
            continue

    if not resolve:
        return amendments

    path_list = PathList()
    path_list.add(*[p["path"] for p in amendments["paths"]])
    path_list.real_files()
    amendments["paths"] = [{"path": p.fslash()} for p in path_list]

    return amendments
