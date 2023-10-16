"""
This file is part of JuPySub

File name: jupysub.py
Author: Pedro de Carvalho Ferreira, Ivo Filot, Ivo Roghair
License: GPLv3
"""

import re
import json
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor

class NotebookManipulator:
    """
    Class to manipulate Jupyter Notebooks.
    
    Attributes:
        notebook (NotebookNode): The loaded notebook object.
    """

    def __init__(self, filename):
        """
        Initialize NotebookManipulator object.

        Parameters:
            filename (str): The name of the notebook file to be loaded.
        """
        self.notebook = self.load_notebook(filename)
        self.stringfy_code_cells()

    def apply_to_cells(self, func, cell_type, args=(), kwargs={}):
        """
        Apply a given function to the cells of a particular type in the notebook.

        Parameters:
            func (callable): Function to apply.
            cell_type (str): The type of cell to apply the function to.
            args (tuple, optional): Additional arguments to pass to func.
            kwargs (dict, optional): Additional keyword arguments to pass to func.
        """
        cells = self.filter_cells(cell_type)
        for cell in list(cells):
            func(cell, *args, **kwargs)

    def filter_cells(self, cell_type):
        """
        Filters cells based on their type.

        Parameters:
            cell_type (str): The type of cell to filter.

        Returns:
            list: List of cells that match the given cell_type.
        """
        if cell_type != "all":
            cells = filter(lambda c: c.cell_type == cell_type, self.notebook.cells)
        else:
            cells = self.notebook.cells
        return cells

    def load_notebook(self, filename):
        """
        Load a Jupyter Notebook.

        Parameters:
            filename (str): The name of the notebook file to be loaded.

        Returns:
            NotebookNode: The loaded notebook object.
        """
        with open(filename, "r", encoding="utf-8") as f:
            return nbformat.read(f, as_version=4)
    
    def apply_replacements(self, replacement_dict):
        """
        Apply regex replacements to the notebook's cells based on a dictionary.

        Parameters:
            replacement_dict (dict): Dictionary containing cell types as keys
            and sub-dictionaries of regex pattern-replacement pairs as values.

        """
        for cell_type, replacements in replacement_dict.items():
            cells = self.filter_cells(cell_type)
            for c in cells:
                source = c.source
                for pattern, replacement in replacements.items():
                    source = re.sub(pattern, replacement, source, flags=re.DOTALL | re.MULTILINE)
                c.source = source

    def save(self, outfile):
        """
        Save the modified notebook to a file.

        Parameters:
            outfile (str): The name of the output notebook file.
        """
        notebook_json = nbformat.writes(self.notebook, version=nbformat.NO_CONVERT)
        notebook_json_dict = json.loads(notebook_json)
        
        for cell in notebook_json_dict["cells"]:
            if "id" in cell:
                del cell["id"]
        
        with open(outfile, "w") as f:
            json.dump(notebook_json_dict, f, indent=1)

    def stringfy_code_cells(self):
        """
        Convert the source of code cells to a single string if they are in list format.
        """
        for cell in self.filter_cells("code"):
            src = cell.source
            if type(src) == list:
                cell.source = "".join(src)

    def remove_cell(self, cell):
        """
        Remove a cell from the notebook.

        Parameters:
            cell (Cell): The cell to remove.
        """
        self.notebook.cells.pop(self.notebook.cells.index(cell))

    def remove_empty_cell(self, cell):
        """
        Remove an empty cell from the notebook.

        Parameters:
            cell (Cell): The cell to remove.
        """
        src = cell.source
        if not src.strip("\n \t"):
            self.remove_cell(cell)

    def remove_cell_output(self, cell):
        """
        Remove the output of a given cell.

        Parameters:
            cell (Cell): The cell from which to remove the output.
        """
        if cell.get("outputs"):
            cell.outputs = []

    def remove_cell_outputs(self):
        """
        Remove the outputs of all cells
        """
        for cell in self.filter_cells("code"):
            self.remove_cell_output(cell)

    @classmethod 
    def build_replacement_dict(cls):
        """
        Returns a notebook with the general form of a replacement dict
        """
        rep_dict = {
            "code": {},
            "markdown": {},
            "raw": {}
        }
        return rep_dict

    def run_notebook(self, timeout=600, kernel_name='python3'):
        """
        Execute the notebook and update the output cells.
        
        Parameters:
            timeout (int): Cell execution timeout in seconds.
            kernel_name (str): Name of the kernel to be used for execution.
                To list available kernels, run 'jupyter kernelspec list' in the terminal.
                Choose the name that corresponds to your desired environment (e.g., 'python3', 'julia-1.5').
            
        Returns:
            None: The notebook object in the instance is updated.
        """
        # Create an ExecutePreprocessor object
        ep = ExecutePreprocessor(timeout=timeout, kernel_name=kernel_name)
        
        # Execute the notebook
        ep.preprocess(self.notebook, {'metadata': {'path': './'}})

    def get_outputs(self):
        """
        Collects the cells and outputs thereof.

        Returns:
            list((cell, [out0, out1,...]) for cell in cells)
        """
        pairs = []
        for cell in filter(lambda c: c.get("outputs"), self.filter_cells("code")):
            outputs = []
            for o in cell.get("outputs"):
                if text := o.get("text"):
                    outputs.append(("text/plain", text))
                elif data := o.get("data"):
                    for data_name, data_value in data.items():
                        if data_name == "text/plain":
                            continue # <Figure size xxx with 1 Axes> are dummy text
                        outputs.append((data_name, data_value))
            if outputs:
                pairs.append((cell, outputs))
        return pairs


if __name__ == "__main__":
    # Testing the basic functionality
    infile = "./main_notebooks/example.ipynb"
    outfile = "./main_notebooks/example_outfile.ipynb"
    note = NotebookManipulator(infile)
    note.run_notebook()
    note.save(outfile)
