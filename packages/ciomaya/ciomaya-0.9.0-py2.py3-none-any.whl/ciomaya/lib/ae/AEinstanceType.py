from __future__ import unicode_literals

"""
Handle the UI for instanceTypes:

"""

import maya.app.renderSetup.model.renderSetup as rs
import maya.app.renderSetup.views.overrideUtils as ov_utils
import pymel.core as pm
from ciocore import data as coredata

from ciomaya.lib import const as k
from ciomaya.lib.ae import AEcommon

INSTANCE_TYPE_LABEL = "Instance Type"

def create_ui(node_attr):
    """Build static UI

    Components:

    1. Category menu - for example: "CPU", "GPU", "High Tier", "Low Tier"
    2. Content menu is a submenu of the categories menu - for example: "c4.8xlarge", "g2.2xlarge", "m4.2xlarge"
    3. Popup menu - contains: "Create Absolute Override for Visible Layer"
    """
    with AEcommon.ae_template():
        form = pm.formLayout("instanceTypesForm", numberOfDivisions=100)

        label = pm.text("instanceTypesLabel", label=INSTANCE_TYPE_LABEL, width=k.AE_TEXT_WIDTH, align="right")
        category_menu = pm.optionMenu("instanceTypesCategoryMenu", acc=True)
        content_menu = pm.optionMenu("instanceTypesContentMenu", acc=True)
            
            
        popup = pm.popupMenu(parent=label)
        pm.setParent(popup, menu=True)
        pm.menuItem(label="Create Absolute Override for Visible Layer")
        pm.setParent("..")  # out of formLayout

        pm.checkBoxGrp("preemptibleCheckbox", label="Preemptible (Spot)")

        form.attachForm(label, "left", 2)
        form.attachNone(label, "right")
        form.attachForm(label, "top", 2)
        form.attachForm(label, "bottom", 2)

        form.attachControl(category_menu, "left", 2, label)
        form.attachPosition(category_menu, "right", 2, 50)
        form.attachForm(category_menu, "top", 2)
        form.attachForm(category_menu, "bottom", 2)

        form.attachControl(content_menu, "left", 2, category_menu)
        form.attachForm(content_menu, "right", 2)
        form.attachForm(content_menu, "top", 2)
        form.attachForm(content_menu, "bottom", 2)

        populate_ui(node_attr)


def populate_ui(node_attr):
    """Rehydrate the UI for the current node.attribute.

    This is called when the UI is first created, and when switching to a different submitter.
    """
    attr = pm.Attribute(node_attr)
    widgets = _get_widgets()
    preemptible_attr = attr.node().attr("preemptible")
    preemptible_value = preemptible_attr.get()
    pm.checkBoxGrp(widgets["preemptible_cb"], edit=True, value1=preemptible_value, changeCommand1=pm.Callback(_on_preemptible_change, preemptible_attr))

    if not coredata.valid():
        for item in pm.optionMenu(widgets["contentmenu"], q=True, itemListLong=True):
            pm.deleteUI(item)
        pm.setParent(widgets["contentmenu"], menu=True)
        pm.menuItem(label="Not connected")
        for item in pm.optionMenu(widgets["catmenu"], q=True, itemListLong=True):
            pm.deleteUI(item)
        pm.setParent(widgets["catmenu"], menu=True)
        pm.menuItem(label="---")
    # update popup menu items
    _configure_popup_menu(attr, widgets)

    pm.optionMenu(
        widgets["catmenu"],
        edit=True,
        changeCommand=pm.Callback(_on_category_menu_change, attr, widgets),
    )
    pm.optionMenu(
        widgets["contentmenu"],
        edit=True,
        changeCommand=pm.Callback(_on_content_menu_change, attr, widgets["contentmenu"]),
    )

    # Update this UI if the attribute changes by some other means
    # For example: setAttr, or another instance of the attribute editor.
    _setup_script_jobs(attr, widgets)
    _set_label_color(attr, widgets["label"])

    pm.evalDeferred(pm.Callback(_ensure_connection, attr, widgets))

### Private

def _configure_popup_menu(attr, widgets):
    override_item = pm.popupMenu(widgets["popup_menu"], q=True, itemArray=True)[0]

    enable_override = (
        pm.editRenderLayerGlobals(query=True, currentRenderLayer=True)
        != "defaultRenderLayer"
    )
    pm.menuItem(
        override_item,
        edit=True,
        en=enable_override,
        command=pm.Callback(_create_layer_override, attr, widgets["label"]),
    )


def _get_widgets(parent=None):
    if not parent:
        parent = pm.setParent(q=True)
    label = AEcommon.find_ui("instanceTypesLabel", parent),
    return {
        "label": label,
        "catmenu": AEcommon.find_ui("instanceTypesCategoryMenu", parent),
        "contentmenu": AEcommon.find_ui("instanceTypesContentMenu", parent),
        "popup_menu": pm.control(label, q=True, popupMenuArray=True)[0],
        "preemptible_cb": AEcommon.find_ui("preemptibleCheckbox", parent)
    }


def _setup_script_jobs(attr, widgets):
    """
    Update the UI based on events.

    1. When the attribute changes - sync the menu to the attribute value.
    2. When the render layer manager changes - sync the menu and update the label color.
    """
    menu = widgets["contentmenu"]

    pm.scriptJob(
        attributeChange=(
            attr,
            pm.Callback(_sync_menu_to_attr, attr, widgets),
        ),
        parent=menu,
        replacePrevious=True,
    )

    pm.scriptJob(
        event=(
            "renderLayerManagerChange",
            pm.Callback(_on_render_layer_manager_change, attr, widgets),
        ),
        parent=menu,
    )


