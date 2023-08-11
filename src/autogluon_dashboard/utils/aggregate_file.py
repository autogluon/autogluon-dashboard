import ast
import os
import re
from collections import namedtuple

"""
The Aggregate File Script
----------------------------
One issue with panel is that it does not allow relative imports. 
The website generated by panel runs in a pyodide web-environment, where it installs the necessary python packages only from the official python index (PyPI). 
Therefore, to circumvent this, we created a script to aggregate all the files within the project directory into one big file to convert the web app into WebAssembly (HTML and JavaScript). 

NOTE: The order of crawling in the aggregate script is very important! 
If the app imports module A before module B, then it is imperative that the script crawls through the folder corresponding to module A first. 
Therefore, pay attention to how the dependency of the subdirectories is affected by any changes you make to app.py. 
The order of crawling can be found and modified in the "__main__" body of this file.
"""


def get_import_tuples(path: str):
    """Extracts import statements from a Python file by leveraging the ast parser library.
    The ast module helps Python applications process trees of Python abstract syntax grammar.
    It allows us to read the file and parse imports as direct import statements or from _ import statements.
    We use a named tuple to store the generated instances of import statements from ast.
    This tuple is divided into "module", "name", and "alias".
    Some examples:
        import pkg -> Import(module=[], name=["pkg"], alias=None)
        import pkg.sub_pkg -> Import(module=[], name=["pkg", "sub_pkg"], alias=None)
        import pkg.sub_pkg as name -> Import(module=[], name=["pkg", "sub_pkg"], alias=name)
        from module import pkg-> Import(module=["module"], name=["pkg"], alias=None)
        from module import pkg as name -> Import(module=["module"], name=["pkg"], alias=name)
        from module.sub_module import pkg as name -> Import(module=["module", "sub_module"], name=["pkg"], alias=name)

    Parameters
    ----------
    path: str,
        File to parse code from.
    """
    Import = namedtuple("Import", ["module", "name", "alias"])
    with open(path) as fh:
        root = ast.parse(fh.read(), path)

    for node in ast.iter_child_nodes(root):
        if isinstance(node, ast.Import):
            module = []
        elif isinstance(node, ast.ImportFrom):
            module = node.module.split(".")
        else:
            continue

        for n in node.names:
            yield Import(module, n.name.split("."), n.asname)


def get_imports(filepath: str, imports: set) -> None:
    """Extracts import statements from a Python file by leveraging the get_import_tuples helper function.
    Filters the parsed imports into different cases to account for import types.
    Some examples:
        import pkg
        import pkg.sub_pkg
        import pkg.sub_pkg as name
        from module import pkg
        from module import pkg as name
        from module.sub_module import pkg as name

    Parameters
    ----------
    filepath: str,
        File to parse code from.
    imports: set,
        Set to store imports in. We use a set to avoid duplicates when possible.
    """
    imps = [import_lib for import_lib in get_import_tuples(filepath)]
    # Extract imports
    for imported in imps:
        module = imported.module
        alias = imported.alias
        name = imported.name
        # import statments with from keyword
        if module:
            if len(module) == 1:
                if alias:
                    imports.add(f"from {module[0]} import {name[0]} as {alias}")
                else:
                    imports.add(f"from {module[0]} import {name[0]}")

            else:
                module_str = ""
                for sub_module in module:
                    module_str += f"{sub_module}."
                module_str = module_str[:-1]
                if alias:
                    imports.add(f"from {module_str} import {name[0]} as {alias}")
                else:
                    imports.add(f"from {module_str} import {name[0]}")

        # direct imports
        else:
            if len(name) == 1:
                if alias:
                    imports.add(f"import {name[0]} as {alias}")
                else:
                    imports.add(f"import {name[0]}")

            else:
                name_str = ""
                for sub_module in name:
                    name_str += f"{sub_module}."
                name_str = name_str[:-1]

                if alias:
                    imports.add(f"import {name_str} as {alias}")
                else:
                    imports.add(f"import {name_str}")


def extract_code(filepath: str) -> str:
    """Extracts code from a Python file excluding import statements.

    Parameters
    ----------
    filepath: str,
        File to parse code from.
    """

    with open(filepath, "r") as file:
        lines = file.readlines()
    code_lines = []
    right_paran = False
    for line in lines:
        # ignore imports
        if not (line.startswith("import") or line.startswith("from")):
            # ignore relative imports from utils since utils functions will be included in aggregate file
            if "utils." in line:
                line = line.replace("utils.", "")
            # handle unnecessary trailing paranthesis
            if right_paran:
                if ")" in line:
                    right_paran = False
                line = ""
            code_lines.append(line)
        elif "import (" in line:
            # set flag to handle trailing paranthesis
            right_paran = True
    return "".join(code_lines)


def create_merged_file(path: str, output_file: str) -> None:
    """Creates a merged file (or appends to if already created)
    with all code from the specified path. The path can be a file or a directory

    Parameters
    ----------
    path: str,
        path to crawl through for aggregation. This can be a path to a file or a directory
    output_file: str,
        Name of output file to store aggregated code in.
    """
    code = []
    imports = set()

    if os.path.isfile(path):
        # Extract code from other files
        code.append(extract_code(path))
        # Extract imports from other files
        get_imports(path, imports)

    elif os.path.isdir(path):
        # Iterate over all files in the directory
        for filename in sorted(os.listdir(path)):
            filepath = os.path.join(path, filename)

            # Skip sub-directories and the output file itself
            if os.path.isdir(filepath) or filename == output_file:
                continue

            # Check if the file is the central file of a directory
            elif filename == "plot.py" or filename == "widget.py":
                continue

            # dashboard is the wrapper file so we don't need it in the aggregated file
            # we also don't need the code in the aggregate_file script
            elif filename == "dashboard.py" or filename == "aggregate_file.py":
                continue

            else:
                # Extract code from other files
                code.append(extract_code(filepath))
                # Extract imports from other files
                get_imports(filepath, imports)

    # sort imports so order remains deterministic
    imports = sorted(imports)
    # filter out relative imports from sub-folders (plotting, utils, and utils) as well as imports from Plot class
    imports = list(filter(lambda imp: not re.search(r"plotting|utils|utils|Plot|autogluon_dashboard", imp), imports))
    # Combine all code and imports
    merged_code = "\n".join(imports) + "\n\n" + "\n".join(code)

    # Write the merged code to the output file
    with open(output_file, "a") as file:
        file.write(merged_code)


if __name__ == "__main__":
    # Specify the directory containing the files and the desired output file name
    out_file_path = "../index.py"
    dirname = os.path.dirname(__file__)
    out_file_path = os.path.join(dirname, out_file_path)

    with open(out_file_path, "w") as fp:
        pass

    base_dir = os.path.join(dirname, "../")

    create_merged_file(os.path.join(base_dir, "constants"), out_file_path)
    create_merged_file(os.path.join(base_dir, "utils"), out_file_path)
    create_merged_file(os.path.join(base_dir, "plotting/plot.py"), out_file_path)
    create_merged_file(os.path.join(base_dir, "plotting"), out_file_path)
    create_merged_file(os.path.join(base_dir, "widgets/widget.py"), out_file_path)
    create_merged_file(os.path.join(base_dir, "widgets"), out_file_path)
    create_merged_file(os.path.join(base_dir, "app.py"), out_file_path)
