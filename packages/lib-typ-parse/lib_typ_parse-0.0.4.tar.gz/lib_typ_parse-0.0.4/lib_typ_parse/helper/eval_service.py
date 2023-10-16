import lib_typ_parse.helper.eval_helper as eval_helper
import lib_typ_parse.utils.exceptions as exceptions

# input: "([arguments]) -> [return_type]"
# returns fparam_ids, arg_types_typon, return_type_typon
def resolve_func_type_from_arguments(arguments):
    T1 = [
        T2.strip()
        for T2 in arguments.split('->')
    ]
    if len(T1) != 2:
        error_msgs = [
            'invalid fxn statement',
            'fxn statement must be formatted as:',
            'fxn ({arguments}) -> {return_type}:',
            f'input: {arguments}',
        ]
        exceptions.raise_exception_ue(error_msgs)

    fparam_ids, arg_types_typon = eval_helper.read_fxn_params(T1[0])
    return_type_typon = T1[1]

    return fparam_ids, arg_types_typon, return_type_typon

# input: "([arguments])"
# returns fparam_ids, arg_types_typon
def resolve_args_only_func_type(arguments):
    T1 = [
        T2.strip()
        for T2 in arguments.split('->')
    ]
    if len(T1) != 1:
        error_msgs = [
            'invalid fxn argument declaration',
            'arguments must be formatted as:',
            '({arg_1}: {type_1}, ..., {arg_i}: {type_i}, ..., {arg_n}: {type_n})',
            f'input: {arguments}',
        ]
        exceptions.raise_exception_ue(error_msgs)

    fparam_ids, arg_types_typon = eval_helper.read_fxn_params(T1[0])

    return fparam_ids, arg_types_typon

# input: "([arguments]) -> [return_type]"
# module space aware
# returns fparam_ids, arg_types_typon, return_type_typon
def resolve_func_type_from_arguments_msa(arguments, module_L0_skeleton, current_module):
    fparam_ids, arg_types_typon, return_type_typon = resolve_func_type_from_arguments(arguments)
    arg_types_typon_msa = [
        eval_helper.fmt_type_module_space_aware_module_L0_skeleton(arg_type_typon, current_module, module_L0_skeleton)
        for arg_type_typon in arg_types_typon
    ]
    return_type_typon_msa = eval_helper.fmt_type_module_space_aware_module_L0_skeleton(return_type_typon, current_module, module_L0_skeleton)
    return fparam_ids, arg_types_typon_msa, return_type_typon_msa

# input: "([arguments])"
# returns fparam_ids, arg_types_typon
def resolve_args_only_func_type_msa(arguments, module_L0_skeleton, current_module):
    fparam_ids, arg_types_typon = resolve_args_only_func_type(arguments)
    arg_types_typon_msa = [
        eval_helper.fmt_type_module_space_aware_module_L0_skeleton(arg_type_typon, current_module, module_L0_skeleton)
        for arg_type_typon in arg_types_typon
    ]
    return fparam_ids, arg_types_typon_msa

def is_valid_var_name(var_name):
    for i in range(0, len(var_name)):
        if not var_name[i].isalnum() and var_name[i] != '_':
            return False
    return True
