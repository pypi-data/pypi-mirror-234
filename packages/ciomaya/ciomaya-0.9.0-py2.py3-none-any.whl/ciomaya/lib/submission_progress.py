
import traceback
import pymel.core as pm
from ciocore import config
from ciomaya.lib import window_utils


try:
    import urlparse as parse
except ImportError:
    from urllib import parse

def _get_numeric_code(response):
    code = response.get("code", 500)
    if not isinstance(code, int):
        code = 500
    return code

def _okay():
    pm.layoutDialog(dismiss="okay")

def responses_layout(responses):
    cfg = config.config().config
    form = pm.setParent(q=True)
    pm.formLayout(form, edit=True, width=300)
    text = pm.text(label="Links to {}".format(cfg["auth_url"]))
    b1 = pm.button(label="Close", command=pm.Callback(_okay))
    scroll = pm.scrollLayout(bv=True)

    pm.setParent("..")
    window_utils.layout_form(form, text, scroll, b1)
    pm.setParent(scroll)
    pm.columnLayout(adjustableColumn=True, columnAttach=("both", 5), rowSpacing=10)
    for success_uri in [
        response["response"]["uri"].replace("jobs", "job")
        for response in responses
        if _get_numeric_code(response) <= 201
    ]:
        job_url = parse.urljoin(cfg["auth_url"], success_uri)
        label = '<a href="{}"><font  color=#ec6a17 size=4>{}</font></a>'.format(
            job_url, job_url
        )
        pm.text(hl=True, label=label)

    failed_submissions = [response for response in responses if _get_numeric_code(response) > 201]
    num_failed = len(failed_submissions)
    if num_failed:
        pm.separator(style="single")
        pm.text(hl=True, label="{:d} failed submissions".format(num_failed))
        pm.separator(style="single")
        for failed_submission in failed_submissions:
            try:
                text = failed_submission["response"]
                pm.text(label=text, align="left", wordWrap=False)
            except BaseException as ex:
                pm.displayWarning(traceback.format_exc())


    pm.setParent(form)

def show_responses(responses):
    return pm.layoutDialog(
        ui=pm.Callback(responses_layout, responses), title="Render Response"
    )
