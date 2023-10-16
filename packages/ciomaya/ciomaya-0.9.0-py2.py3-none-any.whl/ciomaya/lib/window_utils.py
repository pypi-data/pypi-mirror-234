import pymel.core as pm

def layout_form(form, text, main_layout, *buttons):
    form.attachForm(text, "left", 2)
    form.attachForm(text, "right", 2)
    form.attachForm(text, "top", 2)
    form.attachNone(text, "bottom")

    form.attachForm(main_layout, "left", 2)
    form.attachForm(main_layout, "right", 2)
    form.attachControl(main_layout, "top", 2, text)
    form.attachControl(main_layout, "bottom", 2, buttons[0])

    form.attachForm(buttons[0], "left", 2)
    form.attachNone(buttons[0], "top")
    form.attachForm(buttons[0], "bottom", 2)

    if len(buttons) == 1:
        form.attachForm(buttons[0], "right", 2)
    else:  # 2
        form.attachPosition(buttons[0], "right", 2, 50)

        form.attachPosition(buttons[1], "left", 2, 50)
        form.attachForm(buttons[1], "right", 2)
        form.attachNone(buttons[1], "top")
        form.attachForm(buttons[1], "bottom", 2)


def show_as_json(data, **kw):
    title = kw.get("title", "Json Window")
    indent = kw.get("indent", 2)
    sort_keys = kw.get("sort_keys", True)
    result_json = json.dumps(data, indent=indent, sort_keys=sort_keys)
    pm.window(width=600, height=800, title=title)
    pm.frameLayout(cll=False, lv=False)
    pm.scrollField(text=result_json, editable=False, wordWrap=False)
    pm.showWindow()
