"""
This file is part of JuPySub

Author: Pedro de Carvalho Ferreira, Ivo Filot, Ivo Roghair
License: GPLv3
"""

def build_tag(name: str, attrs: dict, text: str="%s", closed: bool = True) -> str:
    attrs_str = ""
    for k, v in attrs.items():
        if type(v) is dict:
            addition = " %s=\"%s\""%(k, "; ".join(["%s: %s"%(str(kk),str(vv)) for kk,vv in v.items()])+";")
        else:
            addition = "%s=\"%s\""%(k, str(v))
        attrs_str += addition + " "
    begin_tag = "<%s %s>"%(name, attrs_str)
    end_tag = "</%s>"%name if closed else ""
    return begin_tag+text+end_tag

## Expected solution tags (with drop down)
es_summary_attrs = {
    "style": {
        "margin": "0px 0px",
        "color": "#3498db",
        "font-size": "13pt"
        }
}
es_span_attrs = {
    "style": {
        "padding": "5px",
        "margin": "0px"
    }
} 
expected_sol_attrs = {
    "style": {
        "padding": "5px",
        "font-family": "monospace",
        "font-size": "10pt",
        "overflow": "auto",
        "border": "1px solid gray",
        "border-radius": "5px",
        "margin":"5px 0px 5px 0px",
        "white-space": "pre-wrap",
    },
    "class": "" #"alert alert-block alert-success"
}
## Expected solution tags (with dropdown)

# Used for hint and tip blocks 
hint_attrs = {
    "class": "alert alert-block alert-info",
}

# Used for h3 html tags such as Expected Output text
h3_attrs = {
}

# Just empty html tag
span_attrs = {
}

# Used for images in markdown html
img_attrs = {
    "style": {"display": "inline-block"},
    "src": "data:image/png;base64,%s"
}

# Used for code inside ``
code_attrs = {
}

# Building all the tags
hint_tag = build_tag("div", hint_attrs, "%s", True)
span_tag = build_tag("span", span_attrs, "%s", True)
img_tag = build_tag("img", img_attrs, "", False) + "<br>"
code_tag = build_tag("code", code_attrs, "%s", True)
h3_tag = build_tag("h3", h3_attrs, span_tag, True)

# Drop down tag
details_tag = build_tag("details", {}, "%s", True)
summary_tag = build_tag("summary", es_summary_attrs, "%s", True)
expected_solution_box_tag = build_tag("div", expected_sol_attrs, "%s", True)
ex_sol_tag = details_tag % (summary_tag+expected_solution_box_tag)

# Packaging the tags 
tags = {
    "hint": hint_tag,
    "span": span_tag,
    "img": img_tag,
    "code": code_tag,
    "h3_tag": h3_tag,
    "ex_sol": ex_sol_tag,
    "ignore": r""
}
