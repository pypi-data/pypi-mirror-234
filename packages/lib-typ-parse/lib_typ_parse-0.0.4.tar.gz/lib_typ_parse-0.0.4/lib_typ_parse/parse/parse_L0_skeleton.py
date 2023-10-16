import os
import traceback
import lib_typ_parse.parse.parser as parser
import lib_typ_parse.utils.fmt_utils as fmt_utils
import lib_typ_parse.utils.exceptions as exceptions
import lib_typ_parse.helper.eval_helper as eval_helper
import lib_typ_parse.helper.eval_service as eval_service

# require code topology
# [imports] -> [L0_variables] -> [classes] -> [functions]
def assert_code_topology(current_module, item_skeleton):
    current_stage = 'S'
    index = 0
    priority_map = {
        'S' : -1,
        'include' : 0,
        'import' : 1,
        # 'instruction' : 2,
        'class' : 3,
        'fxn' : 4,
    }
    # priority_map_inv = { priority_map[x] : x for x in priority_map }
    while index < len(item_skeleton):
        # print(item_skeleton)
        item_type = item_skeleton[index]['type']
        # print(item_skeleton[index])
        if item_type not in priority_map:
            # print(item_skeleton[index])
            line = item_skeleton[index]['expression']
            error_msgs = [
                'code structure error',
                f'item {item_type} in global scope is not allowed.',
                f'line: {line}',

            ]
            exceptions.raise_exception_ue_cm(error_msgs, current_module)

        if priority_map[current_stage] > priority_map[item_type]:
            error_msgs = [
                f'code structure error in module: {current_module}',
                f'statement type: {item_type} must precede statement type: {current_stage}',
            ]
            exceptions.raise_exception_ue_cm(error_msgs, current_module)
        current_stage = item_type
        index += 1

def assert_single_main(item_skeletons):
    main_count = 0
    for item_skeleton in item_skeletons:
        module_fxns = [
            x_item['name']
            for x_item in item_skeleton
            if x_item['type'] == 'fxn'
        ]
        for i in range(0, len(module_fxns)):
            if module_fxns[i] == 'main':
                main_count += 1
    if main_count > 1:
        error_msgs = [
            'code structure error',
            'module contains multiple main methods',
            'one only main method is allowed',
        ]
        exceptions.raise_exception_ue(error_msgs)

def select_modules_to_read(item_skeleton):
    L1 = [
        x for x in item_skeleton
        if x['type'] == 'import'
    ]
    result = []
    for T1 in L1:
        T2 = [
            T3.strip()
            for T3 in T1['expression'][6:].split(' as ')
        ]
        if len(T2) != 2:
            error_msgs = [
                'invalid import statement',
                'import statement must be formatted as:',
                'import {module_name} as {module_alias}',
            ]
            exceptions.raise_exception_ue(error_msgs)
        module_name, module_alias = T2
        result.append(module_name)
    return result

def read_import_to_skeleton(item, module_L0_skeleton, current_module):
    T1 = [
        T2.strip()
        for T2 in item['expression'][6:].split(' as ')
    ]
    assert len(T1) == 2
    # print(T1)
    module_name, module_alias = T1
    module_L0_skeleton['imports']['alias_map'][module_alias] = module_name

def read_include_to_skeleton(item, module_L0_skeleton, current_module):
    c_ext_module = item['expression'][7:].strip()
    module_L0_skeleton['includes'][c_ext_module] = 1

def read_fxn_to_skeleton(item, module_L0_skeleton, current_module):
    arguments = item['arguments']
    func_name = item['name']
    fparam_ids, arg_types_typon, return_type_typon = eval_service.resolve_func_type_from_arguments_msa(arguments, module_L0_skeleton, current_module)
    module_L0_skeleton['functions'][func_name] = {
        'fparam_ids' : fparam_ids,
        'arguments' : arg_types_typon,
        'return_type' : return_type_typon,
    }

# argRepr = "( arg1 , arg2 ) -> ret"
# hasSelfRef = (arg1 == 'self')
# editedArgRepr = "( arg2 ) -> ret"
# return [hasSelfRef, editedArgRepr]
def parseClassFxnArgsRepr(argRepr):
    # "( arg1 , arg2 ) -> ret"
    s1 = argRepr.strip()
    # "arg1 , arg2 ) -> ret"
    s1 = s1[1:].strip()
    i = 0
    # parse [arg1]
    while i < len(s1):
        if not (s1[i].isalnum() or s1[i] == '_'):
            break
        i += 1
    token = s1[0:i]
    # ", arg2 ) -> ret"
    s1 = s1[i:].strip()
    if s1[0] == ',':
        s1 = s1[1:].strip()
    # s1 = "*arg2 ) -> ret"
    hasSelfRef = (token == 'self')
    editedArgRepr = f'({s1}'
    return [hasSelfRef, editedArgRepr]

