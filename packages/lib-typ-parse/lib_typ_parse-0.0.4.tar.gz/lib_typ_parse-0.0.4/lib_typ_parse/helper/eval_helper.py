import lib_typ_parse.utils.constants as constants
import lib_typ_parse.utils.exceptions as exceptions
import lib_typ_parse.utils.parsing_utils as parsing_utils
import lib_typ_parse.helper.type_resolver as type_resolver

def extract_id_var_tuple(S2):
    L1 = [x.strip() for x in S2.split(':')]
    if len(L1) != 2:
        error_msgs = [
            'invalid fxn argument declaration',
            'arguments must be formatted as:',
            '({arg_1}: {type_1}, ..., {arg_i}: {type_i}, ..., {arg_n}: {type_n})',
            f'input: {S2}',
        ]
        exceptions.raise_exception_ue(error_msgs)
    # fparam_id, arg_type_typon = L1
    return L1

# input: "([arguments])"
# returns fparam_ids, arg_types_typon
def read_fxn_params(arg_str):
    S1 = arg_str[1:-1]
    if len(S1) == 0:
        return [], []
    fparam_ids = []
    arg_types_typon = []
    i1 = 0
    index = 0
    while index < len(S1):
        if S1[index] == '[':
            index = parsing_utils.get_char_closure(S1, index+1)
            continue
        if S1[index] == ',':
            S2 = S1[i1:index]
            fparam_id, arg_type_typon = extract_id_var_tuple(S2)
            fparam_ids.append(fparam_id)
            arg_types_typon.append(arg_type_typon)
            i1 = index + 1
        index += 1
    if i1 < index:
        S2 = S1[i1:index]
        fparam_id, arg_type_typon = extract_id_var_tuple(S2)
        fparam_ids.append(fparam_id)
        arg_types_typon.append(arg_type_typon)
    return fparam_ids, arg_types_typon

def fmt_type_module_space_aware_module_L0_skeleton(input_typon_type, current_module, module_L0_skeleton):
    S1 = input_typon_type.replace(' ', '')
    c_ext_type_prefix = constants.select_item_prefix('c_ext_type_prefix')
    primitives_map = constants.select_primitives()

    if S1 in primitives_map:
        return S1

    if S1[0:3] == c_ext_type_prefix:
        return S1

    if S1[0:4] == 'vec[':
        item_type = S1[4:-1]
        item_type_msa = fmt_type_module_space_aware_module_L0_skeleton(item_type, current_module, module_L0_skeleton)
        return f'vec[{item_type_msa}]'

    if S1[0:5] == 'hmap[':
        key_type, value_type = type_resolver.resolve_map_type_L0_skeleton(S1, module_L0_skeleton)
        key_type_msa = fmt_type_module_space_aware_module_L0_skeleton(key_type, current_module, module_L0_skeleton)
        value_type_msa = fmt_type_module_space_aware_module_L0_skeleton(value_type, current_module, module_L0_skeleton)
        return f'hmap[{key_type_msa}, {value_type_msa}]'

    if S1[0:5] == 'smap[':
        key_type, value_type = type_resolver.resolve_map_type_L0_skeleton(S1, module_L0_skeleton)
        key_type_msa = fmt_type_module_space_aware_module_L0_skeleton(key_type, current_module, module_L0_skeleton)
        value_type_msa = fmt_type_module_space_aware_module_L0_skeleton(value_type, current_module, module_L0_skeleton)
        return f'smap[{key_type_msa}, {value_type_msa}]'

    if S1[0:5] == 'tupl[':
        typon_tuple_typon_type_list = type_resolver.read_tuple_types_typon_L0_skeleton(S1, module_L0_skeleton)
        L1 = [
            fmt_type_module_space_aware_module_L0_skeleton(T1, current_module, module_L0_skeleton)
            for T1 in typon_tuple_typon_type_list
        ]
        S2 = ', '.join(L1)
        return f'tupl[{S2}]'

    if S1[0:4] == 'fxn[':
        arg_types_typon, return_type_typon = type_resolver.read_args_ret_from_fxn_typon_type(S1)
        L1 = [
            fmt_type_module_space_aware_module_L0_skeleton(T1, current_module, module_L0_skeleton)
            for T1 in arg_types_typon
        ]
        return_type_typon_msa = fmt_type_module_space_aware_module_L0_skeleton(return_type_typon, current_module, module_L0_skeleton)
        S2 = ', '.join(L1)
        return f'fxn[[{S2}], {return_type_typon_msa}]'

    user_defined_typon_class_type = S1

    if user_defined_typon_class_type.find('|') != -1:
        return f'{user_defined_typon_class_type}'

    i1 = user_defined_typon_class_type.find('.')
    if i1 == -1:
        return f'{current_module}|{user_defined_typon_class_type}'
    L1 = user_defined_typon_class_type.split('.')
    assert len(L1) == 2
    module_alias, class_name = L1

    # print(current_module, module_alias)
    if module_alias not in module_L0_skeleton['imports']['alias_map']:
        e_msg = f'cannot find module_alias: {module_alias} in current_module: {current_module}'
        raise Exception(e_msg)

    fully_qualified_module_name = module_L0_skeleton['imports']['alias_map'][module_alias]
    # print(fully_qualified_module_name)
    return f'{fully_qualified_module_name}|{class_name}'

    # error_msgs = ['Error resolving equivalent c++ type', f'typon type: {typon_type}']
    # error_msgs = ['Error resolving typon type', f'typon type: {typon_type}']
    # exceptions.raise_exception_ST(error_msgs, current_module, module_L0_skeleton)
