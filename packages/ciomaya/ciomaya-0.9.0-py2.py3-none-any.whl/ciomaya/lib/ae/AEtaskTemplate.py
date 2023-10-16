"""
Handle the UI for extra assets:
"""

import pymel.core as pm
from ciomaya.lib import const as k
from ciomaya.lib.ae import AEcommon


def create_ui(node_attr):
    """Build static UI"""
 
    with AEcommon.ae_template():
        grp = pm.textFieldGrp("taskTemplateGrp", label="Task Template")
        label = pm.layout(grp, q=True, childArray=True)[0]
        pm.popupMenu(parent=label)
        pm.menuItem(label="Reset")
        pm.menuItem(label="Add Arnold logging args")
        pm.menuItem(label="Add Arnold abort on license fail args")
        
        
        populate_ui(node_attr)

def populate_ui(node_attr):
    """Populate / reconfigure UI for the current node"""
    attr = pm.Attribute(node_attr)
    widgets = _get_widgets()
    # index 2 is the field. (1 is the label) 
    pm.connectControl(widgets["field"], attr, index=2)
    # reconfigure the popup for this node.
    items = pm.popupMenu(widgets["popup_menu"], q=True, itemArray=True)
    pm.menuItem(items[0], edit=True, command=pm.Callback(_on_reset, attr))
    pm.menuItem(items[1], edit=True, command=pm.Callback(_on_insert_arnold_arg, attr, "lve", 1))
    pm.menuItem(items[2], edit=True, command=pm.Callback(_on_insert_arnold_arg, attr, "alf", 1))
    

def _get_widgets(parent=None):
    if not parent:
        parent = pm.setParent(q=True)
    field_grp = AEcommon.find_ui("taskTemplateGrp", parent)
    label = pm.layout(field_grp, q=True, childArray=True)[0]

    return {
        "field": field_grp,
        "popup_menu": pm.control( label, q=True, popupMenuArray=True)[0]
    }

def _on_reset(attribute):
    attribute.set(k.DEFAULT_TEMPLATE)
 
def _on_insert_arnold_arg(attribute, arg, value):
    """Insert the given arnold args into the task template"""
    template = attribute.get()
    if not template:
        template = k.DEFAULT_TEMPLATE
    template = template.partition("<Renderer>")
    arnold_arg = "-ai:{}".format(arg)
    if not arnold_arg in template[2]:
        arnold_arg_val = "{} {}".format(arnold_arg, value)
        template =[ template[0] , template[1] , arnold_arg_val , template[2]]
        attribute.set(" ".join(template))
    else:
        pm.displayWarning("Arnold arg {} already in template".format(arnold_arg))
 