# return f_arguments w/ self reference removed
# arguments = str repr of function arguments
# fmt = ( arg1 , arg2 ) -> ret
# require = ( self , typonArg1 , typonArg2 ) -> ret
# perform parsing to check argument
# return editedArgRepr (removes 'self' reference)
def check_self_ref_mem_fxn(statement, error_msg):
    argRepr = statement['arguments']
    [hasSelfRef, editedArgRepr] = parseClassFxnArgsRepr(argRepr)
    # print(argRepr, editedArgRepr)
    if not hasSelfRef:
        exceptions.raise_exception_ue(
            ['internal class function requires reference to self', error_msg]
        )
    statement['arguments'] = editedArgRepr
    return editedArgRepr

def read_class_members_to_skeleton(class_name, statement, module_L0_skeleton, current_module):
    args = check_self_ref_mem_fxn(statement, 'syntax: "def __members__(self):"')
    member_statements = statement['statements']
    module_L0_skeleton['classes'][class_name]['members'] = {}
    for i in range(0, len(member_statements)):
        assert member_statements[i]['type'] == 'instruction'
        expr = member_statements[i]['expression']
        L1 = [ x.strip() for x in expr.split(':') ]
        if len(L1) != 2:
            error_msgs = [
                'invalid class member statement',
                'class member statement must be formatted as:',
                '{member_name}: {member_type}',
            ]
            exceptions.raise_exception_ue(error_msgs)
        member_name, member_type = L1
        module_L0_skeleton['classes'][class_name]['members'][member_name] = {
            'type' : eval_helper.fmt_type_module_space_aware_module_L0_skeleton(member_type, current_module, module_L0_skeleton),
        }

def read_constructor_to_skeleton(class_name, statement, module_L0_skeleton, current_module):
    arguments = check_self_ref_mem_fxn(statement, 'syntax: "def __init__(self, [args]):"')
    fparam_ids, arg_types_typon = eval_service.resolve_args_only_func_type_msa(arguments, module_L0_skeleton, current_module)
    # assert len(fparam_ids) == len(arg_types_typon)
    # make sure there are no duplicate constructors
    constructors = module_L0_skeleton['classes'][class_name]['constructors']
    for i in range(0, len(constructors)):
        if len(constructors[i]) != len(arg_types_typon):
            continue
        matched_constructor = True
        for j in range(0, len(constructors[i])):
            if constructors[i][j][1] != arg_types_typon[j]:
                matched_constructor = False
                break
        if matched_constructor:
            S1 = ', '.join(arg_types_typon)
            error_msgs = [
                f'class {class_name} has a duplicate constructor',
                f'duplicate constructor of form: {class_name}({S1})',
            ]
            exceptions.raise_exception_ue(error_msgs)
    new_constructor = [
        [fparam_ids[i], arg_types_typon[i]]
        for i in range(0, len(arg_types_typon))
    ]
    module_L0_skeleton['classes'][class_name]['constructors'].append(new_constructor)

def read_destructor_to_skeleton(class_name, statement, module_L0_skeleton, current_module):
    arguments = check_self_ref_mem_fxn(statement, 'syntax: "def __del__(self):"')
    fparam_ids, arg_types_typon = eval_service.resolve_args_only_func_type_msa(arguments, module_L0_skeleton, current_module)
    # assert len(fparam_ids) == len(arg_types_typon)
    # make sure there are no duplicate destructors
    destructors = module_L0_skeleton['classes'][class_name]['destructors']
    for i in range(0, len(destructors)):
        if len(destructors[i]) != len(arg_types_typon):
            continue
        matched_destructor = True
        for j in range(0, len(destructors[i])):
            if destructors[i][j][1] != arg_types_typon[j]:
                matched_destructor = False
                break
        if matched_destructor:
            S1 = ', '.join(arg_types_typon)
            error_msgs = [
                f'class {class_name} has a duplicate destructor',
                f'duplicate destructor of form: {class_name}({S1})',
            ]
            exceptions.raise_exception_ue(error_msgs)
    new_destructor = [
        [fparam_ids[i], arg_types_typon[i]]
        for i in range(0, len(arg_types_typon))
    ]
    module_L0_skeleton['classes'][class_name]['destructors'].append(new_destructor)

def read_class_fxn_to_skeleton(class_name, statement, module_L0_skeleton, current_module):
    f_arguments = check_self_ref_mem_fxn(statement, 'syntax: "def [func_name](self, [args]):"')
    func_name = statement['name']
    fparam_ids, arg_types_typon, return_type_typon = eval_service.resolve_func_type_from_arguments_msa(f_arguments, module_L0_skeleton, current_module)
    module_L0_skeleton['classes'][class_name]['functions'][func_name] = {
        'fparam_ids' : fparam_ids,
        'arguments' : arg_types_typon,
        'return_type' : return_type_typon,
    }

