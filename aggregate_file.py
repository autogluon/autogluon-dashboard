import ast
import os
import re
from collections import namedtuple


def get_import_tuples(path):
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

def get_imports(filepath):
    imports = set()
    imps = [import_lib for import_lib in get_import_tuples(filepath)]
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

    return imports

def extract_code(filepath):
    """Extracts code from a Python file excluding import statements."""
    with open(filepath, "r") as file:
        lines = file.readlines()
    right_paran = False
    code_lines = []
    for line in lines:
        if not (line.startswith("import") or line.startswith("from")):
            if "utils." in line:
                line = line.replace("utils.", "")
            if right_paran and ")" in line:
                line = ""
                right_paran = False
            code_lines.append(line)
        elif "import (" in line:
            right_paran = True
    return "".join(code_lines)


def create_merged_file(directory, output_file):
    """Creates a merged file with all code from the directory."""
    code = []
    imports = set()

    # Iterate over all files in the directory
    for filename in sorted(os.listdir(directory)):
        filepath = os.path.join(directory, filename)

        # Skip directories and the output file itself
        if os.path.isdir(filepath) or filename == output_file:
            continue

        # Check if the file is the central file (app.py)
        if filename == "app.py":
            code.append(extract_code(filepath))

        elif filename == "dashboard.py":
            continue

        else:
            # Extract code from other files
            code.append(extract_code(filepath))
            imports = sorted(get_imports(filepath))

    imports = list(filter(lambda imp: not re.search(r"plotting|scripts|utils|Plot", imp), imports))
    # Combine all code and imports
    merged_code = "\n".join(imports) + "\n\n" + "\n".join(code)

    # Write the merged code to the output file
    with open(output_file, "a") as file:
        file.write(merged_code)


if __name__ == "__main__":
    # Specify the directory containing the files and the desired output file name
    out_file = "out.py"
    if os.path.exists(out_file):
        os.remove(out_file)
    else:
        open(out_file, "x")
    create_merged_file("src/autogluon_dashboard/scripts/constants", "out.py")
    create_merged_file("src/autogluon_dashboard/scripts", "out.py")
    create_merged_file("src/autogluon_dashboard/plotting", "out.py")
    create_merged_file("src/autogluon_dashboard", "out.py")
