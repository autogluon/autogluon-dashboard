import os
import re
import subprocess
import sys


def get_imports(filepath):
    """Extracts import statements and imported libraries from a Python file."""
    with open(filepath, 'r') as file:
        lines = file.readlines()

    imports = []
    imported_libraries = set()
    for line in lines:
        if line.startswith('import'):
            import_line = line.rstrip()
            libs = re.findall(r'[\w.]+', import_line.split('import')[-1])
            imported_libraries.update(libs)
            if ' as ' in import_line:
                imports.append(import_line)
            else:
                match = re.match(r'import\s+(.+)\s+as\s+(\w+)', import_line)
                if match:
                    imports.append('import {} as {}'.format(match.group(1), match.group(2)))
                else:
                    modules = import_line.split('import')[1].split(',')
                    modules = [module.strip() for module in modules]
                    if len(modules) > 1:
                        imports.append('import {}'.format(', '.join(modules)))
                    else:
                        imports.append('import {}'.format(modules[0]))
        elif line.startswith('from'):
            statement = line.rstrip()
            match = re.match(r'from\s+((?:\w+\.)*\w+)\s+import\s+(.+)', statement)
            if match:
                package = match.group(1)
                modules = match.group(2).split(',')
                import_line = 'from {} import {}'.format(package, ', '.join(modules))
                imports.append(import_line)
                imported_libraries.add(package)

    imports = list(filter(lambda imp: not re.search(r'(?:\bas$)|(?:\bimport pn\b)|(?:\bimport pd\b)|(\bplotting\b)|(\bscripts\b)', imp), imports))
    imported_libraries = list(filter(lambda imp: not re.search(r'(?:\bas$)|(?:\bpn\b)|(?:\bpd\b)|(\bplotting\b)|(\bscripts\b)', imp), imported_libraries))

    return imports, imported_libraries


def extract_code(filepath):
    """Extracts code from a Python file excluding import statements."""
    with open(filepath, 'r') as file:
        lines = file.readlines()

    code_lines = []
    for line in lines:
        if not (line.startswith('import') or line.startswith('from')):
            if 'utils.' in line:
                line = line.replace('utils.', '')
            code_lines.append(line)

    return ''.join(code_lines)

def create_merged_file(directory, output_file):
    """Creates a merged file with all code from the directory."""
    code = []
    imports = []
    imported_libraries = set()

    # Iterate over all files in the directory
    for filename in sorted(os.listdir(directory)):
        filepath = os.path.join(directory, filename)

        # Skip directories and the output file itself
        if os.path.isdir(filepath) or filename == output_file:
            continue

        # Check if the file is the central file (app.py)
        if filename == 'app.py':
            # Extract import statements from app.py
            code.append(extract_code(filepath))
            
        else:
            # Extract code from other files
            code.append(extract_code(filepath))
            files, libs = get_imports(filepath)
            imports.extend(files)
            imported_libraries.update(libs)
    
    additional_imports = [f"import {lib}" for lib in imported_libraries]
    imports.extend(additional_imports)

    # Combine all code and imports
    merged_code = '\n'.join(imports) + '\n\n' + '\n'.join(code)

    # Write the merged code to the output file
    with open(output_file, 'a') as file:
        file.write(merged_code)

if __name__ == '__main__':
    # Specify the directory containing your files and the desired output file name
    out_file = 'out.py'
    if os.path.exists(out_file):
        os.remove(out_file)
    else:
        open(out_file, 'x')
    create_merged_file('src/scripts/constants', 'out.py')
    create_merged_file('src/scripts', 'out.py')
    create_merged_file('src/plotting', 'out.py')
    create_merged_file('src/app', 'out.py')
