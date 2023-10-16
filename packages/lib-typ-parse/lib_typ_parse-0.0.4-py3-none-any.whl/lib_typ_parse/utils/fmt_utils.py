import os, json
import lib_typ_parse.utils.exceptions as exceptions

def format_indent(indent_str, multiline_str):
    return '\n'.join([f'{indent_str}{x}' for x in multiline_str.splitlines()])

def serialize_json(py_dict):
    result = json.dumps(py_dict, indent=1)
    return result

def print_json(py_dict):
    result = json.dumps(py_dict, indent=4)
    print(result)
    return 1

def select_module_src_dir(module_dir, target_module):
    x1 = target_module.replace('.', '/')
    result = f'{module_dir}/{x1}.typ'
    if not os.path.exists(result):
        error_msgs = [
            'module does not exist:',
            f'module: {target_module}',
        ]
        exceptions.raise_exception_ue(error_msgs)
    return result

def read_module_src(module_dir, target_module):
    x1 = target_module.replace('.', '/')
    result = f'{module_dir}/{x1}.typ'
    if not os.path.exists(result):
        error_msgs = [
            'module does not exist:',
            f'module: {target_module}',
        ]
        exceptions.raise_exception_ue(error_msgs)
    module_src = open(result, 'r').read()
    return result