def read_class_to_skeleton(item, module_L0_skeleton, current_module):
    statements = item['statements']
    class_name = item['name']
    read_members = False

    module_L0_skeleton['classes'][class_name] = {
        'inherits' : item['inherits'].strip(),
        'functions' : {},
        'members' : {},
        'constructors' : [],
        'destructors' : [],
    }

    # require [self] parameter in each member function of class
    for i in range(0, len(statements)):
        statement = statements[i]
        # assert statement['type'] == 'fxn'
        func_name = statement['name']
        if func_name == '__members__':
            # assert not read_members
            read_class_members_to_skeleton(class_name, statement, module_L0_skeleton, current_module)
            read_members = True
        elif func_name == '__init__':
            read_constructor_to_skeleton(class_name, statement, module_L0_skeleton, current_module)
        elif func_name == '__del__':
            read_destructor_to_skeleton(class_name, statement, module_L0_skeleton, current_module)
        else:
            read_class_fxn_to_skeleton(class_name, statement, module_L0_skeleton, current_module)

# assign L0 variable declaration to module_L0_skeleton
def read_instruction_to_skeleton(item, module_L0_skeleton, current_module):
    expression = item['expression']
    i1 = expression.find('=')
    if i1 == -1:
        return
    S1 = expression[0:i1]
    L1 = [ x.strip() for x in S1.split(':') ]
    if len(L1) != 2 or not eval_service.is_valid_var_name(L1[0]):
        return
    var_name, typon_type = L1
    module_L0_skeleton['variables'][var_name] = typon_type

def read_ordered_L0_statements(item_skeleton):
    index = 0
    A1 = ['class', 'fxn']
    X1 = { x : 1 for x in A1 }
    while index < len(item_skeleton):
        if item_skeleton[index]['type'] in X1:
            break
        index += 1
    return item_skeleton[index:]

def format_L0_skeleton(item_skeleton, current_module, code):
    module_L0_skeleton = {
        'includes' : {},
        'imports' : {
            'alias_map' : {},
        },
        'ordered_L0_statements' : read_ordered_L0_statements(item_skeleton),
        'module_src' : code,
        'classes' : {},
        'functions' : {},
        'variables' : {},
    }
    parsing_router = {
        'fxn' : read_fxn_to_skeleton,
        'class' : read_class_to_skeleton,
        'import' : read_import_to_skeleton,
        'include' : read_include_to_skeleton,
        'instruction' : read_instruction_to_skeleton,
    }
    for i in range(0, len(item_skeleton)):
        item = item_skeleton[i]
        item_type = item['type']
        parsing_router[item_type](item, module_L0_skeleton, current_module)

    return module_L0_skeleton

def read_L0_skeleton(current_module, item_skeleton, code):
    try:
        assert_code_topology(current_module, item_skeleton)
        modules_to_read = select_modules_to_read(item_skeleton)
        module_L0_skeleton = format_L0_skeleton(item_skeleton, current_module, code)
    except Exception as e:
        e_msg = f'''
error reading module: {current_module}
error_msg: {str(e)}
'''
        traceback.print_exc()
        exit(1)
        # raise Exception(e_msg)

    return modules_to_read, module_L0_skeleton

def fmt_code(src_dir):
    S1 = open(src_dir, 'r').read()
    L1 = S1.splitlines()
    L2 = []
    for line in L1:
        l1 = line.lstrip()
        if len(l1) == 0:
            L2.append(l1)
            continue
        if l1[0] == '#':
            L2.append('')
            continue
        L2.append(line)

    L2.append('')
    result = '\n'.join(L2)
    return result

# module_dir -> base directory of module
def select_code_skeletons(target_module, module_dir):
    q = [target_module]
    L0_skeleton = {}
    # item_skeletons = {}
    visited_modules = {}
    # source_codes = {}
    included_c_exts_map = {}
    while len(q) > 0:
        current_module = q.pop()
        # print(current_module)
        if current_module in visited_modules:
            continue
        src_dir = fmt_utils.select_module_src_dir(module_dir, current_module)
        code = fmt_code(src_dir)
        # print(current_module, src_dir)

        try:
            item_skeleton, end_index = parser.read_scope(code, 0, 0)
        except Exception as e:
            traceback.print_exc()
            print(src_dir)
            exit(1)
            # exceptions.raise_parsing_exception(str(e), current_module, src_dir)
        # fmt_utils.print_json(item_skeleton)
        modules_to_read, module_L0_skeleton = read_L0_skeleton(current_module, item_skeleton, code)
        visited_modules[current_module] = 1
        # item_skeletons.append(item_skeleton)
        q += [
            typon_module
            for typon_module in modules_to_read
            if typon_module not in visited_modules
        ]
        L0_skeleton[current_module] = module_L0_skeleton
        for x in item_skeleton:
            if x['type'] == 'include':
                included_c_exts_map[x['expression'][7:].strip()] = 1
        # item_skeletons[current_module] = item_skeleton
        # source_codes[current_module] = code

    # assert_single_main(item_skeletons)
    L0_skeleton['#namespace_mapping'] = {}
    L0_skeleton['#namespace_mapping']['included_c_exts'] = [ x for x in included_c_exts_map ]
    # S1 = fmt_utils.print_json(L0_skeleton)
    return L0_skeleton
