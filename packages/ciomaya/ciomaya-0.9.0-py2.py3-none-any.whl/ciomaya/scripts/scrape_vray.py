"""
A scraper to collect paths for Vray.
"""
from __future__ import unicode_literals
from ciomaya.lib import scraper_utils



ATTRS = {
    "vray": {
        "VRayMesh": [
            "fileName"
        ],
        "VRaySettingsNode": [
            "ifile",
            "fnm"
        ],
        "VRayVolumeGrid": [
            "inFile",
            "inPath",
        ],
        "VRayScene": [
            "FilePath"
        ]
    }
}

# See https://docs.chaosgroup.com/display/VMAYA/File+Names+for+Bitmap+Textures
TOKENS = (r"<UDIM>", r"<UVTILE>", r"<frameNum>", r"<TileRef>",
          r"\$\d*U.*\$\d*V", r"u<U>_v<V>", r"u<U>_v<V>_<f>", r"#+")


def run(_):
    return doit()


def doit(_=None):
    paths = scraper_utils.get_paths(ATTRS)
    paths = scraper_utils.starize_tokens(paths, *TOKENS)
    paths = scraper_utils.expand_workspace(paths)
    return {"paths":paths, "env":[]}
