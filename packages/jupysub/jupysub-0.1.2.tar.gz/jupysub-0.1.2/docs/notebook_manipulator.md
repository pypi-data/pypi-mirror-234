# NotebookManipulator: Python Library for Jupyter Notebook Manipulation

- [NotebookManipulator: Python Library for Jupyter Notebook Manipulation](#notebookmanipulator-python-library-for-jupyter-notebook-manipulation)
  - [Description](#description)
  - [Features](#features)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Initialization](#initialization)
    - [Applying Functions to Cells](#applying-functions-to-cells)
      - [Function Signature](#function-signature)
      - [Cell Object](#cell-object)
    - [Applying Regex Replacements](#applying-regex-replacements)
      - [Function Signature](#function-signature-1)
      - [Example Dictionary](#example-dictionary)
      - [Cell Object and Regex Patterns](#cell-object-and-regex-patterns)
      - [Sample Use-Case](#sample-use-case)
      - [Using Functions for Advanced Replacements](#using-functions-for-advanced-replacements)
    - [Saving the Notebook](#saving-the-notebook)
    - [Running the Notebook](#running-the-notebook)
  - [API Documentation](#api-documentation)
  - [Advanced Example with Function-based Replacements](#advanced-example-with-function-based-replacements)
      - [Python Code for Replacements](#python-code-for-replacements)
      - [Before and After Tables](#before-and-after-tables)
      - [Markdown Cells](#markdown-cells)

## Description

`NotebookManipulator` is a Python library that provides various methods for manipulating Jupyter Notebooks programmatically. It not only allows you to filter, edit, and remove notebook cells but also enables you to execute the notebook and apply custom regular expression substitutions to the cell contents.

## Features

- Load and Save Jupyter Notebooks
- Apply functions to specific or all cell types
- Remove cells and cell outputs
- Regex-based string replacement
- Execute the entire notebook programmatically

## Installation

Copy the `NotebookManipulator` class into your project or import it as a module.

## Usage

### Initialization

First, you need to create an instance of the `NotebookManipulator` class by providing the notebook filename you wish to manipulate.

```python
from notebook_manipulator import NotebookManipulator

note = NotebookManipulator("example.ipynb")
```

### Applying Functions to Cells

The `apply_to_cells` method allows you to apply a function to cells of specific types. You can target 'code', 'markdown', 'raw', or all types of cells ('all').

#### Function Signature

```python
apply_to_cells(func, cell_type, args=(), kwargs={})
```

- `func`: The function to apply to the cells.
- `cell_type`: The type of cell to target. Can be 'code', 'markdown', 'raw', or 'all'.
- `args` (optional): Tuple of additional positional arguments to pass to `func`.
- `kwargs` (optional): Dictionary of additional keyword arguments to pass to `func`.

#### Cell Object

When your function is called, it will receive a `cell` object as its first argument. The `cell` object has several attributes and methods, but the most commonly used ones you might interact with are:

- `cell.source`: The content of the cell. For 'code' and 'markdown' cells, this is a string containing the cell's source code or Markdown text. You can modify this attribute to change the content of the cell.
  
- `cell.cell_type`: The type of the cell, which can be 'code', 'markdown', or 'raw'. This attribute is read-only and is mainly used for identification purposes.

Here's a sample function that changes the content of 'code' cells to add a comment line at the top:

```python
def add_comment_to_code(cell):
    if cell.cell_type == 'code':
        cell.source = "# This is an auto-generated comment\n" + cell.source
```

You would apply this function to all 'code' cells like this:

```python
note.apply_to_cells(add_comment_to_code, 'code')
```

This will prepend the comment `# This is an auto-generated comment` to all code cells in the notebook.

Feel free to extend the function to suit your specific use-case needs.

### Applying Regex Replacements

The `apply_replacements` method allows you to perform regular expression (regex) replacements on notebook cells. This is particularly useful for batch text manipulations and pattern-based modifications.

#### Function Signature

```python
apply_replacements(replacement_dict)
```

- `replacement_dict`: A dictionary containing the types of cells as keys ('code', 'markdown', 'raw') and sub-dictionaries of regex pattern-replacement pairs as values.

#### Example Dictionary

Here's an example dictionary for replacing text in 'code' and 'markdown' cells:

```python
replacement_dict = {
    "code": {
        "old_string": "new_string"
    },
    "markdown": {
        "\\[TOC\\]": "[Table of Contents]"
    }
}
```

To apply these replacements to your notebook:

```python
note.apply_replacements(replacement_dict)
```

#### Cell Object and Regex Patterns

The `apply_replacements` method modifies the `cell.source` attribute of each cell, using Python's `re.sub` function to perform the replacements.

- `cell.source`: The attribute containing the cell's content, which will be subject to the regex replacements.
  
- Regex flags: The method uses both `re.DOTALL` and `re.MULTILINE`, allowing the regex patterns to match across line breaks and treat the string as a single line.

#### Sample Use-Case

Suppose you have a markdown cell containing the text `[TOC]`, which you want to automatically replace with "[Table of Contents]". With `apply_replacements`, you can achieve this as follows:

```python
replacement_dict = {
    "markdown": {
        "\\[TOC\\]": "[Table of Contents]"
    }
}
note.apply_replacements(replacement_dict)
```

This will search through all 'markdown' cells in the notebook, looking for occurrences of `[TOC]`, and replace them with "[Table of Contents]".

Feel free to extend the `replacement_dict` and your regex patterns to suit your specific needs.

#### Using Functions for Advanced Replacements

For more advanced use-cases, you can set the replacement value in the dictionary to be a function. This function should take a single argument, which is a `re.Match` object, and return a string.

Here's an example:

```python
def custom_replacement(match):
    return f"custom_string_{match.group(1)}"

replacement_dict = {
    "code": {
        r"\bword_(\d+)\b": custom_replacement
    }
}
```

In this example, the function `custom_replacement` will be used to replace occurrences of the pattern `\bword_(\d+)\b` in 'code' cells. The function receives a `re.Match` object and uses `match.group(1)` to fetch the numerical part captured by the regex pattern. It then returns a custom string using that numerical part.

To apply this advanced replacement, you would call:

```python
note.apply_replacements(replacement_dict)
```

In this way, you can perform complex replacements that depend on the matched content, giving you a powerful tool for notebook manipulation.


### Saving the Notebook

After performing all manipulations, you can save the notebook using the `save` method.

```python
note.save("example_modified.ipynb")
```

### Running the Notebook

To execute all the code cells in the notebook, use the `run_notebook` method.

```python
note.run_notebook()
```

## API Documentation

For more details, refer to the inline comments and docstrings in the code.

## Advanced Example with Function-based Replacements

In this example, we will make use of function-based replacements for both 'markdown' and 'code' cells.

#### Python Code for Replacements

```python
def replace_md(match):
    return f"### {match.group(1).upper()}"

def replace_code(match):
    return f"print('Hello, {match.group(1)}')"

replacement_dict = {
    "markdown": {
        r"\#\#\# (.+)": replace_md
    },
    "code": {
        r"print\('(.+)'\)": replace_code
    }
}

note.apply_replacements(replacement_dict)
```

#### Before and After Tables

#### Markdown Cells

| Before Running Script | After Running Script |
|----------------------|----------------------|
| `<h3 style="background-color: #f5f5f5; border: 1px solid #ccc; padding: 10px;">Section</h3>` | `<h3 style="background-color: #f5f5f5; border: 1px solid #ccc; padding: 10px;">SECTION</h3>` |

| Before Running Script    | After Running Script          |
|--------------------------|-------------------------------|
| `<pre style="background-color: #f5f5f5; border: 1px solid #ccc; padding: 10px;">print('world')</pre>` | `<pre style="background-color: #f5f5f5; border: 1px solid #ccc; padding: 10px;">print('Hello, world')</pre>` |

In this example, the 'markdown' cells with headers like `### Section` will be replaced to make the section titles uppercase. The 'code' cells containing `print('world')` will be replaced to say `print('Hello, world')`.

This showcases how function-based replacements can be used for complex and flexible text manipulations in your Jupyter notebooks.
