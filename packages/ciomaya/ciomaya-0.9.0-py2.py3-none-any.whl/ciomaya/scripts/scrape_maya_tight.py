"""
An experimental alternative to "scrape_maya".

NOTE: If you use this scraper, turn off the default Maya scraper.  If you don't, this scraper will
have no effect, other than to slow things down.

Unlike the standard Maya scraper, this scraper does not glob for file sequences. Instead, it
evaluates the frames for which files in a sequence are needed, and then generates the file names for
those frames. This is more efficient than globbing, in that it avoids uploading files that are not
needed. The scraping process may be a little slower, however, because it has to evaluate the frames.
"""

from __future__ import unicode_literals
from logging import root
import pymel.core as pm
import re
import glob
import copy
from ciomaya.lib import scraper_utils
from cioseq.sequence import Sequence

EXPERIMENTAL = True

ATTRS = {
    "AbcImport": {"AlembicNode": ["abc_File"]},
    "MayaBuiltin": {
        "file": ["computedFileTextureNamePattern"],
        "cacheFile": ["cachePath"],
        "gpuCache": ["cacheFileName"],
        "assemblyReference": ["definition"],
    },
    "Type": {"svgToPoly": ["svgFilepath"]},
    "Audio": {"audio": ["filename"]},
}

TILE_TOKENS = (
    r"_MAPID_",  # image_MAPID_.exr - mapid
    r"<UDIM>",  # image.<UDIM>.exr - udim_mari
    r"<UVTILE>",  # image.<UVTILE>.exr - udim_mudbox
    r"<TileRef>",  # Vray
    r"<tile>",  # Arnold tile
    r"<aov>",  # Arnold AOV
    r"\$\d*U.*\$\d*V",  # image.u$2U_v$2V.exr or image.u$Uv$V.exr, etc - udim_vray
    r"u<U>_v<V>",  # image.u<U>_v<V>.exr - udim_zbrush
    r"u<U>_v<V>_<f>",  # image.u<U>_v<V>_<f>.exr - udim_zbrush_f
)

FRAME_TOKENS = (
    r"#+",  # image.####.exr - hash
    r"%0\d+d",  # image.%04d.exr - percent
    r"<f\d?>",  # image.<f>.exr or image.<f4>.exr - frame_seq
    r"<FrameNum>",  # image.<FrameNum>.ext - Redshift
    r"<Frame>",  # image.<Frame>.ext - Redshift
)

TOKENS = TILE_TOKENS + FRAME_TOKENS

SEQUENCE_TOKENS = (r"<f>", r"#+")

BIGNUM = 999999999


def run(node):
    sequence = scraper_utils.get_sequence(node)
    return doit(sequence)


def doit(sequence):
    """
    Find paths in Maya attributes on Maya nodes.

    * Evaluate tokens in file.computedFileTextureNamePattern to the actual render range.
    * Replace any of the above tokens with a "*"
    * Add workspace.mel ([] signifies not required)
    * Make relativbe paths absolute.
    * Add tx equivalents of image files ([] signifies not required)
    * Add the main Maya file and references.

    Image file textures may have a sibling ".tx file".
    """

    paths = scraper_utils.get_paths(ATTRS)
    paths.extend(_get_assembly_assets())
    paths = evaluate_file_node_frames(sequence, paths)
    paths = scraper_utils.starize_tokens(paths, *TOKENS)
    paths.append({"path": "workspace.me[l]"})
    paths = scraper_utils.expand_workspace(paths)
    paths = scraper_utils.extend_with_tx_paths(paths)
    paths.extend(_get_scene_files())

    env = _get_env()

    return {"paths": paths, "env": env}


def evaluate_file_node_frames(sequence, paths):
    """
    Evaluate the frame range of file nodes.

    Args:
        submitter_node (str): name of the submitter node
        paths (list): list of paths to evaluate
    """

    result = []
    num_objects = len(paths)
    for obj_num, path_obj in enumerate(paths):
        if not type(pm.PyNode(path_obj["plug"]).node()) == pm.nt.File:
            result.append(path_obj)
            continue
        if (
            not pm.PyNode(path_obj["plug"]).attrName(longName=True)
            == "computedFileTextureNamePattern"
        ):
            result.append(path_obj)
            continue
        padding_info = _get_padding_info(path_obj)

        if not padding_info:
            result.append(path_obj)
            continue

        result += _generate_padded_filename_sequence(sequence, path_obj, padding_info)
    return result


