# -*- coding: utf-8 -*-
from __future__ import unicode_literals
"""
Submit.
"""

import pymel.core as pm
from ciomaya.lib import window_utils

try:
    import urlparse as parse
except ImportError:
    from urllib import parse


def about_conductor():
    version = pm.moduleInfo(version=True, moduleName="conductor")
    definition = pm.moduleInfo(definition=True, moduleName="conductor")
    path = pm.moduleInfo(path=True, moduleName="conductor")

    result = """
Conductor for Maya

        Module version: {}
   Module install path: {}
Module definition file: {}

LICENSE INFORMATION

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

Copyright © 2020, Conductor Technologies.
    """.format(
        version, path, definition
    )

    return result


def _dismiss():
    pm.layoutDialog(dismiss="abort")
 
def about_layout():
    form = pm.setParent(q=True)
    pm.formLayout(form, edit=True, width=300)
    heading = pm.text(label="Release Info and License")
    b1 = pm.button(label="Close", command=pm.Callback(_dismiss))
    frame = pm.frameLayout(
        bv=True, lv=False, cll=False, cl=False, width=700, height=500
    )
    pm.setParent("..")
    window_utils.layout_form(form, heading, frame, b1)
    pm.setParent(frame)

    pm.scrollField(editable=False, wordWrap=True, text=about_conductor())

    pm.setParent(form)


def show():
    return pm.layoutDialog(ui=pm.Callback(about_layout), title="About Conductor Maya")