def _on_render_layer_manager_change(attr, widgets):
    _sync_menu_to_attr(attr, widgets)
    _set_label_color(attr, widgets["label"])


def _ensure_connection(attr, widgets):
    """Fetch a fresh list of inst types from Conductor (or the cache)

     hardware.categories are expected to be structured like this:

    [
        {
            "label": "Category 1",
            "content": [
                {"description": "Content 1", "name": "content1", and-so-on ...},
                {"description": "Content 2", "name": "content2", and-so-on ...},
                {"description": "Content 3", "name": "content3", and-so-on ...}
            ]
        },
        {
            "label": "Category 2",
            "content": [
                {"description": "Content 4", "name": "content4", and-so-on ...},
                {"description": "Content 5", "name": "content5", and-so-on ...},
                {"description": "Content 6", "name": "content6", and-so-on ...}
            ]
        }
    ]
    """

    hardware = coredata.data().get("instance_types")
    if not hardware:
        return

    category_labels = [item["label"] for item in hardware.categories]
    if not category_labels:
        return
    AEcommon.ensure_populate_menu(widgets["catmenu"], category_labels)
    _sync_menu_to_attr(attr, widgets)
    
    # set preemptible off and hide it if provider is coreweave.
    if hardware.provider == "cw":
        pm.checkBoxGrp(widgets["preemptible_cb"], edit=True, visible=False, value1=False)
    else:
        pm.checkBoxGrp(widgets["preemptible_cb"], edit=True, visible=True)

def _sync_menu_to_attr(attr, widgets):
    """
    Make sure menu item reflects the attribute value.

    If the attribute is invalid, set it to the first valid instance type.
    """

    attr_value = attr.get()
    hardware = coredata.data()["instance_types"]
    category_label = pm.optionMenu(widgets["catmenu"], q=True, value=True)
    
    # try to stay on the current category
    instance_type = hardware.find(attr_value, category=category_label)
    if not instance_type:
        # inst type not in current category, try to find it in any category
        instance_type = hardware.find(attr_value)
        if instance_type:
            category_label = instance_type["categories"][0]["label"]

    if not instance_type:
        # list must have changed or attribute is invalid
        instance_type = hardware.find_first(lambda x: x["cores"] > 2)
        attr_value = instance_type["name"]
        attr.set(attr_value)
        AEcommon.print_setAttr_cmd(attr)
        category_label = instance_type["categories"][0]["label"]
        
    # set the category menu
    pm.optionMenu(widgets["catmenu"], edit=True, value=category_label)
    category = hardware.find_category(category_label)
    if not category:
        pm.displayWarning(
            "Didn't find category '{}' in instance types".format(category_label)
        )
        return
    content_descriptions = [c["description"] for c in category["content"]]
    AEcommon.ensure_populate_menu(widgets["contentmenu"], content_descriptions)
    pm.optionMenu(widgets["contentmenu"], edit=True, value=instance_type["description"])

    _set_label_color(attr, widgets["label"])


def _on_category_menu_change(attr, widgets):
    hardware = coredata.data()["instance_types"]
    num_items = pm.optionMenu(widgets["catmenu"], q=True, numberOfItems=True)
    if not num_items:
        return
    category_label = pm.optionMenu(widgets["catmenu"], q=True, value=True)
    category = hardware.find_category(category_label)
    if not category:
        pm.displayWarning(
            "Didn't find category '{}' in instance types".format(category_label)
        )
        return
    content_labels = [c["description"] for c in category["content"]]

    AEcommon.ensure_populate_menu(widgets["contentmenu"], content_labels)
    attr_value = attr.get()
    instance_type = hardware.find(attr_value)
    if not category_label in [c["label"] for c in instance_type["categories"]]:
        instance_type = category["content"][0]
        attr_value = instance_type["name"]
        attr.set(attr_value)
        AEcommon.print_setAttr_cmd(attr)

    pm.optionMenu(widgets["contentmenu"], edit=True, value=instance_type["description"])


def _on_content_menu_change(attr, menu):
    """
    Respond to menu change.

    Set the value of the attribute to the selected item.
    """
    hardware = coredata.data()["instance_types"]
    num_items = pm.optionMenu(menu, q=True, numberOfItems=True)
    if not num_items:
        return
    label = pm.optionMenu(menu, q=True, value=True)
    instance_type = hardware.find_first(lambda x: x["description"] == label)

    if not instance_type:
        pm.displayWarning("Didn't find '{}' in instance types".format(label))
        return

    name = instance_type["name"]
    if attr.get() != name:
        attr.set(name)
        AEcommon.print_setAttr_cmd(attr)


def _create_layer_override(attr, label):
    ov_utils.createAbsoluteOverride(attr.node().name(), attr.attrName(True))
    _set_label_color(attr, label)


def _set_label_color(attr, label):
    """By convention, label is orange if attr has an override."""
    has_override = rs.hasOverrideApplied(attr.node().name(), attr.attrName(True))
    label_text = "<font color=#ec6a17>{}</font>".format(INSTANCE_TYPE_LABEL) if has_override else INSTANCE_TYPE_LABEL
    pm.text(label, edit=True, label=label_text)

def _on_preemptible_change(attr):
    attr.set(pm.checkBoxGrp("preemptibleCheckbox", q=True, value1=True))
    AEcommon.print_setAttr_cmd(attr)