def _get_padding_info(path):
    """
    Get frame information from a path.

    Args:
        path (str): path to evaluate
        *FRAME_TOKENS (str): tokens to evaluate

    Returns:
        dict: frame information
    """

    token_rx = re.compile("|".join(SEQUENCE_TOKENS), re.IGNORECASE)
    padding_info = {}
    if not ("path" in path and "plug" in path):
        return padding_info

    path["path"] = path["path"].replace("\\", "/")
    match = token_rx.search(path["path"])
    if not match:
        print("NO MATCH FOR: {}".format(path["path"]))
        return padding_info
    else:
        print("FOUND MATCH FOR: {}".format(path["path"]))

    result = _get_padding(path["path"])
    print("PADDING TUPLE: {}".format(result))
    if not result:
        return padding_info
    root, padding, ext = result
    return {"root": root, "padding": padding, "ext": ext}


def _get_padding(path):
    """
    Get padding information from a path.

    Args:
        path (str): path to evaluate

    To determine the padding we have to look on disk and find the shortest frame number for the
    path. We can't just look at the token because any indication of padding in the template is
    meaningless. Example f.####.exr will find f.10.exr.

    Returns:
        tuple: padding information  (root, padding, ext)
    """
    token_rx = re.compile("|".join(SEQUENCE_TOKENS), re.IGNORECASE)
    glob_pattern = token_rx.sub("*", path)

    existing = glob.glob(glob_pattern)
    if not existing:
        return None

    existing = [p.replace("\\", "/") for p in existing]

    parts = token_rx.split(path)
    if not len(parts) == 2:
        return None

    root, ext = parts

    frame_rx = re.compile(r"{}(\d+){}".format(root, ext))

    padding = BIGNUM

    num_existing = len(existing)
    for i, f in enumerate(existing):
        match = frame_rx.match(f)
        if match:
            p = len(match.group(1))
            if p < padding:
                padding = p
            if p == 1:
                break

    return None if padding == BIGNUM else (root, padding, ext)


def _generate_padded_filename_sequence(sequence, path_obj, padding_info):
    """
    Generate a padded filename sequence.

    Args:
        node (str): Maya node
        path (obj): path to evaluate
        padding_info (dict): frame information

    Returns:
        list: padded path sequence
    """
    paths = set()

    padding = padding_info["padding"]
    ext = padding_info["ext"]
    root = padding_info["root"]
    fileNode = pm.PyNode(path_obj["plug"]).node()
    num_frames = len(sequence)
    for i, f in enumerate(sequence):
        evaluatedFrame = fileNode.attr("frameExtension").get(time=f)
        evaluatedFrame += fileNode.attr("frameOffset").get(time=f)
        padded = root + str(evaluatedFrame).zfill(padding) + ext
        paths.add(padded)

    result = []
    num_frames = len(paths)
    for i, p in enumerate(sorted(list(paths))):
        path_obj_copy = copy.deepcopy(path_obj)
        path_obj_copy["path"] = p
        result.append(path_obj_copy)

    return result


def _get_scene_files():
    result = []
    for ref in pm.listReferences(recursive=True):
        result.append({"path": str(ref.path), "refNode": ref.refNode})

    scene_name = str(pm.sceneName())
    if scene_name:
        result.append({"path": scene_name})
    return result


def _get_assembly_assets():
    """
    Get assets definied in assemblyDefinition and assemblyReference nodes.

    Something strange with the representations array attribute type. Means we can't use
    scraper_utils.get_paths()

    We make the value globbabl[e] so that if it's missing it doesn't complain.

    Returns: list(dict): list of (path/plug) pairs
    """
    result = []
    for node in pm.ls(type=("assembly")):
        data_plugs = [
            node.attr(p)
            for p in pm.PyNode(node).attr("rep").elements()
            if p.endswith("repData")
        ]
        for plug in data_plugs:
            value = plug.get()
            if value:
                value = "{}[{}]".format(value[:-1], value[-1])
                result.append({"path": value, "plug": plug.name()})
    return result


def _get_env():
    """Get environment variables.

    Maya's includeAllLights setting can cause the scene to be rendered differently on a remote
    render node. (Bad design) So we query the corresponding optionVar and set the env variable
    accordingly.

    Returns:
        list of dict: list of environment variables in Conductor package_env format.
    """
    setting = pm.optionVar.get("renderSetup_includeAllLights", 1)
    return [
        {
            "name": "MAYA_RENDER_SETUP_INCLUDE_ALL_LIGHTS",
            "value": "{:d}".format(setting),
            "merge_policy": "exclusive",
        }
    ]
