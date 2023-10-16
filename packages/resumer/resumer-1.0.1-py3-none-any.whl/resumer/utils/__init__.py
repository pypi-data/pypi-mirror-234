import subprocess
import os
import ast
import yaml

def _extract_compare(item : ast.Compare):
    items = []
    left = item.left
    right = item.comparators[0]

    if isinstance(left, ast.Name):
        items.append(left.id)

    if isinstance(right, ast.Name):
        items.append(right.id)

    return items

def extract_vars(query : str):
    ast_module = ast.parse(query)
    ast_query = ast_module.body[0].value
    if isinstance(ast_query, ast.Compare):
        return _extract_compare(ast_query)

    if not isinstance(ast_query, ast.BoolOp):
        raise ValueError("not a boolop")

    values = [] 
    for value in ast_query.values:
        if isinstance(value, ast.Compare):
            values += _extract_compare(value)
        else: 
            raise ValueError("not a compare")

    return values

def_template = "lambda {vars} : {query}"

def def_constructor(query : str):
    vars_needed = extract_vars(query)
    func_string = def_template.format(query = query, vars = ", ".join(vars_needed))

    return eval(
        func_string
    ), vars_needed


def check_invalid_cmdlet(response : bytes):
    if b"invalid cmdlet" in response:
        return True
    if b"is not recognized as an internal or external command" in response:
        return True
    return False

def check_installed(app : str, use_version : bool = True) -> bool:
    args = [app]
    if use_version:
        args += ["--version"]
    try:
        # block output
        response = subprocess.check_output(args, stderr=subprocess.STDOUT)
        if check_invalid_cmdlet(response):
            return False
        
        return True
    except Exception: #noqa
        return False
    
def rename_bkup(path : str):
    if not os.path.exists(path):
        return
    
    try:
        os.rename(path, path + ".bak")
    except: # noqa
        os.remove(path + ".bak")
        os.rename(path, path + ".bak")


def dump_yaml(path : str, data : dict):
    yaml_data = yaml.dump(data)
    with open(path, "w") as f:
        f.write("---\n")
        f.write(yaml_data)
        f.write("---\n")