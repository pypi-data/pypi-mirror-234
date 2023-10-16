"""
This file is part of JuPySub

Author: Pedro de Carvalho Ferreira, Ivo Filot, Ivo Roghair
License: GPLv3
"""

from .tags import tags 
from nbformat.v4 import new_markdown_cell

def add_expected_outputs(ntmanip):
    notebook = ntmanip.notebook
    cells = notebook.cells
    for cell, outputs in ntmanip.get_outputs():
        eo_contents = [] # Expected output contents 
        for output_kind, output_content in outputs:
            if output_kind == "text/plain":
                data = output_content
            elif output_kind == "image/png":
                data = tags["img"] %output_content
            else: 
                print(output_kind, output_content)
            eo_contents.append(data)

        # Adding expected outputs cell
        if eo_str := "\n".join(eo_contents):
            eo_str = tags["ex_sol"]%("Expected solution", eo_str)
            markdown_cell = new_markdown_cell(eo_str)
            # Making the markdown cell and adding to notebook
            cell_index = cells.index(cell)
            cells.insert(cell_index+1, markdown_cell)