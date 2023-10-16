import lib_typ_parse.utils.parsing_utils as parsing_utils
import lib_typ_parse.utils.exceptions as exceptions
import lib_typ_parse.utils.constants as constants

def reduce_rel_type( target_module, current_module, rel_type, reverse_imports_map ):
    target_rel = f'{rel_type}'
    if target_module != current_module:
        import_alias = reverse_imports_map[current_module][target_module]
        target_rel = f'{import_alias}.{rel_type}'
    return target_rel

# return target_module, type_name
def compute_relative_type(abs_type, current_module, reverse_imports_map):
    S1 = abs_type.replace(' ', '')
    c_ext_type_prefix = constants.select_item_prefix('c_ext_type_prefix')
    primitives_map = constants.select_primitives()

    # print(S1)

    if S1 in primitives_map:
        return current_module, S1

    if S1[0:3] == c_ext_type_prefix:
        return current_module, S1

    if S1[0:4] == 'vec[':
        item_type = S1[4:-1]
        item_module, item_rel_type = compute_relative_type(item_type, current_module, reverse_imports_map)
        item_rel = reduce_rel_type( item_module, current_module, item_rel_type, reverse_imports_map )
        return current_module, f'vec[{item_rel}]'

    if S1[0:5] == 'hmap[':
        key_type, value_type = resolve_map_type_L0_skeleton(S1, reverse_imports_map)
        key_module, key_rel_type = compute_relative_type(key_type, current_module, reverse_imports_map)
        value_module, value_rel_type = compute_relative_type(value_type, current_module, reverse_imports_map)

        key_rel = reduce_rel_type( key_module, current_module, key_rel_type, reverse_imports_map )
        value_rel = reduce_rel_type( value_module, current_module, value_rel_type, reverse_imports_map )

        return current_module, f'hmap[{key_rel}, {value_rel}]'

    if S1[0:5] == 'smap[':
        key_type, value_type = resolve_map_type_L0_skeleton(S1, reverse_imports_map)
        key_module, key_rel_type = compute_relative_type(key_type, current_module, reverse_imports_map)
        value_module, value_rel_type = compute_relative_type(value_type, current_module, reverse_imports_map)

        key_rel = reduce_rel_type( key_module, current_module, key_rel_type, reverse_imports_map )
        value_rel = reduce_rel_type( value_module, current_module, value_rel_type, reverse_imports_map )

        return current_module, f'smap[{key_rel}, {value_rel}]'

    if S1[0:5] == 'tupl[':
        typon_tuple_typon_type_list = read_tuple_types_typon_L0_skeleton(S1, reverse_imports_map)
        tuple_rel_types = []
        for arg_type in typon_tuple_typon_type_list:
            item_module, item_rel_type = compute_relative_type(arg_type, current_module, reverse_imports_map)
            item_rel = reduce_rel_type( item_module, current_module, item_rel_type, reverse_imports_map )
            tuple_rel_types.append(item_rel)

        S2 = ', '.join(tuple_rel_types)
        return current_module, f'tupl[{S2}]'

    if S1[0:4] == 'fxn[':
        arg_types_typon, return_type_typon = read_args_ret_from_fxn_typon_type(S1)
        arg_rel_types = []
        for arg_type in arg_types_typon:
            item_module, item_rel_type = compute_relative_type(arg_type, current_module, reverse_imports_map)
            item_rel = reduce_rel_type( item_module, current_module, item_rel_type, reverse_imports_map )
            arg_rel_types.append(item_rel)

        ret_module, ret_rel_type = compute_relative_type(return_type_typon, current_module, reverse_imports_map)
        ret_rel = reduce_rel_type( ret_module, current_module, ret_rel_type, reverse_imports_map )
        S2 = ', '.join(arg_rel_types)
        return current_module, f'fxn[[{S2}], {ret_rel}]'

    user_defined_typon_class_type = S1

    if user_defined_typon_class_type.find('|') != -1:
        target_module, type_name = user_defined_typon_class_type.split('|')
        return target_module, type_name

    i1 = user_defined_typon_class_type.find('.')
    if i1 == -1:
        return current_module, user_defined_typon_class_type

    # module, type = user_defined_typon_class_type.split('.')
    # return module, type
    # invalid case: not [abs_module]|[type_name]
    raise Exception(f'could not parse type: {abs_type}' )

# L0_skeleton parameter not required
def resolve_map_type_L0_skeleton(typon_map_type, L0_skeleton):
    assert typon_map_type[0:5] in ['hmap[', 'smap[']
    S1 = typon_map_type.replace(' ', '')
    type_str = S1[5:-1]
    typon_typle = parsing_utils.read_delimited_types(type_str)
    # print(type_str, typon_typle)
    assert len(typon_typle) == 2
    map_key_type, map_value_type = typon_typle
    return map_key_type, map_value_type

# L0_skeleton parameter not required
def read_tuple_types_typon_L0_skeleton(ws_removed_typon_tuple_type, L0_skeleton):
    ws_removed_typon_tuple_type = ws_removed_typon_tuple_type.replace(' ', '')
    interior_tuple_type_str = ws_removed_typon_tuple_type[5:-1]
    if len(interior_tuple_type_str) == 0:
        error_msgs = [
            'invalid type declaration',
            f'empty tuple not allowed: {ws_removed_typon_tuple_type}',
        ]
        exceptions.raise_exception_ue(error_msgs)
    typon_tuple_typon_type_list = parsing_utils.read_delimited_types(interior_tuple_type_str)
    return typon_tuple_typon_type_list

def read_args_ret_from_fxn_typon_type(ws_removed_typon_fxn_type):
    # assert ws_removed_typon_fxn_type[0:4] == 'fxn['
    # interior_fxn_type = "[{arg_types_typon}],{return_type_typon}"
    interior_fxn_type = ws_removed_typon_fxn_type[4:-1]
    if len(interior_fxn_type) == 0:
        error_msgs = [
            'invalid type declaration',
            f'empty fxn not allowed: {ws_removed_typon_fxn_type}',
        ]
        exceptions.raise_exception_ue(error_msgs)
    # assert interior_fxn_type[0] == '['
    arg_closure_index = parsing_utils.get_char_closure(interior_fxn_type, 1)
    # typon_fxn_arg_str = "{arg_types_typon}"
    typon_fxn_arg_str = interior_fxn_type[1:arg_closure_index-1]
    arg_types_typon = parsing_utils.read_delimited_types(typon_fxn_arg_str)
    # assert interior_fxn_type[arg_closure_index] == ','
    return_type_typon = interior_fxn_type[arg_closure_index+1:]
    return arg_types_typon, return_type_typon
