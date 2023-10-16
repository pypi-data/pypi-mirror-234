def select_item_prefix(item_name):
    item_router = {
        'fxn' : 'F',
        'fxn_param' : 'P',
        'namespace' : 'NS',
        'class' : 'C',
        'class_member' : 'A',
        'class_fxn' : 'F',
        'local_var' : 'T',
        'for_loop_index' : 'i',
        'key_value_index' : 'kv',
        'c_ext_type_prefix' : '@c.'
    }
    return item_router[item_name]

def select_primitives():
    ptype_map_V1 = {
        'void' : 'void',
        'fileptr' : 'FILE *',
        'thread' : 'std::thread',
        'semaphore' : 'semaphore *',
        'int' : 'long int',
        'uint32' : 'unsigned int',
        'uint64' : 'unsigned long int',
        'int32' : 'int',
        'dbl' : 'double',
        'char' : 'char',
        'bool' : 'bool',
        'str' : 'std::string',
    }
    return ptype_map_V1

def select_bracket_map():
    t_tokens = '[](){}'
    t_mapper = {
        t_tokens[2 * i] : t_tokens[2 * i + 1]
        for i in range(0, len(t_tokens) // 2)
    }
    return t_mapper
