"""
This file is part of JuPySub

Author: Pedro de Carvalho Ferreira, Ivo Filot, Ivo Roghair
License: GPLv3
"""

import re
import os
import json

def load_json_file(file_name):
    """Load JSON data from a file."""
    with open(file_name, "r", encoding="utf8") as file_pointer:
        return json.load(file_pointer)

# Get the current working directory
current_dir = os.path.dirname(__file__)

# Dictionary to store usage examples for each module
used_examples = {}

# Load JSON files
json_folder = os.path.join(current_dir, "json")
links_data = load_json_file(os.path.join(json_folder, "_links.json"))
info_data = load_json_file(os.path.join(json_folder, "_info.json"))  # General info about docs
global_functions = info_data["global_functions"]
module_list = info_data["module_list"]
abbrev_data = load_json_file(os.path.join(json_folder, "_abbreviations.json"))

# Pattern to match function names
FUNC_PATTERN = r"((?:\b[a-zA-Z_]+[0-9]*\.?)+(?=$|\())"

def build_link(match_obj):
    """Build a hyperlink for a function."""
    func_str = match_obj.group(1)  # Extracted function/library text
    
    # Check if it's a global function
    if "." not in func_str and func_str in global_functions:
        module = "functions"
        func_name = func_str

    # If it's not a module-level function, return original text
    elif "." not in func_str:
        return func_str

    else:  # Either a custom object or a module-level function
        element_pattern = r'(\b[a-zA-Z_]+[0-9]*)(?=\.|\(|$)'  # Pattern to match elements
        elements = re.findall(element_pattern, func_str)
        replace_abbr = lambda x: abbrev_data[x] if x in abbrev_data else x
        func_name = ".".join(map(replace_abbr, elements))
        module = func_name.split(".")[0]
    
    if module not in module_list:
        return func_str
    
    if module not in used_examples:
        used_examples[module] = load_json_file(os.path.join(json_folder, module + ".json"))

    # If both the module and function exist
    if func_name in used_examples[module]:
        link_url = links_data[module].replace("%FNAME%", func_name)
        if "numpy" in func_name:
            link_url = link_url.replace("%SUBMODULE%", "random/" if "random" in link_url else "")
        tooltip = used_examples[module][func_name]
        style = "text-decoration: none;"
        link_tag = r'<a style="%s" title="%s" href="%s">%s</a>'
        return link_tag % (style, tooltip, link_url, func_str)

    # If the link could not be built, return the original text
    return func_str


def add_links_to_code(match):
    """Add documentation links to code blocks."""
    # Extract the components of the <code> block
    opening_tag, code_content, closing_tag = match.group(1), match.group(2), match.group(3)
    
    # Create the full code block template
    code_block = f"{opening_tag}%s{closing_tag}"
    
    # Replace function names with corresponding links
    linked_code = re.sub(FUNC_PATTERN, build_link, code_content)
    
    # Return the new code block with added documentation links
    return code_block % linked_code


def annotate_code_with_links(cell, *args, **kwargs):
    """Wrap code snippets in HTML cells with documentation links."""
    # Regex pattern to match <code> HTML tags
    code_pattern = r'(<code.*?>)(.*?)(</code>)'
    
    # Replace code snippets within <code> tags with documentation links
    annotated_html = re.sub(code_pattern, add_links_to_code, cell.source, flags=re.DOTALL)
    cell.source = annotated_html

if __name__ == "__main__":
    # Example class for HTML cell content
    class MarkdownCell:
        def __init__(self):
            self.source = '''
<code style="background-color: #f0f0f0;">print("Hello, world!")</code>
<code>np.polyval</code>
<code>np.polyval()</code>
<code>np.linalg.norm()</code>
<code>plt.plot(x, y, label="hello")</code>
<code>plt.plot(x, y, label ="hello")</code>
<code>plt.plot(x, y, label = "hello")</code>
<code>a.dot(b)</code>
<code>scipy.integrate.odeint(rate_func, y0, t, args=(args,))</code>
<code>scipy.optimize.curve_fit</code>
<code>()</code>
<code>numpy</code>
<code>scipy</code>
<code>pandas</code>
<code>math.ceil()</code>
<code>dcdt = np.array([1, 2, 3.5])</code>
<code>dcdt = np.max([np.array([1,2]),np.array([3,4])])</code>
<code>pathlib.Path()</code>
<code>import os</code>
<code>import sys</code>
<code>os.path.join("folder", "file.txt")</code>
<code>os.makedirs("new_folder")</code>
<code>sys.argv</code>
<code>sys.exit(0)</code>
<code>open("file.txt", "r")</code>
<code>range(10)</code>
<code>zip([1, 2], [3, 4])</code>
<code>enumerate([10, 20, 30])</code>
<code>sorted([3, 1, 2])</code>
<code>len("hello")</code>
<code>str(42)</code>
<code>int("42")</code>
<code>list((1, 2, 3))</code>
<code>dict(a=1, b=2)</code>
<code>set([1, 2, 3])</code>
            '''
            self.cell_type = "markdown"

    # Create a Markdown cell instance and annotate its code snippets
    example_cell = MarkdownCell()
    annotate_code_with_links(example_cell, None)
    print(example_cell.source)
