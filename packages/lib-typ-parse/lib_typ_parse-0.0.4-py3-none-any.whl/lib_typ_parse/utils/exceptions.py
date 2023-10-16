import json

def find_all(s, t, index):
    i1 = index-1
    result = []
    while True:
        i1 = s.find(t, i1+1)
        if i1 == -1: break
        result.append(i1)
    return result


def raise_exception_msg(code, index, error_msg):
    L1 = find_all(code[:index], '\n', 0)
    line_num = len(L1)
    formal_message = f'''
Compiler Error:
    Line: {line_num}
    Message: {error_msg}
'''
    raise Exception(formal_message)

def raise_exception_msgs(code, index, error_msgs):
    L1 = find_all(code[:index], '\n', 0)
    line_num = len(L1)
    error_msg = '\n'.join([f'        {x}' for x in error_msgs])
    formal_message = f'''
Compiler Error:
    Line: {line_num}
    Messages:
{error_msg}
'''
    raise Exception(formal_message)

def raise_exception_raw(error_msgs):
    # L1 = find_all(code[:index], '\n', 0)
    # line_num = len(L1)
    error_msg = '\n'.join([f'        {x}' for x in error_msgs])
    formal_message = f'''
Compiler Error:
    Type: Semantic Error
    Messages:
{error_msg}
'''
    raise Exception(formal_message)

def raise_exception_ue(error_msgs):
    # L1 = find_all(code[:index], '\n', 0)
    # line_num = len(L1)
    error_msg = '\n'.join([f'        {x}' for x in error_msgs])
    formal_message = f'''
Compiler Error:
    Messages:
{error_msg}
'''
    raise Exception(formal_message)

def raise_exception_ue_cm(error_msgs, current_module):
    # L1 = find_all(code[:index], '\n', 0)
    # line_num = len(L1)
    error_msg = '\n'.join([f'        {x}' for x in error_msgs])
    formal_message = f'''
Compiler Error:
    current module: {current_module}
    Messages:
{error_msg}
'''
    raise Exception(formal_message)

def raise_exception_ST(symbol_table, errors):
    error_msg = ''
    if isinstance(errors, list):
        error_msg = '\n'.join([f'        {x}' for x in errors])
    else:
        error_msg = str(errors)
    code = symbol_table['current_module']['module_src']
    index = -1
    if len(symbol_table['current_module']['current_scope']) > 0:
        index = symbol_table['current_module']['current_scope'][-1]['index']

    L1 = code[:index].splitlines()
    L2 = code.splitlines()
    line_num = len(L1)
    file_name = symbol_table['current_module']['module_src_path']
    formal_message = f'''
Compiler Error:
    File: {file_name}
    Line Number: {line_num}
    Line:
{L2[line_num-1]}
    Messages:
{error_msg}
'''
    raise Exception(formal_message)

def format_parse_tree(abstract_tree):
    return json.dumps(abstract_tree, indent=1)

def raise_inv_exception_decl(exception_decl, symbol_table):
    error_msgs = [
        f'invalid exception declaration: {exception_decl}',
        'required format: except Exception as {typon_identifier}',
    ]
    raise_exception_ST(symbol_table, error_msgs)

def raise_invalid_raise_exception(symbol_table):
    error_msgs = [
        f'invalid use of raise keyword:',
        'required format: raise [Exception]([str])',
    ]
    raise_exception_ST(symbol_table, error_msgs)

def raise_class_not_found_exception(symbol_table, class_name, target_module):
    error_msgs = [
        f'unable to resolve class_name: {class_name}',
        f'located in target module: {target_module}'
    ]
    raise_exception_ST(symbol_table, error_msgs)

def raise_inv_assertion_declaration(symbol_table, interior_assert_typon_type):
    error_msgs = [
        f'invalid assertion declaration:',
        f'interior expression resolves to type: {interior_assert_typon_type}',
        f'when type bool is required',
    ]
    raise_exception_ST(symbol_table, error_msgs)

def raise_exception_L0_skeleton(errors, current_module, L0_skeleton):
    error_msg = ''
    if isinstance(errors, list):
        error_msg = '\n'.join([f'        {x}' for x in errors])
    else:
        error_msg = str(errors)

    formal_message = f'''
    Target Module: {current_module}
{error_msg}
'''
    raise Exception(formal_message)

def raise_parsing_exception(error_msg_str, current_module, src_dir):
    formal_message = f'''
Error parsing module:
    target module: {current_module}
    source path: {src_dir}
{error_msg_str}
'''
    raise Exception(formal_message)
